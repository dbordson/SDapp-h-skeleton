import datetime
from decimal import Decimal
import sys

import django.db
from django.db.models import F, Q

from sdapp.bin.globals import (buyer, grant_period_calc_lookback,
                               hist_sale_period,
                               min_day_gap_for_10b51_trigger_sell_rate, now,
                               price_trigger_lookback, seller,
                               recent_sale_period, today, todaymid)
from sdapp.bin.sdapptools import (
    median, rep_none_with_zero, get_price, price_decline, price_perf,
    post_sale_perf
)
from sdapp.models import (Affiliation, Form345Entry,
                          IssuerCIK, SecurityPriceHist)


def sale_perf_attributes(issuer, reporting_owner):
    sp_dict = {}
    primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(primary_ticker_sym=True)
    if primary_tickers.exists():
        sph_obj = primary_tickers[0]
    else:
        return
    aff = Affiliation.objects\
        .get(issuer=issuer, reporting_owner=reporting_owner)
    years = [2012, 2013, 2014, 2015]
    test_begin_date = datetime.date(2012, 1, 1)
    month_day_tuples =\
        [[1, 1, 3, 31],
         [4, 1, 6, 30],
         [7, 1, 9, 30],
         [10, 1, 12, 31]]
    regular_sale_forms = \
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(transaction_date__gte=F('filedatetime') +
                datetime.timedelta(-10))\
        .filter(transaction_date__gte=test_begin_date)\
        .exclude(xn_price_per_share=None)\
        .exclude(transaction_shares=None)\
        .filter(transaction_code='S')

    td3mo = datetime.timedelta(91)
    td6mo = datetime.timedelta(182)
    td9mo = datetime.timedelta(275)
    td12mo = datetime.timedelta(365)

    quarters_with_sales_since_beg_2012 = 0
    quarter_count_3_mo_decline = 0
    quarter_count_6_mo_decline = 0
    quarter_count_9_mo_decline = 0
    quarter_count_12_mo_decline = 0
    quarters_with_10b_sales_since_beg_2012 = 0
    quarter_count_3_mo_decline_10b = 0
    quarter_count_6_mo_decline_10b = 0
    quarter_count_9_mo_decline_10b = 0
    quarter_count_12_mo_decline_10b = 0

    for year in years:
        for startmonth, startday, endmonth, endday in month_day_tuples:
            startdate = datetime.date(year, startmonth, startday)
            enddate = datetime.date(year, endmonth, endday)
            period_regular_sales = regular_sale_forms\
                .filter(transaction_date__gte=startdate)\
                .filter(transaction_date__lte=enddate)
            # Regular sales
            # print period_regular_sales
            if period_regular_sales.exists():
                quarters_with_sales_since_beg_2012 += 1

                price_decline_3mo =\
                    price_decline(sph_obj, enddate, td3mo, sp_dict)
                if price_decline_3mo:
                    quarter_count_3_mo_decline += 1

                price_decline_6mo =\
                    price_decline(sph_obj, enddate, td6mo, sp_dict)
                if price_decline_6mo:
                    quarter_count_6_mo_decline += 1

                price_decline_9mo =\
                    price_decline(sph_obj, enddate, td9mo, sp_dict)
                if price_decline_9mo:
                    quarter_count_9_mo_decline += 1

                price_decline_12mo =\
                    price_decline(sph_obj, enddate, td12mo, sp_dict)
                if price_decline_12mo:
                    quarter_count_12_mo_decline += 1
            # 10b5-1 sales
            period_sale_10b_forms =\
                period_regular_sales.exclude(tenbfive_note=None)
            if period_sale_10b_forms.exists():
                quarters_with_10b_sales_since_beg_2012 += 1

                price_decline_3mo =\
                    price_decline(sph_obj, enddate, td3mo, sp_dict)
                if price_decline_3mo:
                    quarter_count_3_mo_decline_10b += 1

                price_decline_6mo =\
                    price_decline(sph_obj, enddate, td6mo, sp_dict)
                if price_decline_6mo:
                    quarter_count_6_mo_decline_10b += 1

                price_decline_9mo =\
                    price_decline(sph_obj, enddate, td9mo, sp_dict)
                if price_decline_9mo:
                    quarter_count_9_mo_decline_10b += 1

                price_decline_12mo =\
                    price_decline(sph_obj, enddate, td12mo, sp_dict)
                if price_decline_12mo:
                    quarter_count_12_mo_decline_10b += 1

    aff.quarters_with_sales_since_beg_2012 =\
        quarters_with_sales_since_beg_2012
    aff.quarter_count_3_mo_decline =\
        quarter_count_3_mo_decline
    aff.quarter_count_6_mo_decline =\
        quarter_count_6_mo_decline
    aff.quarter_count_9_mo_decline =\
        quarter_count_9_mo_decline
    aff.quarter_count_12_mo_decline =\
        quarter_count_12_mo_decline
    aff.quarters_with_10b_sales_since_beg_2012 =\
        quarters_with_10b_sales_since_beg_2012
    aff.quarter_count_3_mo_decline_10b =\
        quarter_count_3_mo_decline_10b
    aff.quarter_count_6_mo_decline_10b =\
        quarter_count_6_mo_decline_10b
    aff.quarter_count_9_mo_decline_10b =\
        quarter_count_9_mo_decline_10b
    aff.quarter_count_12_mo_decline_10b =\
        quarter_count_12_mo_decline_10b

    aff.post_sale_perf_3mo =\
        post_sale_perf(regular_sale_forms, sph_obj, td3mo, sp_dict)
    aff.post_sale_perf_6mo =\
        post_sale_perf(regular_sale_forms, sph_obj, td6mo, sp_dict)
    aff.post_sale_perf_9mo =\
        post_sale_perf(regular_sale_forms, sph_obj, td9mo, sp_dict)
    aff.post_sale_perf_12mo =\
        post_sale_perf(regular_sale_forms, sph_obj, td12mo, sp_dict)
    period_sale_10b_forms =\
        regular_sale_forms.exclude(tenbfive_note=None)
    aff.post_sale_perf_10b_3mo =\
        post_sale_perf(period_sale_10b_forms, sph_obj, td3mo, sp_dict)
    aff.post_sale_perf_10b_6mo =\
        post_sale_perf(period_sale_10b_forms, sph_obj, td6mo, sp_dict)
    aff.post_sale_perf_10b_9mo =\
        post_sale_perf(period_sale_10b_forms, sph_obj, td9mo, sp_dict)
    aff.post_sale_perf_10b_12mo =\
        post_sale_perf(period_sale_10b_forms, sph_obj, td12mo, sp_dict)

    td_since_begin = today - test_begin_date
    cumulativeperformance =\
        price_perf(sph_obj, test_begin_date,
                   td_since_begin, sp_dict)
    years_since_begin = Decimal(td_since_begin.days) / Decimal(365)
    if cumulativeperformance is not None:
        aff.annualized_perf_from_beg_2012_to_today =\
            (cumulativeperformance +
             Decimal(1))**(Decimal(1)/years_since_begin)\
            - Decimal(1)
    aff.save()
    return


