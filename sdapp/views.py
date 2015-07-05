from collections import defaultdict
import datetime
from decimal import Decimal
from math import sqrt
import pytz
import time
import urllib

from django.shortcuts import (render_to_response, redirect,
                              RequestContext, HttpResponseRedirect)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, Sum
from django.template.defaulttags import register

from sdapp.models import (Security, Signal, SecurityPriceHist,
                          Form345Entry, PersonHoldingView, SecurityView,
                          Affiliation, Recommendation,
                          ClosePrice, WatchedName)
from sdapp.misc.filingcodes import filingcodes, acq_disp_codes
from sdapp import holdingbuild

# from django.core.context_processors import csrf
# from django.db.models import Count

# def check_auth(request):
#     if request.user.is_authenticated():
#         return True
#     else:
#         messagetext = \
#             'Login required for access'
#         messages.success(request, messagetext)
#         return False


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def mean(lst):
    # """calculates mean"""
    lstsum = Decimal(0)
    for i in range(len(lst)):
        lstsum += lst[i]
    return (lstsum / len(lst))


def stddev(lst):
    # """calculates standard deviation"""
    lstsum = Decimal(0)
    mn = mean(lst)
    for entry in lst:
        lstsum += pow((entry - mn), 2)
    return sqrt(lstsum / Decimal(len(lst) - 1))


def dotproduct(four_column_table):
    dotprod = sum(Decimal(r) * Decimal(s) for p, q, r, s in four_column_table)
    return dotprod


def js_readable_date(some_datetime_object):
    timetuple = some_datetime_object.timetuple()
    timestamp = time.mktime(timetuple)
    return timestamp * 1000.0


# converts date to datetime, but ignores None
def nd(dt):
    try:
        return dt.date()
    except:
        return dt


def index(request):
    sphset = SecurityPriceHist.objects.exclude(issuer=None)\
        .order_by('ticker_sym')
    for sph in sphset:
        sph.name = sph.issuer.name

    return render_to_response('sdapp/index.html',
                              {'sphset': sphset,
                               },
                              context_instance=RequestContext(request),
                              )


@login_required()
def options(request, ticker):
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    issuer_name = issuer.name
    # Pulls whether this stock is on the user's watch list
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)

    signals = Signal.objects.filter(issuer=issuer)\
        .order_by('-signal_date')
    persons_data = \
        signals.exclude(reporting_person=None)\
        .values_list('reporting_person', 'reporting_person_name')
    graph_data_json, titles_json, ymax =\
        holdingbuild.buildgraphdata(issuer, ticker, persons_data)

    # print prices_json, titles_json

    signals = Signal.objects.filter(issuer=issuer)\
        .order_by('-signal_date')
    sig_highlights = []
    for signal in signals:
        sig_highlights.append(
            [js_readable_date(signal.signal_date + datetime.timedelta(-5)),
             js_readable_date(signal.signal_date + datetime.timedelta(5))])

    recset = Recommendation.objects.filter(issuer=issuer)
    if recset.exists():
        rec = recset[0]
    else:
        rec = None

    issuer_affiliations = Affiliation.objects.filter(issuer=issuer)
    ann_affiliations = issuer_affiliations\
        .annotate(intrinsic_value=Sum('personholdingview__intrinsic_value'))\
        .exclude(intrinsic_value=None).order_by('-intrinsic_value')[:3]

    return render_to_response('sdapp/options.html',
                              {'ann_affiliations': ann_affiliations,
                               'issuer_name': issuer_name,
                               'graph_data_json': graph_data_json,
                               'rec': rec,
                               'sig_highlights': sig_highlights,
                               'signals': signals,
                               'titles_json': titles_json,
                               'ticker': ticker,
                               'watchedname': watchedname,
                               'ymax': ymax,
                               },
                              context_instance=RequestContext(request),
                              )


