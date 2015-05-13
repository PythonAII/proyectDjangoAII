# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PricesGame.stock'
        db.alter_column('product_pricesgame', 'stock', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):

        # Changing field 'PricesGame.stock'
        db.alter_column('product_pricesgame', 'stock', self.gf('django.db.models.fields.TextField')())

    models = {
        'product.game': {
            'Meta': {'ordering': "['name', 'category__name', 'release_date']", 'object_name': 'Game'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['product.GameCategory']", 'max_length': '400', 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imagen_main'", 'to': "orm['product.GameImage']"}),
            'imagenes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['product.GameImage']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pegi': ('django.db.models.fields.related.ManyToManyField', [], {'max_length': '10000', 'to': "orm['product.GamePegi']", 'null': 'True', 'symmetrical': 'False'}),
            'prices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['product.PricesGame']", 'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'product.gamecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'GameCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.IntegerField', [], {'max_length': '400'})
        },
        'product.gameimage': {
            'Meta': {'object_name': 'GameImage'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'product.gamepegi': {
            'Meta': {'object_name': 'GamePegi'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.IntegerField', [], {'max_length': '10000', 'null': 'True'})
        },
        'product.pricesgame': {
            'Meta': {'ordering': "['shop', 'price_now', 'price_old']", 'object_name': 'PricesGame'},
            'gift': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plataform': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price_now': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_old': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'shop': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'stock': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['product']