def calc_holdings(issuer, reporting_owner, sec_ids, primary_sec_id, datetime,
                  price_dict, ticker_sec_dict):
    date = datetime.date()
    prim_price = get_price(ticker_sec_dict[primary_sec_id],
                           date, price_dict)
    if prim_price is None or prim_price == Decimal(0):
        return None, None, None, None
    holdings = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .exclude(filedatetime__gt=datetime)\
        .exclude(supersededdt__lte=datetime)\
        .exclude(shares_following_xn=None)\
        .values('shares_following_xn', 'adjustment_factor',
                'security__conversion_multiple', 'conversion_price',
                'security', 'underlying_security')
    total_shares_held = Decimal(0)
    total_value = Decimal(0)
    total_conv_cost = Decimal(0)
    for h in holdings:
        # Do we price security directly or underlying?
        if h['security'] in ticker_sec_dict:
            sec_id = h['security']
            underlying_conversion_mult = Decimal(1)
        else:
            sec_id = h['underlying_security']
            underlying_conversion_mult = h['security__conversion_multiple']
        # If pricing secondary security, calculate conversion multiple.
        if sec_id != primary_sec_id:
            holding_price = get_price(ticker_sec_dict[sec_id],
                                      date, price_dict)
            if holding_price is None or prim_price is None or\
                    prim_price == Decimal(0):
                continue
            share_conversion_mult_to_primary_ticker = \
                holding_price / prim_price
        else:
            share_conversion_mult_to_primary_ticker = Decimal(1)
        security_shares = h['shares_following_xn'] * h['adjustment_factor'] *\
            underlying_conversion_mult
        prim_eq_shares = security_shares *\
            share_conversion_mult_to_primary_ticker
        price = get_price(ticker_sec_dict[sec_id], date, price_dict)
        if price is None or price == Decimal(0):
            continue
        adj_conversion_price = rep_none_with_zero(h['conversion_price']) /\
            h['adjustment_factor']
        holding_value = security_shares *\
            max(Decimal(0), price - adj_conversion_price)
        conv_cost = adj_conversion_price * security_shares
        total_shares_held += prim_eq_shares
        total_value += holding_value
        total_conv_cost += conv_cost
    if total_shares_held != Decimal(0):
        avg_conv_price = total_conv_cost / total_shares_held
        conv_to_price_ratio = avg_conv_price / prim_price
    else:
        avg_conv_price = None
        conv_to_price_ratio = None
    return total_shares_held, avg_conv_price, total_value, conv_to_price_ratio