@login_required()
def drilldown(request, ticker):
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    issuer_name = issuer.name
    # Pulls whether this stock is on the user's watch list
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)

    signals = Signal.objects.filter(issuer=issuer)\
        .order_by('-signal_date')

    now = datetime.datetime.now(pytz.UTC)
    startdate = now - datetime.timedelta(270)
    # Builds transaction queryset
    recententries_qs =\
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(filedatetime__gte=startdate)
    persons_for_radio =\
        recententries_qs\
        .values('reporting_owner_name', 'reporting_owner_cik')\
        .order_by('reporting_owner_name').distinct()
    # Creates variable to be used to filter by person
    if 'person_cik' in request.GET:
        selected_person = int(request.GET['person_cik'])
        recententries_qs =\
            recententries_qs.filter(reporting_owner_cik=selected_person)
    else:
        selected_person = None
    recententries =\
        recententries_qs\
        .order_by('-filedatetime', 'transaction_number')\
        .values('filedatetime', 'transaction_number', 'transaction_date',
                'reporting_owner_cik', 'reporting_owner_name',
                'transaction_code', 'xn_acq_disp_code',
                'transaction_shares', 'security_title',
                'xn_price_per_share', 'conversion_price', 'sec_path',
                'form_type', 'reported_shares_following_xn',
                'is_director', 'is_officer', 'is_ten_percent')
    # Creates variable to filter graph by person
    if selected_person is None:
        persons_data =\
            Affiliation.objects.filter(issuer=issuer)\
            .values_list('reporting_owner', 'person_name')
    else:
        persons_data =\
            Affiliation.objects.filter(issuer=issuer)\
            .filter(reporting_owner=selected_person)\
            .values_list('reporting_owner', 'person_name')
    persons_with_data = len(persons_data)
    # builds graph data -- see housingbuild.py for logic
    graph_data_json, titles_json, ymax =\
        holdingbuild.buildgraphdata(issuer, ticker, persons_data)

    sig_highlights = []
    for signal in signals:
        sig_highlights.append(
            [js_readable_date(signal.signal_date + datetime.timedelta(-5)),
             js_readable_date(signal.signal_date + datetime.timedelta(5))])

    return render_to_response('sdapp/drilldown.html',
                              {'acq_disp_codes': acq_disp_codes,
                               'recententries': recententries,
                               'filingcodes': filingcodes,
                               'graph_data_json': graph_data_json,
                               'issuer_name': issuer_name,
                               'persons_for_radio': persons_for_radio,
                               'persons_with_data': persons_with_data,
                               'selected_person': selected_person,
                               'sig_highlights': sig_highlights,
                               'signals': signals,
                               'titles_json': titles_json,
                               'ticker': ticker,
                               'watchedname': watchedname,
                               'ymax': ymax,
                               },
                              context_instance=RequestContext(request),
                              )


@login_required()
def watchtoggle(request, ticker):
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    print 'watchedname', watchedname
    print 'watchedname.exists()', watchedname.exists()
    if watchedname.exists():
        watchedname.delete()
        messagetext = \
            'Removed from watchlist'
        messages.info(request, messagetext)
        if 'HTTP_REFERER' in request.META:
            url = request.META['HTTP_REFERER']
            if url.find('/?') != -1:
                url = url[:url.find('/?')]
            return redirect(url)
        return HttpResponseRedirect('/sdapp/' + str(ticker))
    else:
        sph = SecurityPriceHist.objects.filter(ticker_sym=ticker)[0]
        signals = Signal.objects.filter(issuer=issuer)
        if signals.exists():
            last_signal_sent = signals.latest('signal_date').signal_date
        else:
            last_signal_sent = None
        WatchedName(user=request.user,
                    issuer=issuer,
                    securitypricehist=sph,
                    ticker_sym=ticker,
                    last_signal_sent=last_signal_sent).save()
        messagetext = \
            'Added to watchlist'
        messages.info(request, messagetext)
        if 'HTTP_REFERER' in request.META:
            return redirect(request.META['HTTP_REFERER'])
        return HttpResponseRedirect('/sdapp/' + str(ticker))


# class filterscreens(ListView):

#     # c = {}
#     # c.update(csrf(request))

#     template_name = 'sdapp/filterscreens.html'
#     context_object_name = 'screens'

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(filterscreens, self).dispatch(*args, **kwargs)

#     def get_queryset(self):
#         print self
#         self.issuer = get_object_or_404(IssuerCIK, cik_num=self.args[0])
#         return Signal.objects.filter(issuer=self.issuer)


