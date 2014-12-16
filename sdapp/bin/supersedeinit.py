from sdapp.models import Form345Entry
# from django.db import connection
import datetime


def convert_date_to_datetimestring(date):
    c = str(date)
    return c[:10] + " 23:59:59Z"

# entries34, untagged_entries


def superseded_initialize():
    print "Calculating superseded dates of unsuperseded forms..."
    entries34 = Form345Entry.objects\
        .exclude(filedatetime=None)\
        .exclude(short_sec_title=None)
    untagged_entries = entries34.filter(supersededdt=None)
    looplength = float(len(untagged_entries))
    counter = 0.0
    today = datetime.date.today()
    for untagged_entry in untagged_entries:
        # Counter below
        if float(int(10*counter/looplength)) !=\
                float(int(10*(counter-1)/looplength)):
            print int(counter/looplength*100), 'percent'
        counter += 1.0
        # Logic below
        supersededdt_already_assigned = False

        # This adjusts Form 3, 3/A entries to work, since they lack
        # transaction dates and instead tie to the period of the report.
        date_of_untagged_entry = untagged_entry.transaction_date
        if date_of_untagged_entry is None:
            date_of_untagged_entry = \
                untagged_entry.period_of_report

        # The below may happen when a form 5 reflecting an old transaction
        # is filed.
        was_the_filing_superseded_before_filed = \
            entries34\
            .filter(issuer_cik_num=untagged_entry.issuer_cik_num)\
            .filter(reporting_owner_cik_num=untagged_entry
                    .reporting_owner_cik_num)\
            .filter(short_sec_title=untagged_entry.short_sec_title)\
            .filter(expiration_date=untagged_entry.expiration_date)\
            .filter(filedatetime__lt=untagged_entry.filedatetime)\
            .filter(transaction_date__gt=date_of_untagged_entry)\
            .exists()
        if was_the_filing_superseded_before_filed is True:
            untagged_entry.supersededdt = untagged_entry.filedatetime
            untagged_entry.save()
            supersededdt_already_assigned = True

        # The below will happen when a single form provides multiple
        # transactions in a single security.  All transactions but the last
        # will be superseded at the moment the form is filed.

        was_the_filing_superseded_by_the_same_form = \
            entries34\
            .filter(issuer_cik_num=untagged_entry.issuer_cik_num)\
            .filter(reporting_owner_cik_num=untagged_entry
                    .reporting_owner_cik_num)\
            .filter(short_sec_title=untagged_entry.short_sec_title)\
            .filter(expiration_date=untagged_entry.expiration_date)\
            .filter(filedatetime=untagged_entry.filedatetime)\
            .filter(transaction_number__gt=untagged_entry.transaction_number)\
            .exists()
        if supersededdt_already_assigned is False and\
                was_the_filing_superseded_by_the_same_form is True:
            untagged_entry.supersededdt = untagged_entry.filedatetime
            untagged_entry.save()
            supersededdt_already_assigned = True

        # The below handles derivatives that have expired

        if supersededdt_already_assigned is False and\
                untagged_entry.expiration_date is not None and\
                today >= untagged_entry.expiration_date:
            untagged_entry.supersededdt = \
                convert_date_to_datetimestring(untagged_entry.expiration_date)
            untagged_entry.save()
            supersededdt_already_assigned = True

        # The below handles the general case where subsequent filings with
        # simultaneous or later transactions supersede current transactions
        #
        # FYI there is voodoo here and in the first if statement, because we
        # don't have a module that is dealing with form amendments in a
        # sophisticated way.  There is the possibility that someone could
        # amend a transaction in the middle of a form 4 but not later
        # transactions.  The logic will supersede the whole day's transactions
        # when it notices a subsequent amendment to a transaction on that day
        # because it doesn't know better (and I can't figure out silver bullet
        # solution, in light of the often inconsistent way these forms are
        # completed).

        if supersededdt_already_assigned is False:
            filtered_entries = entries34\
                .filter(issuer_cik_num=untagged_entry.issuer_cik_num)\
                .filter(reporting_owner_cik_num=untagged_entry
                        .reporting_owner_cik_num)\
                .filter(short_sec_title=untagged_entry.short_sec_title)\
                .filter(expiration_date=untagged_entry.expiration_date)\
                .filter(filedatetime__gt=untagged_entry.filedatetime)\
                .exclude(transaction_date__lte=date_of_untagged_entry)\
                .order_by('filedatetime')
            if filtered_entries.exists():
                untagged_entry.supersededdt = filtered_entries[0].filedatetime
                untagged_entry.save()
    print 'Done.'
    return

# not just transactions
# first check if same datetime filed
# if same datetime test for xn number, if not same,
# test for closest date
# treat form 5 correctly? -- maybe use xn date as a proxy for filedate,
# because would be a poor assumption to assume it is latest?

# How do you best remove the entries recently tagged as superseded from the
# query set?

superseded_initialize()
