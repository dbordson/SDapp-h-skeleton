# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HoldingType'
        db.create_table(u'sdapp_holdingtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('affiliation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Affiliation'])),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('units_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('first_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('last_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('wavg_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('min_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('max_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('wavg_conversion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('underlying_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('underlying_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('intrinsic_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('first_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('most_recent_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('wavg_xn_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('transactions_included', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('tranches_included', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('units_transacted', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
        ))
        db.send_create_signal(u'sdapp', ['HoldingType'])


    def backwards(self, orm):
        # Deleting model 'HoldingType'
        db.delete_table(u'sdapp_holdingtype')


    models = {
        u'sdapp.affiliation': {
            'Meta': {'object_name': 'Affiliation'},
            'first_filing': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_director': ('django.db.models.fields.BooleanField', [], {}),
            'is_officer': ('django.db.models.fields.BooleanField', [], {}),
            'is_something_else': ('django.db.models.fields.BooleanField', [], {}),
            'is_ten_percent': ('django.db.models.fields.BooleanField', [], {}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'issuer_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'most_recent_filing': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'reporting_owner_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        u'sdapp.closeprice': {
            'Meta': {'object_name': 'ClosePrice'},
            'close_date': ('django.db.models.fields.DateField', [], {}),
            'close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'companystockhist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.CompanyStockHist']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sdapp.companystockhist': {
            'Meta': {'object_name': 'CompanyStockHist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']", 'null': 'True'}),
            'ticker_sym': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'sdapp.form345entry': {
            'Meta': {'object_name': 'Form345Entry'},
            'conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'direct_or_indirect': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'entry_internal_id': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'five_form_four_transactions': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'five_form_three_holdings': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'five_not_subject_to_section_sixteen': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'form_type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_director': ('django.db.models.fields.BooleanField', [], {}),
            'is_officer': ('django.db.models.fields.BooleanField', [], {}),
            'is_something_else': ('django.db.models.fields.BooleanField', [], {}),
            'is_ten_percent': ('django.db.models.fields.BooleanField', [], {}),
            'issuer_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']", 'null': 'True'}),
            'issuer_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'period_of_report': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'reporting_owner_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']", 'null': 'True'}),
            'reporting_owner_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'reporting_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'shares_following_xn': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'source_name_partial_path': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'tenbfive_note': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transaction_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'transaction_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'transaction_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transaction_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'xn_acq_disp_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'xn_price_per_share': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'})
        },
        u'sdapp.holding': {
            'Meta': {'object_name': 'Holding'},
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Affiliation']"}),
            'conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'most_recent_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'underlying_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'units_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'})
        },
        u'sdapp.holdingtype': {
            'Meta': {'object_name': 'HoldingType'},
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Affiliation']"}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'first_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intrinsic_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'max_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'min_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'most_recent_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'tranches_included': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transactions_included': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'underlying_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'units_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'units_transacted': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_conversion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'wavg_xn_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        u'sdapp.issuercik': {
            'Meta': {'object_name': 'IssuerCIK'},
            'cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sdapp.reportingperson': {
            'Meta': {'object_name': 'ReportingPerson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'reporting_owner_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['sdapp']