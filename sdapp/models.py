from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
# class StockHistories(models.Model):


class ReportingPerson(models.Model):
    person_name = models.CharField(max_length=80)
    reporting_owner_cik_num = models.IntegerField(primary_key=True)

    def __unicode__(self):
        return self.person_name


class IssuerCIK(models.Model):
    cik_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80, null=True)
    # current_ceo = models.ForeignKey(ReportingPerson, null=True)
    # Adapt this for companies with more than one public stock (GOOG)
    # to do this, we will need to update the ticker finder script

    def __unicode__(self):
        return str(self.cik_num)


class Affiliation(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    reporting_owner = models.ForeignKey(ReportingPerson)

    person_name = models.CharField(max_length=80, null=True)
    is_director = models.NullBooleanField(null=True)
    is_officer = models.NullBooleanField(null=True)
    is_ten_percent = models.NullBooleanField(null=True)
    is_something_else = models.NullBooleanField(null=True)
    reporting_owner_title = models.CharField(max_length=80, null=True)

    share_equivalents_held =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    average_conversion_price =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    equity_grant_rate =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)

    share_equivalents_value =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    conversion_to_price_ratio =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    equity_grant_value =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)

    share_equivalents_value_percentile = \
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    average_conversion_price_ratio_percentile = \
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    equity_grant_value_percentile = \
        models.DecimalField(max_digits=15, decimal_places=2, null=True)

    latest_form_dt = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.person_name) or u''