def calc_equity_grants(issuer, reporting_owner, sec_ids, primary_sec_id,
                       price_dict, ticker_sec_dict):
    grants = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .filter(transaction_code='A')\
        .exclude(transaction_shares=None)\
        .exclude(transaction_date=None)\
        .filter(transaction_date__gte=today - grant_period_calc_lookback -
                datetime.timedelta(5))\
        .filter(filedatetime__gte=todaymid - grant_period_calc_lookback)
    grant_dates = \
        list(grants.order_by('transaction_date')
             .values_list('transaction_date', flat=True).distinct())
    # Do not pass go if no grant info available
    if len(grant_dates) == 0:
        return Decimal(0), Decimal(0)
    # If you have only one grant, assume annual because that is typical
    if len(grant_dates) == 1:
        grants_per_year = 1
    # Otherwise, figure out grants per year received based on spacing
    else:
        day_gaps = []
        for first_date, second_date in zip(grant_dates, grant_dates[1:]):
            day_gaps.append(Decimal((second_date - first_date).days))
        median_day_gap = median(day_gaps)
        day_gap_options = [Decimal(30), Decimal(45), Decimal(60),
                           Decimal(91), Decimal(182), Decimal(365)]
        estimated_day_gap = min(day_gap_options,
                                key=lambda x: abs(x-median_day_gap))
        grants_per_year = int(round(Decimal(365) / estimated_day_gap, 0))
    # now calc grant amounts in last year and use total to annualize
    grant_dates.reverse()
    last_year_dates = grant_dates[:grants_per_year]
    grants_amounts = grants\
        .filter(transaction_date__in=last_year_dates)\
        .values('transaction_shares', 'adjustment_factor',
                'security__conversion_multiple', 'conversion_price',
                'security', 'underlying_security', 'transaction_date')
    # If no grants in last year, stop here.
    if grants_amounts.count() == 0:
        return Decimal(0), Decimal(0)
    # Otherwise calculate total grants
    annual_grant_shares = Decimal(0)
    total_conv_cost = Decimal(0)
    for g in grants_amounts:
        # Do we price security directly or underlying?
        if g['security'] in ticker_sec_dict:
            sec_id = g['security']
            underlying_conversion_mult = Decimal(1)
        else:
            sec_id = g['underlying_security']
            underlying_conversion_mult = g['security__conversion_multiple']
        # If pricing secondary security, calculate conversion multiple.
        if sec_id != primary_sec_id:
            grant_sec_price = get_price(ticker_sec_dict[sec_id],
                                        g['transaction_date'], price_dict)
            prim_price = get_price(ticker_sec_dict[primary_sec_id],
                                   g['transaction_date'], price_dict)
            if grant_sec_price is None or prim_price is None or\
                    prim_price == Decimal(0):
                continue
            share_conversion_mult_to_primary_ticker = \
                grant_sec_price / prim_price
        else:
            share_conversion_mult_to_primary_ticker = Decimal(1)
        security_shares = g['transaction_shares'] * g['adjustment_factor'] *\
            underlying_conversion_mult
        prim_eq_shares = security_shares *\
            share_conversion_mult_to_primary_ticker

        adj_conversion_price = rep_none_with_zero(g['conversion_price']) /\
            g['adjustment_factor']
        conv_cost = adj_conversion_price * security_shares
        annual_grant_shares += prim_eq_shares
        total_conv_cost += conv_cost

    if annual_grant_shares != Decimal(0):
        avg_conv_price = total_conv_cost / annual_grant_shares
    else:
        avg_conv_price = None

    return annual_grant_shares, avg_conv_price


