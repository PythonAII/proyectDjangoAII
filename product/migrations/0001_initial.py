# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PricesGame'
        db.create_table('product_pricesgame', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shop', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('stock', self.gf('django.db.models.fields.IntegerField')()),
            ('plataform', self.gf('django.db.models.fields.IntegerField')(max_length=200)),
            ('price_old', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price_now', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('gift', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
        ))
        db.send_create_signal('product', ['PricesGame'])

        # Adding model 'GameImage'
        db.create_table('product_gameimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('product', ['GameImage'])

        # Adding model 'GameCategory'
        db.create_table('product_gamecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.IntegerField')(max_length=400)),
        ))
        db.send_create_signal('product', ['GameCategory'])

        # Adding model 'GamePegi'
        db.create_table('product_gamepegi', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.IntegerField')(max_length=10000, null=True)),
        ))
        db.send_create_signal('product', ['GamePegi'])

        # Adding model 'Game'
        db.create_table('product_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=3000)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('imagen', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imagen_main', null=True, to=orm['product.GameImage'])),
        ))
        db.send_create_signal('product', ['Game'])

        # Adding M2M table for field category on 'Game'
        db.create_table('product_game_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm['product.game'], null=False)),
            ('gamecategory', models.ForeignKey(orm['product.gamecategory'], null=False))
        ))
        db.create_unique('product_game_category', ['game_id', 'gamecategory_id'])

        # Adding M2M table for field prices on 'Game'
        db.create_table('product_game_prices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm['product.game'], null=False)),
            ('pricesgame', models.ForeignKey(orm['product.pricesgame'], null=False))
        ))
        db.create_unique('product_game_prices', ['game_id', 'pricesgame_id'])

        # Adding M2M table for field pegi on 'Game'
        db.create_table('product_game_pegi', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm['product.game'], null=False)),
            ('gamepegi', models.ForeignKey(orm['product.gamepegi'], null=False))
        ))
        db.create_unique('product_game_pegi', ['game_id', 'gamepegi_id'])

        # Adding M2M table for field imagenes on 'Game'
        db.create_table('product_game_imagenes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm['product.game'], null=False)),
            ('gameimage', models.ForeignKey(orm['product.gameimage'], null=False))
        ))
        db.create_unique('product_game_imagenes', ['game_id', 'gameimage_id'])


    def backwards(self, orm):
        # Deleting model 'PricesGame'
        db.delete_table('product_pricesgame')

        # Deleting model 'GameImage'
        db.delete_table('product_gameimage')

        # Deleting model 'GameCategory'
        db.delete_table('product_gamecategory')

        # Deleting model 'GamePegi'
        db.delete_table('product_gamepegi')

        # Deleting model 'Game'
        db.delete_table('product_game')

        # Removing M2M table for field category on 'Game'
        db.delete_table('product_game_category')

        # Removing M2M table for field prices on 'Game'
        db.delete_table('product_game_prices')

        # Removing M2M table for field pegi on 'Game'
        db.delete_table('product_game_pegi')

        # Removing M2M table for field imagenes on 'Game'
        db.delete_table('product_game_imagenes')


    models = {
        'product.game': {
            'Meta': {'ordering': "['name', 'category__name', 'release_date']", 'object_name': 'Game'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['product.GameCategory']", 'max_length': '400', 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imagen_main'", 'null': 'True', 'to': "orm['product.GameImage']"}),
            'imagenes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['product.GameImage']", 'null': 'True', 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pegi': ('django.db.models.fields.related.ManyToManyField', [], {'max_length': '10000', 'to': "orm['product.GamePegi']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
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
            'plataform': ('django.db.models.fields.IntegerField', [], {'max_length': '200'}),
            'price_now': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_old': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'shop': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'stock': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['product']