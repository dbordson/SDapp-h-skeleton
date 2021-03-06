import datetime
from decimal import Decimal
import sys

from sdapp.models import SecurityPriceHist, ClosePrice, Form345Entry
from sdapp.models import ReportingPersonAtts

from django.db.models import Q
import django.db

days_over_which_a_trade_is_evaluated = 180
trade_delta = datetime.timedelta(days_over_which_a_trade_is_evaluated)
win_hurdle = .10


def irrelevant():
    relevant = False
    success = False
    xn_perf = None
    return relevant, success, xn_perf, None, None, None, None, None, None


def laxer_start_price(sec_price_hist, date):
    wkd_td = datetime.timedelta(5)
    close_prices = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)
    price_list = \
        close_prices.filter(close_date__lte=date+wkd_td)\
        .filter(close_date__gte=date + datetime.timedelta(1))\
        .order_by('close_date')
    if price_list.exists():
        return price_list[0].adj_close_price
    else:
        return None


def get_start(sec_price_hist, date):
    close_price = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)\
        .filter(close_date=date + datetime.timedelta(1))
    if close_price.exists():
        return close_price[0].adj_close_price
    else:
        return laxer_start_price(sec_price_hist, date)


# Note that the date calculations are intentionally conservative measures
# of returns; start date is no LESS than filingdatetime + 1 and ending date
# is no MORE than filingdatetime + 1.  E.g. If you test over 7 days, you
# get the advantage of an avg effective period of over 7 days because you'll
# regularly have to grab the close price on Monday if t + 7 falls on a
# saturday.

def laxer_end_price(sec_price_hist, date):
    wkd_td = datetime.timedelta(5)
    close_prices = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)
    price_list = \
        close_prices.filter(close_date__lte=date + datetime.timedelta(1))\
        .filter(close_date__gte=date - wkd_td + datetime.timedelta(2))\
        .order_by('-close_date')
    if price_list.exists():
        return price_list[0].adj_close_price
    else:
        return None


def get_end(sec_price_hist, date):
    close_price = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)\
        .filter(close_date=date + datetime.timedelta(1))
    if close_price.exists():
        return close_price[0].adj_close_price
    else:
        return laxer_end_price(sec_price_hist, date)

# NOT USED, BUT MAY BE USEFUL
# def issuerdailyperf(sec_price_hist, repperson):
#     # Tries to calculate return over the period that the holder has
#     # transacted in company stock.  Returns None if pricing unavailable
#     # or less than a year of history.
#     issuer = sec_price_hist.issuer
#     entry_dates = \
#         list(Form345Entry.objects
#              .filter(issuer_cik=issuer, reporting_owner_cik=repperson)
#              .order_by('filedatetime')
#              .values_list('filedatetime', flat=True).distinct())
#     first_date = entry_dates[0].date()
#     last_date = entry_dates[-1].date()
#     days = Decimal(((last_date - first_date).days))
#     if days < 365.25:
#         return None
#     first_price = get_price(sec_price_hist, first_date)
#     last_price = get_price(sec_price_hist, last_date)
#     if first_price is None or last_price is None:
#         return None
#     daily_return = ((last_price - first_price) / first_price) / days

#     return daily_return


def xnanalyze(repperson, filedate, acq_or_disp, issuer, trade_delta,
              win_hurdle):
    sec_price_hist_qs = SecurityPriceHist.objects.filter(issuer=issuer)
    # First figure out if the necessary information (ticker sym, necessary
    # price history exist)
    if sec_price_hist_qs.exists():
        sec_price_hist = sec_price_hist_qs[0]
    else:
        return irrelevant()
    # print 'repperson:', repperson,
    start_price = get_start(sec_price_hist, filedate)
    price_10 = get_end(sec_price_hist, filedate + datetime.timedelta(10))
    price_30 = get_end(sec_price_hist, filedate + datetime.timedelta(30))
    price_60 = get_end(sec_price_hist, filedate + datetime.timedelta(60))
    price_90 = get_end(sec_price_hist, filedate + datetime.timedelta(90))
    price_120 = get_end(sec_price_hist, filedate + datetime.timedelta(120))
    price_150 = get_end(sec_price_hist, filedate + datetime.timedelta(150))
    enddate = filedate + trade_delta
    end_price = get_end(sec_price_hist, enddate)
    if start_price is None or end_price is None:
        # print 'no start price'
        return irrelevant()
    # Note the below day calculation may not be perfect for all scenarios
    # because in some cases, a transaction may somehow happen on a day for
    # which we don't have a closing price.  We should generally be okay,
    # though.
    if start_price == 0:
        # print 'start price is zero'
        return irrelevant()
    perf_10 = ((price_10 - start_price) / start_price)
    perf_30 = ((price_30 - start_price) / start_price)
    perf_60 = ((price_60 - start_price) / start_price)
    perf_90 = ((price_90 - start_price) / start_price)
    perf_120 = ((price_120 - start_price) / start_price)
    perf_150 = ((price_150 - start_price) / start_price)

    xn_perf = ((end_price - start_price) / start_price)
    # issuer_daily_perf = issuerdailyperf(sec_price_hist, repperson)
    # if issuer_daily_perf is None:
    # print 'no issuer daily perf'
    # return irrelevant()

    relevant = True
    # print 'went up'
    # print 'went down'
    success = False
    if acq_or_disp == 'A' and xn_perf >= win_hurdle:
        success = True
    if acq_or_disp == 'D' and xn_perf <= -win_hurdle:
        success = True

    return (relevant, success, xn_perf, perf_10, perf_30, perf_60, perf_90,
            perf_120, perf_150)