# def search(request):
#     query_string = ''
#     found_entries = None
#     if ('q' in request.GET) and request.GET['q'].strip():
#         query_string = request.GET['q']
#
#         entry_query = get_query(query_string, ['title', 'body',])
#
#         found_entries = Entry.objects.filter(entry_query)\
#             .order_by('-pub_date')
#
#     return render_to_response('search/search_results.html',
#                           { 'query_string': query_string,
#                             'found_entries': found_entries },
#                           context_instance=RequestContext(request))


def filterintermed(request):
    cik_num = request.POST.get('cik_num', '')
    if cik_num is not '':
        return HttpResponseRedirect('/sdapp/screens/' + cik_num + '/')
    else:
        return HttpResponseRedirect('/sdapp/screens/')


def tickersearch(request):

    if 'ticker' in request.GET\
            and 'HTTP_REFERER' in request.META\
            and request.GET['ticker'].strip() == '':
        messagetext = \
            'Please enter a ticker.'
        messages.success(request, messagetext)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if ('ticker' in request.GET)\
            and SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['ticker'].strip().upper()).exists()\
            and SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['ticker'].strip().upper())[0]\
            .issuer is not None:
        ticker = request.GET['ticker'].strip().upper()
        return HttpResponseRedirect('/sdapp/' + str(ticker))

    else:
        messagetext = \
            'Ticker Not Found'
        messages.success(request, messagetext)
        return HttpResponseRedirect('/sdapp/')


@login_required()
def screens(request):
    query_string = None
    found_entries = None
    signal_types = []
    dbuyactive = True
    wbuyactive = True
    ticker = None
    num_of_records = None
    watchlist = \
        WatchedName.objects.filter(user=request.user).order_by('ticker_sym')
    #
    # Search results (if there was a search)
    if ('q' in request.GET):
        query_string = request.GET['q'].strip()
        dbuyactive = False
        wbuyactive = False

    if 'selectbox' in request.GET\
            and 'discretionarybuy' in request.GET.getlist('selectbox'):
        signal_types.append('Discretionary Buy')
        dbuyactive = True

    if 'selectbox' in request.GET\
            and 'buyonweakness' in request.GET.getlist('selectbox'):
        signal_types.append('Discretionary Buy after a Decline')
        wbuyactive = True

    # THE BELOW COMMENTED CODE WOULD BE USED FOR THE TOGGLE BUTTON
    # CHECKBOXES IN THE SCREENS.HTML TEMPLATE INSTEAD OF THE ABOVE
    # if 'discretionarybuy' in request.GET:
    #     signal_types.append('Discretionary Buy')
    #     dbuyactive = True
    #     # print 'discretionarybuy', request.GET['discretionarybuy'].strip()
    # if 'buyonweakness' in request.GET:
    #     signal_types.append('Discretionary Buy after a Decline')
    #     wbuyactive = True
    #     # print 'buyonweakness', request.GET['buyonweakness'].strip()

    if ('q' in request.GET) and\
            SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['q'].strip().upper()).exists() and\
            SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['q'].strip().upper())[0]\
            .issuer is not None:
        ticker = request.GET['q'].strip().upper()
        issuer = SecurityPriceHist.objects\
            .filter(ticker_sym=query_string.upper())[0].issuer
        found_entries = \
            Signal.objects.filter(signal_name__in=signal_types)\
            .filter(issuer=issuer).order_by('-signal_date')
        num_of_records = found_entries.count()
    elif ('q' in request.GET) and\
            request.GET['q'].strip() == '':
        query_string = ' '
        found_entries = \
            Signal.objects.filter(signal_name__in=signal_types)\
            .order_by('-signal_date')
        num_of_records = found_entries.count()

    return render_to_response('sdapp/screens.html',
                              {'dbuyactive': dbuyactive,
                               'found_entries': found_entries,
                               'num_of_records': num_of_records,
                               'query_string': query_string,
                               'ticker': ticker,
                               'watchlist': watchlist,
                               'wbuyactive': wbuyactive,
                               },
                              context_instance=RequestContext(request),
                              )