def calc_disc_xns(issuer, reporting_owner, sec_ids, primary_sec_id,
                  price_dict, ticker_sec_dict, startdate, enddate,
                  only_10b5_1):
    disc_xns = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .filter(Q(transaction_code='P') | Q(transaction_code='S'))\
        .filter(transaction_date__gte=startdate)\
        .filter(transaction_date__lte=enddate)\
        .exclude(transaction_shares=None)
    if only_10b5_1 is True:
        disc_xns = disc_xns.filter(tenbfive_note=True)
    disc_xns = disc_xns\
        .values('transaction_shares', 'adjustment_factor',
                'security__conversion_multiple', 'security',
                'underlying_security', 'transaction_date', 'transaction_code',)
    if len(disc_xns) is 0:
        return Decimal(0), Decimal(0)
    net_xn_shares = Decimal(0)
    net_xn_value = Decimal(0)
    xn_sign = {'S': Decimal(-1), 'P': Decimal(1)}
    for x in disc_xns:
        # Do we price security directly or underlying?
        if x['security'] in ticker_sec_dict:
            sec_id = x['security']
            underlying_conversion_mult = Decimal(1)
        else:
            sec_id = x['underlying_security']
            underlying_conversion_mult = x['security__conversion_multiple']
        # If pricing secondary security, calculate conversion multiple.
        if sec_id != primary_sec_id and\
                x['underlying_security'] != primary_sec_id:
            sec_price = get_price(ticker_sec_dict[sec_id],
                                  x['transaction_date'], price_dict)
            prim_price = get_price(ticker_sec_dict[primary_sec_id],
                                   x['transaction_date'], price_dict)
            if sec_price is None or prim_price is None or\
                    prim_price == Decimal(0):
                continue
            share_conversion_mult_to_primary_ticker = \
                sec_price / prim_price
        else:
            share_conversion_mult_to_primary_ticker = Decimal(1)
        price = get_price(ticker_sec_dict[sec_id],
                          x['transaction_date'], price_dict)
        if price is None:
            continue
        prim_eq_shares = x['transaction_shares'] * x['adjustment_factor'] *\
            underlying_conversion_mult *\
            xn_sign[x['transaction_code']] *\
            share_conversion_mult_to_primary_ticker
        net_xn_shares += prim_eq_shares
        net_xn_value += prim_eq_shares * price
    return net_xn_shares, net_xn_value


