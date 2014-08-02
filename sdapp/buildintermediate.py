from sdapp.models import ReportingPerson, IssuerCIK, Form345Entry,\
    Affiliation, Holding


def update_reportingpersons():
    source_entries = Form345Entry.\
        objects.values_list('reporting_owner_cik_num', flat=True).distinct()
    all_entries = Form345Entry.objects.all()
    # all_issuer_ciks = IssuerCIK.objects.all()
    existing_reportingperson = ReportingPerson.\
        objects.values_list('reporting_owner_cik_num', flat=True).distinct()
    print 'creating reporting person entries'
    entries = []
    print 'building person list'
    for entry in source_entries:
        # try:
        if entry not in existing_reportingperson:
            ciknum = entry
            xns = all_entries.filter(reporting_owner_cik_num=ciknum).\
                exclude(period_of_report__isnull=True).\
                order_by('-period_of_report')
            if xns.exists():
                latest_xn = xns[0]
            else:
                xns = all_entries.filter(reporting_owner_cik_num=ciknum)
                latest_xn = xns[0]
            name = latest_xn.reporting_owner_name
            entrytosave = ReportingPerson(person_name=name,
                                          reporting_owner_cik_num=ciknum)
            entries.append(entrytosave)
            # issuerciks = all_entries.filter(reporting_owner_cik_num=entry).\
                # values_list('issuer_cik_num', flat=True).distinct()
            # for issuercik in issuerciks:
                # entrytosave.issuer = all_issuer_ciks.get(cik_num=issuercik)
        # except:
            # print 'error:', entry
    print 'saving'
    ReportingPerson.objects.bulk_create(entries)
    print 'done updating reporting persons'


def new_affiliation(all_issuer_ciks, issuer_cik, person, name, personentries):
    newaffiliation = Affiliation()
    newaffiliation.issuer = all_issuer_ciks.get(cik_num=str(int(issuer_cik)))
    newaffiliation.reporting_owner = person
    newaffiliation.issuer_cik_num = issuer_cik
    newaffiliation.reporting_owner_cik_num =\
        person.reporting_owner_cik_num
    newaffiliation.person_name = name

    affiliationentries = personentries\
        .filter(issuer_cik_num=issuer_cik)
    if affiliationentries.exclude(period_of_report__isnull=True).exists():
        latestentry = affiliationentries\
            .exclude(period_of_report__isnull=True)\
            .order_by('-period_of_report')[0]
        firstentry = affiliationentries\
            .exclude(period_of_report__isnull=True)\
            .order_by('period_of_report')[0]
        newaffiliation.first_filing = firstentry.period_of_report
        newaffiliation.most_recent_filing = latestentry\
            .period_of_report
        governingentry = latestentry
        newaffiliation.title = governingentry.reporting_owner_title
        newaffiliation.is_director = governingentry.is_director
        newaffiliation.is_officer = governingentry.is_officer
        newaffiliation.is_ten_percent = governingentry.is_ten_percent
        newaffiliation.is_something_else = governingentry.is_something_else
        return newaffiliation
    # else:
    #     governingentry = affiliationentries[0]
    # newaffiliation.title = governingentry.reporting_owner_title
    # newaffiliation.is_director = governingentry.is_director
    # newaffiliation.is_officer = governingentry.is_officer
    # newaffiliation.is_ten_percent = governingentry.is_ten_percent
    # newaffiliation.is_something_else = governingentry.is_something_else

    return None