@login_required()
def discretionarybuy(request):
    signal_name_1 = 'Discretionary Buy'
    signal_name_2 = 'Discretionary Buy after a Decline'
    qs = Signal.objects\
        .filter(Q(signal_name=signal_name_1) |
                Q(signal_name=signal_name_2))\
        .order_by('-signal_date')

    return render_to_response('sdapp/discretionarybuy.html',
                              {'signals': qs},
                              context_instance=RequestContext(request),
                              )


@login_required()
def weaknessbuy(request):
    signal_name = 'Discretionary Buy after a Decline'
    qs = Signal.objects\
        .filter(signal_name=signal_name)\
        .order_by('-signal_date')

    return render_to_response('sdapp/weaknessbuy.html',
                              {'signals': qs},
                              context_instance=RequestContext(request),
                              )


@login_required()
def formentrydetail(request, ticker):
    headtitle = 'All Entries'
    security_obj = \
        Security.objects.get(ticker=ticker)
    issuer = security_obj.issuer
    issuer_pk = security_obj.issuer.pk
    entrylist = Form345Entry.objects.filter(issuer_cik_id=issuer_pk)\
        .order_by('reporting_owner_cik', 'security', '-filedatetime')
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    return render_to_response('sdapp/formentrydetail.html',
                              {'headtitle': headtitle,
                               'entrylist': entrylist,
                               'ticker': ticker,
                               'issuer': issuer,
                               'issuer_pk': issuer_pk,
                               'watchedname': watchedname, },
                              context_instance=RequestContext(request),)


@login_required()
def holdingdetail(request, ticker):
    headtitle = 'Current Holdings'
    security_obj = \
        Security.objects.get(ticker=ticker)
    issuer = security_obj.issuer
    issuer_pk = security_obj.issuer.pk
    entrylist = Form345Entry.objects\
        .filter(issuer_cik_id=issuer_pk)\
        .filter(supersededdt=None)\
        .order_by('reporting_owner_cik', 'security', '-filedatetime')
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    return render_to_response('sdapp/formentrydetail.html',
                              {'headtitle': headtitle,
                               'entrylist': entrylist,
                               'ticker': ticker,
                               'issuer': issuer,
                               'issuer_pk': issuer_pk,
                               'watchedname': watchedname, },
                              context_instance=RequestContext(request),)


@login_required()
def byperson(request, ticker):
    issuer = \
        Security.objects.get(ticker=ticker).issuer
    personviews = PersonHoldingView.objects.filter(issuer=issuer)\
        .order_by('person_name', '-intrinsic_value')
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    return render_to_response('sdapp/personviews.html',
                              {'ticker': ticker,
                               'issuer_pk': issuer.pk,
                               'personviews': personviews,
                               'watchedname': watchedname, },
                              context_instance=RequestContext(request),)


def compile_holdings_into_table(person_view_set, total_view_set,
                                deriv_or_nonderiv):
    sec_ids_titles = \
        total_view_set\
        .filter(deriv_or_nonderiv=deriv_or_nonderiv)\
        .values_list('security', 'short_sec_title').distinct()\
        .order_by('-intrinsic_value')
    holding_lists = []
    for security_id, short_sec_title in sec_ids_titles:
        sec_holdings = person_view_set.filter(security_id=security_id)\
            .order_by('-units_held')[:5]
        total = total_view_set.filter(security=security_id)[0]
        holding_list = [short_sec_title, sec_holdings, total]
        holding_lists.append(holding_list)
    return holding_lists


@login_required()
def holdingtable(request, ticker):
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    issuer_name = Form345Entry.objects.filter(issuer_cik=issuer)\
        .latest('filedatetime').issuer_name

    person_view_set = PersonHoldingView.objects.filter(issuer=issuer)\
        .exclude(units_held=0.0).exclude(units_held=None)

    total_view_set = SecurityView.objects.filter(issuer=issuer)\
        .exclude(units_held=0.0).exclude(units_held=None)
    non_deriv_table = \
        compile_holdings_into_table(person_view_set, total_view_set, 'N')
    deriv_table = \
        compile_holdings_into_table(person_view_set, total_view_set, 'D')
    return render_to_response('sdapp/holdingtable.html',
                              {'ticker': ticker,
                               'issuer_name': issuer_name,
                               'non_deriv_table': non_deriv_table,
                               'deriv_table': deriv_table,
                               'watchedname': watchedname, },
                              context_instance=RequestContext(request),
                              )