def hist_10b5_1_sales_per_year(
        issuer, reporting_owner, sec_ids,
        primary_sec_id, price_dict, ticker_sec_dict,
        startdate, enddate
):
    sales = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .filter(transaction_code='S')\
        .exclude(transaction_shares=None)\
        .filter(transaction_date__gte=startdate)\
        .filter(transaction_date__lte=enddate)\
        .filter(tenbfive_note=True)
    sale_dates = \
        list(sales.order_by('transaction_date')
             .values_list('transaction_date', flat=True).distinct())
    # Do not pass go if no grant info available
    if len(sale_dates) == 0:
        sales_per_year = 0
    # If you have only one grant, assume annual because that is typical
    elif len(sale_dates) == 1:
        sales_per_year = 1
    # Otherwise, figure out grants per year received based on spacing
    else:
        day_gaps = []
        for first_date, second_date in zip(sale_dates, sale_dates[1:]):
            gap = Decimal((second_date - first_date).days)
            if gap > min_day_gap_for_10b51_trigger_sell_rate:
                day_gaps.append(gap)
        if len(day_gaps) == 0:
            return None
        median_day_gap = median(day_gaps)
        day_gap_options = [Decimal(30), Decimal(45), Decimal(60),
                           Decimal(91), Decimal(182), Decimal(365)]
        estimated_day_gap = min(day_gap_options,
                                key=lambda x: abs(x-median_day_gap))
        sales_per_year = int(round(Decimal(365) / estimated_day_gap, 0))
    return sales_per_year


def recent_10b5_1_dates_prices(issuer, reporting_owner, sec_ids,
                               primary_sec_id, price_dict, ticker_sec_dict,
                               startdate, enddate):
    sales = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .filter(transaction_code='S')\
        .exclude(transaction_shares=None)\
        .filter(transaction_date__gte=startdate)\
        .filter(transaction_date__lte=enddate)\
        .filter(tenbfive_note=True)
    sale_dates = \
        list(sales.order_by('transaction_date')
             .values_list('transaction_date', flat=True).distinct())
    # Do not pass go if no grant info available
    if len(sale_dates) == 0:
        transaction_date_price_info = [(None, None)]
    # If you have only one grant, assume annual because that is typical
    elif len(sale_dates) == 1:
        date = sale_dates[0]
        transaction_date_price_info =\
            [(date,
              get_price(ticker_sec_dict[primary_sec_id],
                        date, price_dict))]
    # Otherwise, figure out grants per year received based on spacing
    else:
        transaction_date_price_info = []
        for first_date, second_date in zip(sale_dates, sale_dates[1:]):
            gap = Decimal((second_date - first_date).days)
            if gap > min_day_gap_for_10b51_trigger_sell_rate:
                date = first_date
                price = get_price(ticker_sec_dict[primary_sec_id],
                                  date, price_dict)
                transaction_date_price_info.append((date, price))
        last_date = sale_dates[-1]
        last_price = get_price(ticker_sec_dict[primary_sec_id],
                               last_date, price_dict)
        transaction_date_price_info.append((last_date, last_price))

    return transaction_date_price_info