class Security(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    short_sec_title = models.CharField(max_length=80, null=True)
    ticker = models.CharField(max_length=10, null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    scrubbed_underlying_title = models.CharField(max_length=80, null=True)
    conversion_multiple = models.DecimalField(max_digits=15, decimal_places=4,
                                              default=Decimal('1.00'))

    def __unicode__(self):
        return unicode(self.short_sec_title) or u''


class SecurityPriceHist(models.Model):
    ticker_sym = models.CharField(max_length=10)
    primary_ticker_sym = models.BooleanField(default=True)

    issuer = models.ForeignKey(IssuerCIK, null=True)
    security = models.ForeignKey(Security, null=True)

    def __unicode__(self):
        return u"%s, %s" % (str(self.ticker_sym),
                            str(self.issuer.name))


class ClosePrice(models.Model):
    close_price = models.DecimalField(max_digits=12, decimal_places=4)
    adj_close_price = models.DecimalField(max_digits=12, decimal_places=4)
    close_date = models.DateField()
    securitypricehist = models.ForeignKey(SecurityPriceHist, null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (str(self.securitypricehist),
                                str(self.close_price),
                                str(self.close_date))


class SplitOrAdjustmentEvent(models.Model):
    security = models.ForeignKey(Security)
    adjustment_factor = models.DecimalField(max_digits=15, decimal_places=4)
    event_date = models.DateField(null=True)

    def __unicode__(self):
        return unicode(self.security) or u''


class TransactionEvent(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    net_xn_val = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    end_holding_val = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    net_xn_pct = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    period_start = models.DateField(null=True)
    period_end = models.DateField(null=True)
    price_at_period_end = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    perf_at_91_days = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    perf_at_182_days = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    perf_at_274_days = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    perf_at_365_days = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    perf_at_456_days = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (str(self.issuer),
                                str(self.period_start),
                                str(self.period_end))


class WatchedName(models.Model):
    user = models.ForeignKey(User)
    issuer = models.ForeignKey(IssuerCIK)
    securitypricehist = models.ForeignKey(SecurityPriceHist)
    ticker_sym = models.CharField(max_length=10)
    last_signal_sent = models.DateField(null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (str(self.user),
                                str(self.issuer),
                                str(self.ticker_sym),
                                )


class ReportingPersonAtts(models.Model):
    reporting_person = models.ForeignKey(ReportingPerson)
    transactions = models.IntegerField()
    buys = models.IntegerField()
    sells = models.IntegerField()
    activity_threshold = models.BooleanField()
    t_win_rate = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    b_win_rate = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    s_win_rate = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    exec_years = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    t_perf = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    s_perf = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_10 = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_30 = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_60 = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_90 = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_120 = \
        models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_150 = \
        models.DecimalField(max_digits=10, decimal_places=4, null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (str(self.reporting_person),
                                str(self.transactions),
                                str(self.activity_threshold))


class YearlyReportingPersonAtts(models.Model):
    reporting_person = models.ForeignKey(ReportingPerson)
    year = models.IntegerField()
    buys = models.IntegerField()
    b_win_rate_180 = models.DecimalField(max_digits=7, decimal_places=4,
                                         null=True)
    exec_years = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    b_perf_10 = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_30 = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_60 = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_90 = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_120 = \
        models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_150 = \
        models.DecimalField(max_digits=10, decimal_places=4, null=True)
    b_perf_180 = \
        models.DecimalField(max_digits=10, decimal_places=4, null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (str(self.reporting_person),
                                str(self.transactions),
                                str(self.activity_threshold))


class SecurityView(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    security = models.ForeignKey(Security)
    short_sec_title = models.CharField(max_length=80, null=True)
    ticker = models.CharField(max_length=10, null=True)
    last_close_price = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    # security_title = models.CharField(max_length=80, null=True)
    units_held = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    first_expiration_date = models.DateField(null=True)
    last_expiration_date = models.DateField(null=True)
    wavg_expiration_date = models.DateField(null=True)
    min_conversion_price = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    max_conversion_price = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    wavg_conversion = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    # underlying_title = models.CharField(max_length=80, null=True)
    scrubbed_underlying_title = models.CharField(max_length=80, null=True)
    underlying_ticker = models.CharField(max_length=10, null=True)
    underlying_shares_total = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    underlying_close_price = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    intrinsic_value = \
        models.DecimalField(max_digits=16, decimal_places=4, null=True)
    first_xn = models.DateField(null=True)
    most_recent_xn = models.DateField(null=True)
    wavg_xn_date = models.DateField(null=True)

    def __unicode__(self):
        return unicode(self.short_sec_title) or u''


class PersonHoldingView(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    owner = models.ForeignKey(ReportingPerson)
    person_name = models.CharField(max_length=80, null=True)
    person_title = models.CharField(max_length=80, null=True)
    security = models.ForeignKey(Security)
    affiliation = models.ForeignKey(Affiliation)
    short_sec_title = models.CharField(max_length=80, null=True)
    ticker = models.CharField(max_length=10, null=True)
    last_close_price = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    # security_title = models.CharField(max_length=80, null=True)
    units_held = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    first_expiration_date = models.DateField(null=True)
    last_expiration_date = models.DateField(null=True)
    wavg_expiration_date = models.DateField(null=True)
    min_conversion_price = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    max_conversion_price = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    wavg_conversion = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    # underlying_title = models.CharField(max_length=80, null=True)
    scrubbed_underlying_title = models.CharField(max_length=80, null=True)
    underlying_ticker = models.CharField(max_length=10, null=True)
    underlying_shares_total = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    underlying_close_price = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    intrinsic_value = \
        models.DecimalField(max_digits=16, decimal_places=4, null=True)
    first_xn = models.DateField(null=True)
    most_recent_xn = models.DateField(null=True)
    wavg_xn_date = models.DateField(null=True)

    def __unicode__(self):
        return unicode(self.short_sec_title) or u''


class FTPFileList(models.Model):
    files = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return unicode(len(self.files)) or u''


class SECDayIndex(models.Model):
    indexname = models.TextField()
    indexcontents = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return unicode(self.indexname) or u''


class FullForm(models.Model):
    sec_path = models.CharField(max_length=150, primary_key=True)
    save_date = models.DateField(null=True)
    issuer_cik_num = models.CharField(max_length=10)
    text = models.TextField()
    parsable = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s, %s" % (str(self.sec_path),
                            str(self.save_date))
    # def __unicode__(self):
        # return str(self.sec_path), str(self.save_date)


class Form345Entry(models.Model):
    entry_internal_id = models.CharField(max_length=80)
    period_of_report = models.DateField(null=True)
    issuer_cik = models.ForeignKey(IssuerCIK, null=True)
    issuer_cik_num = models.IntegerField(max_length=10)
    issuer_name = models.CharField(max_length=80, null=True)
    security = models.ForeignKey(Security, null=True,
                                 related_name="security_relationship")
    reporting_owner_cik = models.ForeignKey(ReportingPerson, null=True)
    reporting_owner_cik_num = models.IntegerField(max_length=10)
    reporting_owner_name = models.CharField(max_length=80, null=True)
    affiliation = models.ForeignKey(Affiliation, null=True)
    is_director = models.BooleanField()
    is_officer = models.BooleanField()
    is_ten_percent = models.BooleanField()
    is_something_else = models.BooleanField()
    reporting_owner_title = models.CharField(max_length=80, null=True)
    security_title = models.CharField(max_length=80, null=True)
    short_sec_title = models.CharField(max_length=80, null=True)
    conversion_price = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    transaction_date = models.DateField(null=True)
    transaction_code = models.CharField(max_length=2, null=True)
    transaction_shares = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    xn_price_per_share = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    xn_acq_disp_code = models.CharField(max_length=2, null=True)
    expiration_date = models.DateField(null=True)
    underlying_title = models.CharField(max_length=80, null=True)
    scrubbed_underlying_title = models.CharField(max_length=80, null=True)
    underlying_shares = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    shares_following_xn = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    reported_shares_following_xn = \
        models.DecimalField(max_digits=15, decimal_places=4, null=True)
    shares_following_xn_is_adjusted = models.BooleanField(default=False)
    direct_or_indirect = models.CharField(max_length=2, null=True)
    tenbfive_note = models.IntegerField(null=True)
    transaction_number = models.IntegerField(null=True)
    sec_path = models.CharField(max_length=150, null=True)
    sec_url = models.CharField(max_length=150, null=True)
    five_not_subject_to_section_sixteen = models.IntegerField(null=True)
    five_form_three_holdings = models.IntegerField(null=True)
    five_form_four_transactions = models.IntegerField(null=True)
    form_type = models.CharField(max_length=5, null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    filedatetime = models.DateTimeField()
    supersededdt = models.DateTimeField(null=True)
    # The below number is the number the reported shares must be multiplied by
    # to convert to today's units to account for special dividends and splits.
    adjustment_factor = models.DecimalField(max_digits=15, decimal_places=4,
                                            default=Decimal('1.00'))
    adjustment_date = models.DateField(null=True)
    underlying_security = \
        models.ForeignKey(Security, null=True,
                          related_name="underlying_relationship")

    def __unicode__(self):
        return str(self.entry_internal_id)


class DiscretionaryXnEvent(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    reporting_person = models.ForeignKey(ReportingPerson)
    person_title = models.CharField(max_length=80, null=True)
    security = models.ForeignKey(Security)
    form_entry = models.ForeignKey(Form345Entry, null=True)
    xn_acq_disp_code = models.CharField(max_length=1)
    transaction_code = models.CharField(max_length=1)
    xn_val = models.DecimalField(max_digits=15, decimal_places=2)
    xn_shares = models.DecimalField(max_digits=15, decimal_places=2)
    filedate = models.DateField()

    def __unicode__(self):
        return u"%s, %s, %s, %s, %s" % (str(self.issuer.name),
                                        str(self.security.short_sec_title),
                                        str(self.reporting_person.person_name),
                                        str(self.xn_val),
                                        str(self.filedate))


class PersonSignal(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    sec_price_hist = models.ForeignKey(SecurityPriceHist, null=True)
    reporting_person = models.ForeignKey(ReportingPerson)
    eq_annual_share_grants = \
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    security_1 = models.ForeignKey(Security)
    only_security_1 = models.BooleanField()

    reporting_person_title = models.CharField(max_length=80, null=True)
    signal_name = models.CharField(max_length=80, default='ERROR')
    signal_detect_date = models.DateField()
    first_file_date = models.DateField()
    last_file_date = models.DateField()
    transactions = models.IntegerField(max_length=15)

    average_price_sec_1 =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    gross_signal_value = models.DecimalField(max_digits=15, decimal_places=2)
    net_signal_value = models.DecimalField(max_digits=15, decimal_places=2)
    net_signal_shares = models.DecimalField(max_digits=15, decimal_places=2)
    prior_holding_value =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    net_signal_pct =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)

    preceding_stock_perf = models.DecimalField(max_digits=15, decimal_places=2,
                                               null=True)
    perf_period_days = models.IntegerField(max_length=3)
    perf_after_detection =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    subs_stock_period_days = models.IntegerField(max_length=3)

    significant = models.BooleanField()
    new = models.BooleanField()

    def __unicode__(self):
        return u"%s, %s, %s, %s" % (str(self.issuer.name),
                                    str(self.reporting_person.person_name),
                                    str(self.net_signal_value),
                                    str(self.signal_detect_date))


class SigDisplay(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    sec_price_hist = models.ForeignKey(SecurityPriceHist, null=True)
    last_signal = models.DateField(null=True)

    # Buy on Weakness
    buy_on_weakness = models.CharField(max_length=500, null=True)
    bow_plural_insiders = models.NullBooleanField(null=True)
    bow_start_date = models.DateField(null=True)
    bow_end_date = models.DateField(null=True)
    bow_first_sig_detect_date = models.DateField(null=True)
    bow_person_name = models.CharField(max_length=80, null=True)
    bow_includes_ceo = models.NullBooleanField(null=True)
    bow_net_signal_value =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    bow_first_perf_period_days = models.IntegerField(max_length=3, null=True)
    bow_first_pre_stock_perf =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    bow_first_post_stock_perf =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)

    # Cluster Buy
    cluster_buy = models.CharField(max_length=500, null=True)
    cb_start_date = models.DateField(null=True)
    cb_end_date = models.DateField(null=True)
    cb_plural_insiders = models.NullBooleanField(null=True)
    cb_buy_xns = models.IntegerField(max_length=3, null=True)
    cb_net_xn_value =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)

    # Discretionary Buy
    discretionary_buy = models.CharField(max_length=500, null=True)
    db_large_xn_size = models.NullBooleanField(null=True)
    db_was_ceo = models.NullBooleanField(null=True)
    db_start_date = models.DateField(null=True)
    db_end_date = models.DateField(null=True)
    db_detect_date = models.DateField(null=True)
    db_person_name = models.CharField(max_length=80, null=True)
    db_xn_val = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    db_security_name = models.CharField(max_length=80, null=True)
    db_xn_pct_holdings =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)

    # Sell on Strength
    sell_on_strength = models.CharField(max_length=500, null=True)
    sos_plural_insiders = models.NullBooleanField(null=True)
    sos_start_date = models.DateField(null=True)
    sos_end_date = models.DateField(null=True)
    sos_first_sig_detect_date = models.DateField(null=True)
    sos_person_name = models.CharField(max_length=80, null=True)
    sos_includes_ceo = models.NullBooleanField(null=True)
    sos_net_signal_value =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sos_first_perf_period_days = models.IntegerField(max_length=3, null=True)
    sos_first_pre_stock_perf =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sos_first_post_stock_perf =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)

    # Cluster Sell
    cluster_sell = models.CharField(max_length=500, null=True)
    cs_start_date = models.DateField(null=True)
    cs_end_date = models.DateField(null=True)
    cs_plural_insiders = models.NullBooleanField(null=True)
    cs_sell_xns = models.IntegerField(max_length=3, null=True)
    cs_net_xn_value =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    cs_annual_grant_rate =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    cs_net_shares =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)
    # Discretionary Sell
    discretionary_sell = models.CharField(max_length=500, null=True)
    ds_large_xn_size = models.NullBooleanField(null=True)
    ds_was_ceo = models.NullBooleanField(null=True)
    ds_start_date = models.DateField(null=True)
    ds_end_date = models.DateField(null=True)
    ds_detect_date = models.DateField(null=True)
    ds_person_name = models.CharField(max_length=80, null=True)
    ds_xn_val = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ds_security_name = models.CharField(max_length=80, null=True)
    ds_xn_pct_holdings =\
        models.DecimalField(max_digits=15, decimal_places=2, null=True)

    total_transactions = models.IntegerField(max_length=15)
    # mixed_signals = models.BooleanField()
    signal_is_new = models.BooleanField()

    def __unicode__(self):
        return u"%s, %s" % (str(self.issuer.name),
                            str(self.total_transactions))