def update_affiliation(affiliationupd, all_issuer_ciks, issuer_cik, person,
                       name, personentries):
    affiliationupd.issuer = all_issuer_ciks.get(cik_num=str(int(issuer_cik)))
    affiliationupd.reporting_owner = person
    affiliationupd.person_name = name
    affiliationentries = personentries\
        .filter(issuer_cik_num=issuer_cik)
    if affiliationentries.exclude(period_of_report__isnull=True).exists():
        latestentry = affiliationentries\
            .exclude(period_of_report__isnull=True)\
            .order_by('-period_of_report')[0]
        affiliationupd.most_recent_filing = latestentry\
            .period_of_report
        governingentry = latestentry
        affiliationupd.title = governingentry.reporting_owner_title
        affiliationupd.is_director = governingentry.is_director
        affiliationupd.is_officer = governingentry.is_officer
        affiliationupd.is_ten_percent = governingentry.is_ten_percent
        affiliationupd.is_something_else = governingentry.is_something_else
        affiliationupd.save()
    # else:
    #     governingentry = affiliationentries[0]
    # affiliationupd.title = governingentry.reporting_owner_title
    # affiliationupd.is_director = governingentry.is_director
    # affiliationupd.is_officer = governingentry.is_officer
    # affiliationupd.is_ten_percent = governingentry.is_ten_percent
    # affiliationupd.is_something_else = governingentry.is_something_else
    # affiliationupd.save()


def revise_affiliations():
    allpersons = ReportingPerson.objects.all()
    allentries = Form345Entry.objects.all()
    all_issuer_ciks = IssuerCIK.objects.all()
    old_affiliations = Affiliation.objects.all()
    entries = []
    print 'building affiliation list'
    for person in allpersons:
        personentries = allentries\
            .filter(reporting_owner_cik_num=person.reporting_owner_cik_num)
        personissuerciks = personentries\
            .values_list('issuer_cik_num', flat=True).distinct()
        name = person.person_name
        person_cik = person.reporting_owner_cik_num
        for issuer_cik in personissuerciks:
            aff_set = old_affiliations.filter(issuer_cik_num=issuer_cik)\
                .filter(reporting_owner_cik_num=person_cik)
            if not aff_set.exists():
                newaffiliation = new_affiliation(all_issuer_ciks, issuer_cik,
                                                 person, name, personentries)
                if newaffiliation is not None:
                    entries.append(newaffiliation)
            if aff_set.exists():
                # if there is already an entry we determine whether to update
                affiliationentries = personentries\
                    .filter(issuer_cik_num=issuer_cik)\
                    .exclude(period_of_report__isnull=True)
                if affiliationentries.exists():
                    latestentry = affiliationentries\
                        .order_by('-period_of_report')[0]
                    if latestentry.period_of_report !=\
                            aff_set[0].most_recent_filing:
                        update_affiliation(aff_set[0], all_issuer_ciks,
                                           issuer_cik, person, name,
                                           personentries)

    print 'saving'
    Affiliation.objects.bulk_create(entries)
    print 'done updating affiliations'


def new_holding(title, expdate, affiliationentries, affiliation):
    newholding = Holding()
    newholding.issuer = affiliation.issuer
    newholding.owner = affiliation.reporting_owner
    newholding.affiliation = affiliation
    newholding.security_title = title
    newholding.expiration_date = expdate

    holdingentries = affiliationentries.filter(security_title=title)\
        .filter(expiration_date=expdate)
    if holdingentries.exclude(transaction_date__isnull=True).exists():
        latestxndate = holdingentries\
            .exclude(transaction_date__isnull=True)\
            .order_by('-transaction_date')[0].transaction_date
        latestxn = holdingentries\
            .filter(transaction_date=latestxndate)\
            .order_by('-transaction_number')[0]
        firstxn = holdingentries\
            .exclude(transaction_date__isnull=True)\
            .order_by('transaction_date')[0]
        newholding.first_xn = firstxn.transaction_date
        newholding.most_recent_xn = latestxn.transaction_date
        newholding.units_held = latestxn.shares_following_xn
        newholding.deriv_or_nonderiv = latestxn.deriv_or_nonderiv
        newholding.conversion_price = latestxn.conversion_price
        newholding.underlying_title = latestxn.underlying_title
        newholding.underlying_shares = latestxn.underlying_shares

        return newholding

    # elif len(holdingentries
    #          .exclude(period_of_report__isnull=True)
    #          .order_by('-period_of_report')) != 0:
    #     governingentry = holdingentries\
    #         .exclude(period_of_report__isnull=True)\
    #         .order_by('-period_of_report')[0]
    #     newholding.units_held = governingentry.shares_following_xn
    #     newholding.deriv_or_nonderiv = governingentry.deriv_or_nonderiv
    #     newholding.underlying_title = governingentry.underlying_title
    #     newholding.underlying_shares = governingentry.underlying_shares

    return None