def calc_person_affiliation(issuer, reporting_owner, price_dict):
    affiliation_forms = Form345Entry.objects.filter(issuer_cik=issuer)\
            .filter(reporting_owner_cik=reporting_owner)
    latest_form = affiliation_forms.latest('filedatetime')
    aff =\
        Affiliation.objects.get(issuer=issuer,
                                reporting_owner=reporting_owner)
    # General info
    aff.issuer_name = IssuerCIK.objects.get(cik_num=issuer).name
    aff.person_name = latest_form.reporting_owner_name
    aff.is_director = latest_form.is_director
    aff.is_officer = latest_form.is_officer
    aff.is_ten_percent = latest_form.is_ten_percent
    aff.is_something_else = latest_form.is_something_else
    aff.reporting_owner_title = latest_form.reporting_owner_title
    aff.latest_form_dt = latest_form.filedatetime
    first_form = affiliation_forms.earliest('filedatetime')
    aff.first_form_dt = first_form.filedatetime
    aff.is_active = True
    ticker_list = SecurityPriceHist.objects.filter(issuer=issuer)\
        .exclude(security=None).values_list('security', 'pk')
    ticker_sec_dict = dict(ticker_list)
    primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(primary_ticker_sym=True)
    # If no primary ticker, the numerical analysis is meaningless
    # This will catch errors if the script is run before db populated
    # of if a company's ticker wasn't linked. Should otherwise not happen.
    if primary_tickers.count() == 0:
        aff.save()
        return
    prim_ticker = primary_tickers[0]
    prim_security = prim_ticker.security
    all_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .exclude(security=None)
    ticker_sec_ids = all_tickers.values_list('security', flat=True)

    # Populate current and prior shares, conv price, value, conv price ratio
    aff.share_equivalents_held, aff.average_conversion_price,\
        aff.share_equivalents_value, aff.conversion_to_price_ratio =\
        calc_holdings(issuer, reporting_owner, ticker_sec_ids,
                      prim_security.pk, todaymid, price_dict, ticker_sec_dict)

    prior_datetime = todaymid - recent_sale_period
    aff.prior_share_equivalents_held, aff.prior_average_conversion_price,\
        aff.prior_share_equivalents_value,\
        aff.prior_conversion_to_price_ratio =\
        calc_holdings(issuer, reporting_owner, ticker_sec_ids,
                      prim_security.pk, prior_datetime, price_dict,
                      ticker_sec_dict)

    # Populate grant rate info
    aff.equity_grant_rate, aff.avg_grant_conv_price =\
        calc_equity_grants(issuer, reporting_owner, ticker_sec_ids,
                           prim_security.pk, price_dict, ticker_sec_dict)
    # Recent / hist sale data
    recent_period_start = today - recent_sale_period
    hist_period_start = today - hist_sale_period

    number_of_recent_shares_sold, value_of_recent_shares_sold =\
        calc_disc_xns(issuer, reporting_owner, ticker_sec_ids,
                      prim_security.pk, price_dict, ticker_sec_dict,
                      recent_period_start,
                      today, False)
    aff.number_of_recent_shares_sold, aff.value_of_recent_shares_sold =\
        number_of_recent_shares_sold, value_of_recent_shares_sold

    historical_selling_rate_shares, historical_selling_rate_value =\
        calc_disc_xns(issuer, reporting_owner, ticker_sec_ids,
                      prim_security.pk, price_dict, ticker_sec_dict,
                      hist_period_start,
                      recent_period_start, False)
    aff.historical_selling_rate_shares, aff.historical_selling_rate_value =\
        historical_selling_rate_shares, historical_selling_rate_value

    recent_share_sell_rate_for_10b5_1_plans, recent_10b5_1_xn_value =\
        calc_disc_xns(issuer, reporting_owner, ticker_sec_ids,
                      prim_security.pk, price_dict, ticker_sec_dict,
                      recent_period_start,
                      today, True)
    aff.recent_share_sell_rate_for_10b5_1_plans =\
        recent_share_sell_rate_for_10b5_1_plans

    historical_share_sell_rate_for_10b5_1_plans, hist_10b5_1_xn_value =\
        calc_disc_xns(issuer, reporting_owner, ticker_sec_ids,
                      prim_security.pk, price_dict, ticker_sec_dict,
                      hist_period_start,
                      recent_period_start, True)
    aff.historical_share_sell_rate_for_10b5_1_plans =\
        historical_share_sell_rate_for_10b5_1_plans

    if number_of_recent_shares_sold < Decimal(0) and\
            historical_selling_rate_shares < Decimal(0):

        len_hist_over_len_recent =\
            (recent_period_start - hist_period_start).days /\
            (today - recent_period_start).days

        aff.percent_change_in_shares_hist_to_recent =\
            (number_of_recent_shares_sold * len_hist_over_len_recent) /\
            historical_selling_rate_shares - 1

        aff.percent_change_in_value_hist_to_recent =\
            (number_of_recent_shares_sold * len_hist_over_len_recent) /\
            historical_selling_rate_shares - 1

        aff.percent_recent_shares_sold_under_10b5_1_plans =\
            recent_share_sell_rate_for_10b5_1_plans /\
            number_of_recent_shares_sold

    # Detect 10b5-1 rises

    clusters_in_hist_period =\
        hist_10b5_1_sales_per_year(issuer, reporting_owner, ticker_sec_ids,
                                   prim_security.pk, price_dict,
                                   ticker_sec_dict, hist_period_start,
                                   recent_period_start)
    transaction_date_price_info = \
        recent_10b5_1_dates_prices(issuer, reporting_owner, ticker_sec_ids,
                                   prim_security.pk, price_dict,
                                   ticker_sec_dict, recent_period_start, today)
    if recent_share_sell_rate_for_10b5_1_plans < Decimal(0) and\
            historical_share_sell_rate_for_10b5_1_plans < Decimal(0) and\
            clusters_in_hist_period is not None:
        recent = recent_share_sell_rate_for_10b5_1_plans
        hist = historical_share_sell_rate_for_10b5_1_plans
        len_hist_over_len_recent =\
            (recent_period_start - hist_period_start).days /\
            (today - recent_period_start).days
        # Note that the signs are flipped below because we are looking
        # for the most negative quantities.
        if hist is not None and clusters_in_hist_period is not None and\
                clusters_in_hist_period is not 0 and\
                recent < min(hist / len_hist_over_len_recent,
                             hist / clusters_in_hist_period) and\
                len(transaction_date_price_info) != 0:
            increase_in_10b5_1 = True
            aff.increase_in_10b5_1_selling = increase_in_10b5_1
            aff.expected_recent_10b5_1_sale_amount =\
                min(hist / len_hist_over_len_recent,
                    hist / clusters_in_hist_period)
            trigger_detected = False
            for date, price in transaction_date_price_info:
                trigger_10b5_1_price_perf =\
                    price_perf(ticker_sec_dict[prim_security.pk],
                               date - price_trigger_lookback,
                               price_trigger_lookback, price_dict)
                # recent_10b5_1_price_perf =\
                #     price_perf(prim_security.pk,
                #                date - recent_sale_period,
                #                -recent_sale_period, price_dict)
                if increase_in_10b5_1 is True and\
                        trigger_10b5_1_price_perf > Decimal(0):
                    aff.price_trigger_detected = True
                    trigger_detected = False
                    aff.selling_price = price
                    aff.selling_date = date
                    aff.selling_prior_performance = trigger_10b5_1_price_perf
                    aff.selling_subs_performance =\
                        price_perf(prim_security.pk,
                                   date,
                                   today - date, price_dict)
                if increase_in_10b5_1 is True and\
                        trigger_detected is False:
                    aff.selling_price = price
                    aff.selling_date = date
                    aff.selling_prior_performance = trigger_10b5_1_price_perf
                    aff.selling_subs_performance =\
                        price_perf(prim_security.pk,
                                   date,
                                   today - date, price_dict)

    # Placeholder behavior calculation
    if number_of_recent_shares_sold > Decimal(0):
        behavior = buyer
    elif number_of_recent_shares_sold == Decimal(0):
        behavior = None
    elif aff.equity_grant_rate is not None\
            and Decimal(-1) * number_of_recent_shares_sold\
            <= aff.equity_grant_rate:
        behavior = None
    else:
        behavior = seller
    aff.behavior = behavior

    if aff.prior_share_equivalents_held >= 1000000000000\
            or aff.share_equivalents_held >= 1000000000000:
        print issuer, reporting_owner, aff.person_name
        print 'prior_share_equivalents_held',
        print aff.prior_share_equivalents_held
        print 'share_equivalents_held',
        print aff.share_equivalents_held
        print 'a number is too big'
        aff.prior_share_equivalents_held = 0
        aff.share_equivalents_held = 0

    aff.save()
    return


