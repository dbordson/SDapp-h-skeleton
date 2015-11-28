# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Affiliation.average_conversion_price_ratio_percentile'
        db.delete_column(u'sdapp_affiliation', 'average_conversion_price_ratio_percentile')

        # Deleting field 'Affiliation.share_equivalents_value_percentile'
        db.delete_column(u'sdapp_affiliation', 'share_equivalents_value_percentile')

        # Deleting field 'Affiliation.equity_grant_value_percentile'
        db.delete_column(u'sdapp_affiliation', 'equity_grant_value_percentile')

        # Adding field 'Affiliation.prior_share_equivalents_held'
        db.add_column(u'sdapp_affiliation', 'prior_share_equivalents_held',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.prior_average_conversion_price'
        db.add_column(u'sdapp_affiliation', 'prior_average_conversion_price',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.prior_share_equivalents_value'
        db.add_column(u'sdapp_affiliation', 'prior_share_equivalents_value',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.prior_conversion_to_price_ratio'
        db.add_column(u'sdapp_affiliation', 'prior_conversion_to_price_ratio',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Deleting field 'SigDisplay.discretionary_buy'
        db.delete_column(u'sdapp_sigdisplay', 'discretionary_buy')

        # Deleting field 'SigDisplay.sell_on_strength'
        db.delete_column(u'sdapp_sigdisplay', 'sell_on_strength')

        # Deleting field 'SigDisplay.discretionary_sell'
        db.delete_column(u'sdapp_sigdisplay', 'discretionary_sell')

        # Deleting field 'SigDisplay.cluster_sell'
        db.delete_column(u'sdapp_sigdisplay', 'cluster_sell')

        # Deleting field 'SigDisplay.cluster_buy'
        db.delete_column(u'sdapp_sigdisplay', 'cluster_buy')

        # Deleting field 'SigDisplay.buy_on_weakness'
        db.delete_column(u'sdapp_sigdisplay', 'buy_on_weakness')

        # Adding field 'SigDisplay.buyonweakness'
        db.add_column(u'sdapp_sigdisplay', 'buyonweakness',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SigDisplay.clusterbuy'
        db.add_column(u'sdapp_sigdisplay', 'clusterbuy',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SigDisplay.discretionarybuy'
        db.add_column(u'sdapp_sigdisplay', 'discretionarybuy',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SigDisplay.sellonstrength'
        db.add_column(u'sdapp_sigdisplay', 'sellonstrength',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SigDisplay.clustersell'
        db.add_column(u'sdapp_sigdisplay', 'clustersell',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SigDisplay.discretionarysell'
        db.add_column(u'sdapp_sigdisplay', 'discretionarysell',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SigDisplay.saleofall'
        db.add_column(u'sdapp_sigdisplay', 'saleofall',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SigDisplay.soa_detect_date'
        db.add_column(u'sdapp_sigdisplay', 'soa_detect_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.soa_start_date'
        db.add_column(u'sdapp_sigdisplay', 'soa_start_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.soa_end_date'
        db.add_column(u'sdapp_sigdisplay', 'soa_end_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.soa_primary_affiliation'
        db.add_column(u'sdapp_sigdisplay', 'soa_primary_affiliation',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Affiliation'], null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.soa_inc_ceo'
        db.add_column(u'sdapp_sigdisplay', 'soa_inc_ceo',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SigDisplay.soa_people_count'
        db.add_column(u'sdapp_sigdisplay', 'soa_people_count',
                      self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.soa_biggest_value'
        db.add_column(u'sdapp_sigdisplay', 'soa_biggest_value',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.soa_total_value'
        db.add_column(u'sdapp_sigdisplay', 'soa_total_value',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.active_insiders'
        db.add_column(u'sdapp_sigdisplay', 'active_insiders',
                      self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.sellers'
        db.add_column(u'sdapp_sigdisplay', 'sellers',
                      self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.insiders_reduced_holdings'
        db.add_column(u'sdapp_sigdisplay', 'insiders_reduced_holdings',
                      self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.average_holding_reduction'
        db.add_column(u'sdapp_sigdisplay', 'average_holding_reduction',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.number_of_recent_shares_sold'
        db.add_column(u'sdapp_sigdisplay', 'number_of_recent_shares_sold',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.value_of_recent_shares_sold'
        db.add_column(u'sdapp_sigdisplay', 'value_of_recent_shares_sold',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.historical_selling_rate_shares'
        db.add_column(u'sdapp_sigdisplay', 'historical_selling_rate_shares',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.historical_selling_rate_value'
        db.add_column(u'sdapp_sigdisplay', 'historical_selling_rate_value',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.percent_change_in_shares_historical_to_recent'
        db.add_column(u'sdapp_sigdisplay', 'percent_change_in_shares_historical_to_recent',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.percent_change_in_value_historical_to_recent'
        db.add_column(u'sdapp_sigdisplay', 'percent_change_in_value_historical_to_recent',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.percent_options_converted_to_expire_in_current_year'
        db.add_column(u'sdapp_sigdisplay', 'percent_options_converted_to_expire_in_current_year',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.percent_shares_sold_under_10b5_1_plans'
        db.add_column(u'sdapp_sigdisplay', 'percent_shares_sold_under_10b5_1_plans',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.recent_share_sell_rate_for_10b5_1_plans'
        db.add_column(u'sdapp_sigdisplay', 'recent_share_sell_rate_for_10b5_1_plans',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.historical_share_sell_rate_for_10b5_1_plans'
        db.add_column(u'sdapp_sigdisplay', 'historical_share_sell_rate_for_10b5_1_plans',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.sell_price_trigger_detected'
        db.add_column(u'sdapp_sigdisplay', 'sell_price_trigger_detected',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SigDisplay.trigger_price'
        db.add_column(u'sdapp_sigdisplay', 'trigger_price',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.trigger_date'
        db.add_column(u'sdapp_sigdisplay', 'trigger_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.trigger_subs_performance'
        db.add_column(u'sdapp_sigdisplay', 'trigger_subs_performance',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'SigDisplay.avg_prior_trigger_performance'
        db.add_column(u'sdapp_sigdisplay', 'avg_prior_trigger_performance',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)


        # Changing field 'SigDisplay.total_transactions'
        db.alter_column(u'sdapp_sigdisplay', 'total_transactions', self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True))

    def backwards(self, orm):
        # Adding field 'Affiliation.average_conversion_price_ratio_percentile'
        db.add_column(u'sdapp_affiliation', 'average_conversion_price_ratio_percentile',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.share_equivalents_value_percentile'
        db.add_column(u'sdapp_affiliation', 'share_equivalents_value_percentile',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.equity_grant_value_percentile'
        db.add_column(u'sdapp_affiliation', 'equity_grant_value_percentile',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Deleting field 'Affiliation.prior_share_equivalents_held'
        db.delete_column(u'sdapp_affiliation', 'prior_share_equivalents_held')

        # Deleting field 'Affiliation.prior_average_conversion_price'
        db.delete_column(u'sdapp_affiliation', 'prior_average_conversion_price')

        # Deleting field 'Affiliation.prior_share_equivalents_value'
        db.delete_column(u'sdapp_affiliation', 'prior_share_equivalents_value')

        # Deleting field 'Affiliation.prior_conversion_to_price_ratio'
        db.delete_column(u'sdapp_affiliation', 'prior_conversion_to_price_ratio')

        # Adding field 'SigDisplay.discretionary_buy'
        db.add_column(u'sdapp_sigdisplay', 'discretionary_buy',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.sell_on_strength'
        db.add_column(u'sdapp_sigdisplay', 'sell_on_strength',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.discretionary_sell'
        db.add_column(u'sdapp_sigdisplay', 'discretionary_sell',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.cluster_sell'
        db.add_column(u'sdapp_sigdisplay', 'cluster_sell',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.cluster_buy'
        db.add_column(u'sdapp_sigdisplay', 'cluster_buy',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True),
                      keep_default=False)

        # Adding field 'SigDisplay.buy_on_weakness'
        db.add_column(u'sdapp_sigdisplay', 'buy_on_weakness',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True),
                      keep_default=False)

        # Deleting field 'SigDisplay.buyonweakness'
        db.delete_column(u'sdapp_sigdisplay', 'buyonweakness')

        # Deleting field 'SigDisplay.clusterbuy'
        db.delete_column(u'sdapp_sigdisplay', 'clusterbuy')

        # Deleting field 'SigDisplay.discretionarybuy'
        db.delete_column(u'sdapp_sigdisplay', 'discretionarybuy')

        # Deleting field 'SigDisplay.sellonstrength'
        db.delete_column(u'sdapp_sigdisplay', 'sellonstrength')

        # Deleting field 'SigDisplay.clustersell'
        db.delete_column(u'sdapp_sigdisplay', 'clustersell')

        # Deleting field 'SigDisplay.discretionarysell'
        db.delete_column(u'sdapp_sigdisplay', 'discretionarysell')

        # Deleting field 'SigDisplay.saleofall'
        db.delete_column(u'sdapp_sigdisplay', 'saleofall')

        # Deleting field 'SigDisplay.soa_detect_date'
        db.delete_column(u'sdapp_sigdisplay', 'soa_detect_date')

        # Deleting field 'SigDisplay.soa_start_date'
        db.delete_column(u'sdapp_sigdisplay', 'soa_start_date')

        # Deleting field 'SigDisplay.soa_end_date'
        db.delete_column(u'sdapp_sigdisplay', 'soa_end_date')

        # Deleting field 'SigDisplay.soa_primary_affiliation'
        db.delete_column(u'sdapp_sigdisplay', 'soa_primary_affiliation_id')

        # Deleting field 'SigDisplay.soa_inc_ceo'
        db.delete_column(u'sdapp_sigdisplay', 'soa_inc_ceo')

        # Deleting field 'SigDisplay.soa_people_count'
        db.delete_column(u'sdapp_sigdisplay', 'soa_people_count')

        # Deleting field 'SigDisplay.soa_biggest_value'
        db.delete_column(u'sdapp_sigdisplay', 'soa_biggest_value')

        # Deleting field 'SigDisplay.soa_total_value'
        db.delete_column(u'sdapp_sigdisplay', 'soa_total_value')

        # Deleting field 'SigDisplay.active_insiders'
        db.delete_column(u'sdapp_sigdisplay', 'active_insiders')

        # Deleting field 'SigDisplay.sellers'
        db.delete_column(u'sdapp_sigdisplay', 'sellers')

        # Deleting field 'SigDisplay.insiders_reduced_holdings'
        db.delete_column(u'sdapp_sigdisplay', 'insiders_reduced_holdings')

        # Deleting field 'SigDisplay.average_holding_reduction'
        db.delete_column(u'sdapp_sigdisplay', 'average_holding_reduction')

        # Deleting field 'SigDisplay.number_of_recent_shares_sold'
        db.delete_column(u'sdapp_sigdisplay', 'number_of_recent_shares_sold')

        # Deleting field 'SigDisplay.value_of_recent_shares_sold'
        db.delete_column(u'sdapp_sigdisplay', 'value_of_recent_shares_sold')

        # Deleting field 'SigDisplay.historical_selling_rate_shares'
        db.delete_column(u'sdapp_sigdisplay', 'historical_selling_rate_shares')

        # Deleting field 'SigDisplay.historical_selling_rate_value'
        db.delete_column(u'sdapp_sigdisplay', 'historical_selling_rate_value')

        # Deleting field 'SigDisplay.percent_change_in_shares_historical_to_recent'
        db.delete_column(u'sdapp_sigdisplay', 'percent_change_in_shares_historical_to_recent')

        # Deleting field 'SigDisplay.percent_change_in_value_historical_to_recent'
        db.delete_column(u'sdapp_sigdisplay', 'percent_change_in_value_historical_to_recent')

        # Deleting field 'SigDisplay.percent_options_converted_to_expire_in_current_year'
        db.delete_column(u'sdapp_sigdisplay', 'percent_options_converted_to_expire_in_current_year')

        # Deleting field 'SigDisplay.percent_shares_sold_under_10b5_1_plans'
        db.delete_column(u'sdapp_sigdisplay', 'percent_shares_sold_under_10b5_1_plans')

        # Deleting field 'SigDisplay.recent_share_sell_rate_for_10b5_1_plans'
        db.delete_column(u'sdapp_sigdisplay', 'recent_share_sell_rate_for_10b5_1_plans')

        # Deleting field 'SigDisplay.historical_share_sell_rate_for_10b5_1_plans'
        db.delete_column(u'sdapp_sigdisplay', 'historical_share_sell_rate_for_10b5_1_plans')

        # Deleting field 'SigDisplay.sell_price_trigger_detected'
        db.delete_column(u'sdapp_sigdisplay', 'sell_price_trigger_detected')

        # Deleting field 'SigDisplay.trigger_price'
        db.delete_column(u'sdapp_sigdisplay', 'trigger_price')

        # Deleting field 'SigDisplay.trigger_date'
        db.delete_column(u'sdapp_sigdisplay', 'trigger_date')

        # Deleting field 'SigDisplay.trigger_subs_performance'
        db.delete_column(u'sdapp_sigdisplay', 'trigger_subs_performance')

        # Deleting field 'SigDisplay.avg_prior_trigger_performance'
        db.delete_column(u'sdapp_sigdisplay', 'avg_prior_trigger_performance')


        # Changing field 'SigDisplay.total_transactions'
        db.alter_column(u'sdapp_sigdisplay', 'total_transactions', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=15))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sdapp.affiliation': {
            'Meta': {'object_name': 'Affiliation'},
            'average_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'behavior': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'conversion_to_price_ratio': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'equity_grant_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'equity_grant_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_director': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_officer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_something_else': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_ten_percent': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'latest_form_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'prior_average_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_conversion_to_price_ratio': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_share_equivalents_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_share_equivalents_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'reporting_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'share_equivalents_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'share_equivalents_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'})
        },
        u'sdapp.closeprice': {
            'Meta': {'object_name': 'ClosePrice'},
            'adj_close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'close_date': ('django.db.models.fields.DateField', [], {}),
            'close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'securitypricehist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'})
        },
        u'sdapp.discretionaryxnevent': {
            'Meta': {'object_name': 'DiscretionaryXnEvent'},
            'filedate': ('django.db.models.fields.DateField', [], {}),
            'form_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Form345Entry']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'person_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"}),
            'transaction_code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'xn_acq_disp_code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'xn_shares': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'xn_val': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'})
        },
        u'sdapp.form345entry': {
            'Meta': {'object_name': 'Form345Entry'},
            'adjustment_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'adjustment_factor': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '15', 'decimal_places': '4'}),
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Affiliation']", 'null': 'True'}),
            'conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'direct_or_indirect': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'entry_internal_id': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'filedatetime': ('django.db.models.fields.DateTimeField', [], {}),
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
            'issuer_cik_num': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'issuer_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'period_of_report': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'reported_shares_following_xn': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'reporting_owner_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']", 'null': 'True'}),
            'reporting_owner_cik_num': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'reporting_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'scrubbed_underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'sec_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'sec_url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'security_relationship'", 'null': 'True', 'to': u"orm['sdapp.Security']"}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'shares_following_xn': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'shares_following_xn_is_adjusted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_sec_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'supersededdt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'tenbfive_note': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transaction_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'transaction_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'transaction_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transaction_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_security': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'underlying_relationship'", 'null': 'True', 'to': u"orm['sdapp.Security']"}),
            'underlying_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'xn_acq_disp_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'xn_price_per_share': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'})
        },
        u'sdapp.ftpfilelist': {
            'Meta': {'object_name': 'FTPFileList'},
            'files': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'sdapp.fullform': {
            'Meta': {'object_name': 'FullForm'},
            'issuer_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'parsable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'save_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'sec_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'sdapp.issuercik': {
            'Meta': {'object_name': 'IssuerCIK'},
            'cik_num': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'})
        },
        u'sdapp.personholdingview': {
            'Meta': {'object_name': 'PersonHoldingView'},
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Affiliation']"}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'first_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intrinsic_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '4'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_close_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'last_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'max_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'min_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'most_recent_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'person_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'scrubbed_underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"}),
            'short_sec_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'underlying_close_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_shares_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'units_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_conversion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'wavg_xn_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        u'sdapp.personsignal': {
            'Meta': {'object_name': 'PersonSignal'},
            'average_price_sec_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'eq_annual_share_grants': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'first_file_date': ('django.db.models.fields.DateField', [], {}),
            'gross_signal_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_file_date': ('django.db.models.fields.DateField', [], {}),
            'net_signal_pct': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'net_signal_shares': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'net_signal_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'new': ('django.db.models.fields.BooleanField', [], {}),
            'only_security_1': ('django.db.models.fields.BooleanField', [], {}),
            'perf_after_detection': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'perf_period_days': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'preceding_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_holding_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'reporting_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'reporting_person_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'sec_price_hist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'}),
            'security_1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"}),
            'signal_detect_date': ('django.db.models.fields.DateField', [], {}),
            'signal_name': ('django.db.models.fields.CharField', [], {'default': "'ERROR'", 'max_length': '80'}),
            'significant': ('django.db.models.fields.BooleanField', [], {}),
            'subs_stock_period_days': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'transactions': ('django.db.models.fields.IntegerField', [], {'max_length': '15'})
        },
        u'sdapp.reportingperson': {
            'Meta': {'object_name': 'ReportingPerson'},
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'reporting_owner_cik_num': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'sdapp.reportingpersonatts': {
            'Meta': {'object_name': 'ReportingPersonAtts'},
            'activity_threshold': ('django.db.models.fields.BooleanField', [], {}),
            'b_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_10': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_120': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_150': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_30': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_60': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_90': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_win_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'buys': ('django.db.models.fields.IntegerField', [], {}),
            'exec_years': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reporting_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            's_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            's_win_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'sells': ('django.db.models.fields.IntegerField', [], {}),
            't_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            't_win_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'transactions': ('django.db.models.fields.IntegerField', [], {})
        },
        u'sdapp.secdayindex': {
            'Meta': {'object_name': 'SECDayIndex'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indexcontents': ('django.db.models.fields.TextField', [], {}),
            'indexname': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'sdapp.security': {
            'Meta': {'object_name': 'Security'},
            'conversion_multiple': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '15', 'decimal_places': '4'}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'scrubbed_underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'short_sec_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        u'sdapp.securitypricehist': {
            'Meta': {'object_name': 'SecurityPriceHist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']", 'null': 'True'}),
            'primary_ticker_sym': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']", 'null': 'True'}),
            'ticker_sym': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'sdapp.securityview': {
            'Meta': {'object_name': 'SecurityView'},
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'first_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intrinsic_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '4'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_close_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'last_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'max_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'min_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'most_recent_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'scrubbed_underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"}),
            'short_sec_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'underlying_close_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_shares_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'units_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_conversion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'wavg_xn_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        u'sdapp.sigdisplay': {
            'Meta': {'object_name': 'SigDisplay'},
            'active_insiders': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'average_holding_reduction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'avg_prior_trigger_performance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'bow_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'bow_first_perf_period_days': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'bow_first_post_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'bow_first_pre_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'bow_first_sig_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'bow_includes_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'bow_net_signal_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'bow_person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'bow_plural_insiders': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'bow_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'buyonweakness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cb_buy_xns': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'cb_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'cb_net_xn_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'cb_plural_insiders': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'cb_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'clusterbuy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clustersell': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cs_annual_grant_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'cs_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'cs_net_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'cs_net_xn_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'cs_plural_insiders': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'cs_sell_xns': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'cs_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'db_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'db_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'db_large_xn_size': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'db_person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'db_security_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'db_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'db_was_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'db_xn_pct_holdings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'db_xn_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'discretionarybuy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'discretionarysell': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ds_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ds_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ds_large_xn_size': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ds_person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ds_security_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ds_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ds_was_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ds_xn_pct_holdings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'ds_xn_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'historical_selling_rate_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'historical_selling_rate_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'historical_share_sell_rate_for_10b5_1_plans': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insiders_reduced_holdings': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_signal': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'number_of_recent_shares_sold': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'percent_change_in_shares_historical_to_recent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'percent_change_in_value_historical_to_recent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'percent_options_converted_to_expire_in_current_year': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'percent_shares_sold_under_10b5_1_plans': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'recent_share_sell_rate_for_10b5_1_plans': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'saleofall': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sec_price_hist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'}),
            'sell_price_trigger_detected': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sellers': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'sellonstrength': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signal_is_new': ('django.db.models.fields.BooleanField', [], {}),
            'soa_biggest_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'soa_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'soa_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'soa_inc_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'soa_people_count': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'soa_primary_affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Affiliation']", 'null': 'True'}),
            'soa_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'soa_total_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'sos_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'sos_first_perf_period_days': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'sos_first_post_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'sos_first_pre_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'sos_first_sig_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'sos_includes_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sos_net_signal_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'sos_person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'sos_plural_insiders': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sos_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'total_transactions': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'trigger_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'trigger_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'trigger_subs_performance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'value_of_recent_shares_sold': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'})
        },
        u'sdapp.splitoradjustmentevent': {
            'Meta': {'object_name': 'SplitOrAdjustmentEvent'},
            'adjustment_factor': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '4'}),
            'event_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"})
        },
        u'sdapp.transactionevent': {
            'Meta': {'object_name': 'TransactionEvent'},
            'end_holding_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'net_xn_pct': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'net_xn_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_182_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_274_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_365_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_456_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_91_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'period_end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'period_start': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'price_at_period_end': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'})
        },
        u'sdapp.watchedname': {
            'Meta': {'object_name': 'WatchedName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_signal_sent': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'securitypricehist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']"}),
            'ticker_sym': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'sdapp.yearlyreportingpersonatts': {
            'Meta': {'object_name': 'YearlyReportingPersonAtts'},
            'b_perf_10': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_120': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_150': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_180': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_30': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_60': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_90': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_win_rate_180': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'buys': ('django.db.models.fields.IntegerField', [], {}),
            'exec_years': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reporting_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['sdapp']