def update_holding(holding, title, expdate, holdingentries, affiliation):
    if holdingentries.exclude(transaction_date__isnull=True).exists():
        latestxndate = holdingentries\
            .exclude(transaction_date__isnull=True)\
            .order_by('-transaction_date')[0].transaction_date
        latestxn = holdingentries\
            .filter(transaction_date=latestxndate)\
            .order_by('-transaction_number')[0]
        holding.most_recent_xn = latestxn\
            .transaction_date
        holding.units_held = latestxn.shares_following_xn
        holding.deriv_or_nonderiv = latestxn.deriv_or_nonderiv
        holding.conversion_price = latestxn.conversion_price
        holding.underlying_title = latestxn.underlying_title
        holding.underlying_shares = latestxn.underlying_shares
        holding.save()

    # elif len(holdingentries
    #          .exclude(period_of_report__isnull=True)
    #          .order_by('-period_of_report')) != 0:
    #     governingentry = holdingentries[0]
    #     holding.units_held = governingentry.shares_following_xn
    #     holding.deriv_or_nonderiv = governingentry.deriv_or_nonderiv
    #     holding.underlying_title = governingentry.underlying_title
    #     holding.underlying_shares = governingentry.underlying_shares


def revise_holdings():
    allentries = Form345Entry.objects.all()
    all_affiliations = Affiliation.objects.all()
    old_holdings = Holding.objects.all()
    entries = []
    print 'building holding list'
    looplength = float(len(all_affiliations))
    count = 0.0
    for affiliation in all_affiliations:
        if float(int(10*count/looplength)) !=\
                float(int(10*(count-1)/looplength)):
            print int(count/looplength*100), 'percent'
        count += 1.0
        # the security title and underlying title mechanic could create issues
        # if someone writes the titles inconsistently from form to form this
        # could be the source of very bad data, so we need to test
        affiliationentries = allentries\
            .filter(issuer_cik_num=
                    affiliation.issuer_cik_num)\
            .filter(reporting_owner_cik_num=
                    affiliation.reporting_owner_cik_num)
        affiliation_security_titles = affiliationentries\
            .values_list('security_title', flat=True).distinct()
        title_expiration_list = []
        # This for loop constructs a flat list of securities with distinct
        # titles AND expiration dates.
        for title in affiliation_security_titles:
            titleexpirationdates = affiliationentries\
                .filter(security_title=title)\
                .values_list('expiration_date', flat=True).distinct()
            if not titleexpirationdates.exists():
                titleset = [title, None]
                title_expiration_list.append(titleset)
            else:
                for expdate in titleexpirationdates:
                    titleset = [title, expdate]
                    title_expiration_list.append(titleset)
        # This for loop determines whether the holding already exists and
        # either adds or updates it as appropriate
        for title_and_date_set in title_expiration_list:
            title, expdate = title_and_date_set
            titledate_holding = old_holdings.filter(security_title=title)\
                .filter(expiration_date=expdate)
            if not titledate_holding.exists():
                newholding = new_holding(title, expdate, affiliationentries,
                                         affiliation)
                if newholding is not None:
                    entries.append(newholding)
            if titledate_holding.exists():
                # if there is already an entry we determine whether to update
                holdingentries = affiliationentries\
                    .filter(security_title=title)\
                    .filter(expiration_date=expdate)
                nonullholdingentries = holdingentries\
                    .exclude(period_of_report__isnull=True)
                if nonullholdingentries.exists():
                    latestentry = nonullholdingentries\
                        .order_by('-period_of_report')[0]
                    if latestentry.transaction_date !=\
                            titledate_holding[0].most_recent_xn:
                        update_holding(titledate_holding[0], title, expdate,
                                       holdingentries, affiliation)
    print 'saving'
    Holding.objects.bulk_create(entries)
    print 'done updating holdings'

update_reportingpersons()
revise_affiliations()
revise_holdings()