def upd():
    affiliations_with_new_forms = Affiliation.objects.all()\
        .values_list('issuer', 'reporting_owner')
    counter = 0.0
    looplength = float(len(affiliations_with_new_forms))
    price_dict = {}
    for issuer, reporting_owner in affiliations_with_new_forms:
        calc_person_affiliation(issuer, reporting_owner, price_dict)
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s affiliation to update: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()

    print '\n   ...determining who is active...'
    general_include_date = now - datetime.timedelta(3 * 365)
    no_shares_include_date = now - datetime.timedelta(365)
    officer_include_date = now - datetime.timedelta(400)
    # If officer and not 10%, use officer date.
    Affiliation.objects.filter(is_active=True)\
        .filter(is_officer=True).exclude(is_ten_percent=True)\
        .filter(latest_form_dt__lte=officer_include_date)\
        .update(is_active=False)
    # If officer and 10%, use gen include date (big owners may not
    # get annual stock grants, so give more time between transactions)
    Affiliation.objects.filter(is_active=True)\
        .filter(is_officer=True).filter(is_ten_percent=True)\
        .filter(latest_form_dt__lte=general_include_date)\
        .update(is_active=False)
    # If not an officer and have shares, just get general date
    Affiliation.objects.filter(is_active=True)\
        .filter(~Q(is_officer=True))\
        .filter(share_equivalents_held__gt=Decimal(0))\
        .filter(latest_form_dt__lte=general_include_date)\
        .update(is_active=False)
    # If not an officer and have no shares, get less time
    Affiliation.objects.filter(is_active=True)\
        .filter(~Q(is_officer=True))\
        .exclude(share_equivalents_held__gt=Decimal(0))\
        .filter(latest_form_dt__lte=no_shares_include_date)\
        .update(is_active=False)
    print '   ...active status updated.'
    return