# Remember to analyze the population of executives who are good traders
# against what population would be good traders by virtue of throwing
# darts.


def execanalyze(repperson, trade_delta, win_hurdle):
    execentries =\
        Form345Entry.objects\
        .filter(reporting_owner_cik=repperson)\
        .filter(is_officer=True)\
        .exclude(transaction_date=None)\
        .exclude(xn_acq_disp_code=None)\
        .filter(Q(transaction_code='P') |  # Open mkt / private purch
                Q(transaction_code='S') |  # Open mkt / private sale
                Q(transaction_code='I'))  # Discretionary 16b-3 Xn
    xns = 0
    buys = 0
    sells = 0
    good_xns = 0
    good_buys = 0
    good_sells = 0
    # Below can be changed freely to change whether the activity_threshold
    # is met.
    necessary_xns = 8
    necessary_buys = 2
    necessary_sales = 2

    # entrydates =\
    #     list(Form345Entry.objects
    #          .filter(reporting_owner_cik=repperson)
    #          .exclude(is_officer=False)
    #          .order_by('filedatetime')
    #          .values_list('filedatetime', flat=True).distinct())
    exec_start =\
        Form345Entry.objects.filter(reporting_owner_cik=repperson)\
        .exclude(is_officer=False).earliest('filedatetime').filedatetime
    # entrydates[0]

    exec_end =\
        Form345Entry.objects.filter(reporting_owner_cik=repperson)\
        .exclude(is_officer=False).latest('filedatetime').filedatetime
    # entrydates[-1]
    # Note that exec years is years as an SEC reporting exec
    exec_years = Decimal((exec_end - exec_start).days) / Decimal(365.25)
    gross_t_perf = Decimal(0)
    gross_b_perf = Decimal(0)
    gross_s_perf = Decimal(0)
    gross_b_perf_10 = Decimal(0)
    gross_b_perf_30 = Decimal(0)
    gross_b_perf_60 = Decimal(0)
    gross_b_perf_90 = Decimal(0)
    gross_b_perf_120 = Decimal(0)
    gross_b_perf_150 = Decimal(0)
    # exexentrydates = execentries.datetimes('filedatetime', 'day').distinct()
    distinct_date_entries =\
        execentries.order_by('filedatetime', 'transaction_number')\
        .distinct('filedatetime')
    # for exexentrydate in exexentrydates:
    for firstentry in distinct_date_entries:
        # firstentry = \
        #     Form345Entry.objects\
        #     .filter(reporting_owner_cik=repperson)\
        #     .filter(is_officer=True)\
        #     .exclude(transaction_date=None)\
        #     .exclude(xn_acq_disp_code=None)\
        #     .filter(filedatetime__year=exexentrydate.year,
        #             filedatetime__month=exexentrydate.month,
        #             filedatetime__day=exexentrydate.day)\
        #     .filter(Q(transaction_code='P') |
        #             Q(transaction_code='S') |
        #             Q(transaction_code='I'))\
        #     .order_by('transaction_number')[0]
        filedate = firstentry.filedatetime.date()
        acq_or_disp = firstentry.xn_acq_disp_code
        issuer = firstentry.issuer_cik_num
        # Add weighting by units / value?
        (relevant, success, xn_perf, perf_10, perf_30, perf_60, perf_90,
            perf_120, perf_150) = xnanalyze(repperson, filedate, acq_or_disp,
                                            issuer, trade_delta, win_hurdle)
        if relevant:
            if acq_or_disp == 'A':
                xns += 1
                buys += 1
                if success:
                    good_xns += 1
                    good_buys += 1
                gross_t_perf += xn_perf
                gross_b_perf += xn_perf
                gross_b_perf_10 += perf_10
                gross_b_perf_30 += perf_30
                gross_b_perf_60 += perf_60
                gross_b_perf_90 += perf_90
                gross_b_perf_120 += perf_120
                gross_b_perf_150 += perf_150

            if acq_or_disp == 'D':
                xns += 1
                sells += 1
                gross_t_perf += -1 * xn_perf
                gross_s_perf += -1 * xn_perf
                if success:
                    good_xns += 1
                    good_sells += 1
    if xns == 0:
        t_win_rate = None
        t_perf = None
        return
    else:
        t_win_rate = Decimal(good_xns) / Decimal(xns)
        t_perf = gross_t_perf / Decimal(xns)

    if buys == 0:
        b_win_rate = None
        b_perf = None
        b_perf_10 = None
        b_perf_30 = None
        b_perf_60 = None
        b_perf_90 = None
        b_perf_120 = None
        b_perf_150 = None
    else:
        b_win_rate = Decimal(good_buys) / Decimal(buys)
        b_perf = gross_b_perf / Decimal(buys)
        b_perf_10 = gross_b_perf_10 / Decimal(buys)
        b_perf_30 = gross_b_perf_30 / Decimal(buys)
        b_perf_60 = gross_b_perf_60 / Decimal(buys)
        b_perf_90 = gross_b_perf_90 / Decimal(buys)
        b_perf_120 = gross_b_perf_120 / Decimal(buys)
        b_perf_150 = gross_b_perf_150 / Decimal(buys)

    if sells == 0:
        s_win_rate = None
        s_perf = None
    else:
        s_win_rate = Decimal(good_sells) / Decimal(sells)
        s_perf = gross_s_perf / Decimal(sells)

    if xns >= necessary_xns and buys >= necessary_buys\
            and sells >= necessary_sales:
        activity_threshold = True
    else:
        activity_threshold = False

    rpatts_object =\
        ReportingPersonAtts(reporting_person_id=repperson,
                            transactions=xns,
                            buys=buys,
                            sells=sells,
                            activity_threshold=activity_threshold,
                            t_win_rate=t_win_rate,
                            b_win_rate=b_win_rate,
                            s_win_rate=s_win_rate,
                            exec_years=exec_years,
                            t_perf=t_perf,
                            b_perf=b_perf,
                            s_perf=s_perf,
                            b_perf_10=b_perf_10,
                            b_perf_30=b_perf_30,
                            b_perf_60=b_perf_60,
                            b_perf_90=b_perf_90,
                            b_perf_120=b_perf_120,
                            b_perf_150=b_perf_150).save()
    django.db.reset_queries()
    return
    # return rpatts_object