# def holdingtable(request, ticker):
#     issuer = \
#         IssuerCIK.objects.filter(SecurityPriceHist__ticker_sym=ticker_sym)[0]
#     lookbackdays = 365 * 100
#     startdate = datetime.date.today() - datetime.timedelta(lookbackdays)
#     affiliationset = Affiliation.objects.filter(issuer=issuer)\
#         .filter(most_recent_filing__gte=startdate)
#     holdingset = HoldingType.objects.filter(issuer=issuer)\
#         .filter(affiliation__in=affiliationset).order_by('owner')\
#         .exclude(units_held=0.0).exclude(units_held=None)
#     stockholdingset = holdingset.filter(deriv_or_nonderiv='N')
#     stockholdingtitles = list(set(stockholdingset
#                               .values_list('security_title', flat=True)
#                               .distinct()))
#     totalset = AggHoldingType.objects.filter(issuer=issuer)\
#         .exclude(units_held=None)
#     stocktotals = totalset.filter(deriv_or_nonderiv='N')
#     stockholdinglists = []
#     for title in stockholdingtitles:
#         stockholdinglist = []
#         stockholdinglist.append(title)
#         titleholdings = stockholdingset.filter(security_title=title)\
#             .order_by('-units_held')[:5]
#         # print titleholdings.values_list('owner', flat=True)
#         stockholdinglist.append(titleholdings)

#         total = stocktotals.filter(security_title=title)[0]
#         stockholdinglist.append(total)
#         stockholdinglists.append(stockholdinglist)
#         # print title
#         # print stockholdinglist

#     derivholdingset = holdingset.filter(deriv_or_nonderiv='D')
#     derivholdingtitles = list(set(derivholdingset
#                               .values_list('security_title', flat=True)
#                               .distinct()))
#     derivtotals = totalset.filter(deriv_or_nonderiv='D')
#     derivholdinglists = []
#     for title in derivholdingtitles:
#         derivholdinglist = []
#         derivholdinglist.append(title)
#         titleholdings = derivholdingset.filter(security_title=title)\
#             .order_by('-units_held')[:5]
#         derivholdinglist.append(titleholdings)
#         total = derivtotals.filter(security_title=title)[0]
#         derivholdinglist.append(total)
#         derivholdinglists.append(derivholdinglist)
#     # print stockholdinglists
#     return render_to_response('sdapp/holdingtable.html',
#                               {'ticker_sym': ticker_sym,
#                                'startdate': startdate,
#                                'stockholdingtitles': stockholdingtitles,
#                                'affiliationset': affiliationset,
#                                'stockholdinglists': stockholdinglists,
#                                'derivholdinglists': derivholdinglists})

@login_required()
def personholdingtable(request, ticker, owner):
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    latest_form_filed = Form345Entry.objects\
        .filter(issuer_cik=issuer).filter(reporting_owner_cik=owner)\
        .latest('filedatetime')
    person_name = latest_form_filed.reporting_owner_name
    person_title = latest_form_filed.reporting_owner_title
    person_view_set = PersonHoldingView.objects\
        .filter(issuer=issuer).filter(owner=owner)\
        .exclude(units_held=0.0).exclude(units_held=None)
    # These should be reordered by intrinsic economic value, once available
    nonderivativeholdings = person_view_set.filter(deriv_or_nonderiv='N')\
        .order_by('-intrinsic_value', '-units_held')
    derivativeholdings = person_view_set.filter(deriv_or_nonderiv='D')\
        .order_by('-intrinsic_value', '-units_held')

    return render_to_response('sdapp/personholdingtable.html',
                              {'ticker': ticker,
                               'person_name': person_name,
                               'person_title': person_title,
                               'issuer': issuer,
                               'nonderivativeholdings': nonderivativeholdings,
                               'derivativeholdings': derivativeholdings},
                              context_instance=RequestContext(request),
                              )