def annotatestats():
    affiliations = Affiliation.objects.all()\
        .values_list('issuer', 'reporting_owner')
    affiliations.update(
        quarters_with_sales_since_beg_2012=None,
        quarter_count_3_mo_decline=None,
        quarter_count_6_mo_decline=None,
        quarter_count_9_mo_decline=None,
        quarter_count_12_mo_decline=None,
        post_sale_perf_3mo=None,
        post_sale_perf_6mo=None,
        post_sale_perf_9mo=None,
        post_sale_perf_12mo=None,
        quarters_with_10b_sales_since_beg_2012=None,
        quarter_count_3_mo_decline_10b=None,
        quarter_count_6_mo_decline_10b=None,
        quarter_count_9_mo_decline_10b=None,
        quarter_count_12_mo_decline_10b=None,
        post_sale_perf_10b_3mo=None,
        post_sale_perf_10b_6mo=None,
        post_sale_perf_10b_9mo=None,
        post_sale_perf_10b_12mo=None,
        annualized_perf_from_beg_2012_to_today=None,
    )
    counter = 0.0
    looplength = float(len(affiliations))
    for issuer, reporting_owner in affiliations:
        top_holders = Affiliation.objects.filter(issuer=issuer)\
            .order_by('-share_equivalents_value')\
            .values_list('reporting_owner', flat=True)
        top_3_holders = list(top_holders)[:3]
        if reporting_owner in top_3_holders:
            sale_perf_attributes(issuer, reporting_owner)
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s affiliations to update: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
        django.db.reset_queries()
    return
