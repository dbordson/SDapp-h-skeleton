from django.shortcuts import render_to_response
from sdapp.models import CompanyStockHist, ClosePrice, IssuerCIK, Form345Entry


def options(request, ticker_sym):
    tickersym = ticker_sym
    return render_to_response('sdapp/options.html',
                              {'tickersym': tickersym})


def pricedetail(request, ticker_sym):
    stockid = CompanyStockHist.objects.filter(ticker_sym=ticker_sym)[0]

    pricelist = ClosePrice.objects.filter(companystockhist=stockid)
    return render_to_response('sdapp/pricedetail.html',
                              {'pricelist': pricelist})


def formentrydetail(request, ticker_sym):
    stockid = CompanyStockHist.objects.get(ticker_sym=ticker_sym)
    cikforticker = IssuerCIK.objects.filter(companystockhist_id=stockid)[0]
    cikidforticker = cikforticker.companystockhist_id
    entrylist = Form345Entry.objects.filter(issuer_cik_id=cikidforticker)
    # pricelist = ClosePrice.objects.filter(companystockhist=stockid)
    return render_to_response('sdapp/entrydetail.html',
                              {'entrylist': entrylist,
                               'cikforticker': cikforticker,
                               'cikidforticker': cikidforticker})