def reviewreppersons(trade_delta):
    ReportingPersonAtts.objects.all().delete()
    print "Building ReportingPersonAtts table..."
    '    Sorting, analyzing and saving...'
    reppersonobjects =\
        Form345Entry.objects\
        .filter(is_officer=True)\
        .exclude(transaction_date=None)\
        .exclude(xn_acq_disp_code=None)\
        .filter(Q(transaction_code='P') |  # Open mkt / private purch
                Q(transaction_code='S') |  # Open mkt / private sale
                Q(transaction_code='I'))  # Discretionary 16b-3 Xn
    reppersons =\
        reppersonobjects\
        .values_list('reporting_owner_cik', flat=True).distinct()
    print '    Number of potential reporting persons:', len(reppersons)
    looplength = float(len(reppersons))
    count = 0.0
    # rpatts_objects = []
    for repperson in reppersons:
        count += 1.0
        percentcomplete = round(count / looplength * 100, 2)
        sys.stdout.write("\r%s / %s reporting persons: %.2f%%" %
                         (int(count), int(looplength),
                          percentcomplete))
        sys.stdout.flush()
        # rpatts_object = \
        execanalyze(repperson, trade_delta, win_hurdle)
        # if rpatts_object is not None:
        #    rpatts_objects.append(rpatts_object)
    # ReportingPersonAtts.objects.bulk_create(rpatts_objects)
    # django.db.reset_queries()
    print 'Done'
    return

reviewreppersons(trade_delta)
