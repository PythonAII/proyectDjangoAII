# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameUser'
        db.create_table('AiiWebs_gameuser', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('favorite_console', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('AiiWebs', ['GameUser'])

        # Adding M2M table for field visited_games on 'GameUser'
        db.create_table('AiiWebs_gameuser_visited_games', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gameuser', models.ForeignKey(orm['AiiWebs.gameuser'], null=False)),
            ('game', models.ForeignKey(orm['product.game'], null=False))
        ))
        db.create_unique('AiiWebs_gameuser_visited_games', ['gameuser_id', 'game_id'])

        # Adding M2M table for field visited_links on 'GameUser'
        db.create_table('AiiWebs_gameuser_visited_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gameuser', models.ForeignKey(orm['AiiWebs.gameuser'], null=False)),
            ('pricesgame', models.ForeignKey(orm['product.pricesgame'], null=False))
        ))
        db.create_unique('AiiWebs_gameuser_visited_links', ['gameuser_id', 'pricesgame_id'])

        # Adding M2M table for field favorite_games on 'GameUser'
        db.create_table('AiiWebs_gameuser_favorite_games', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gameuser', models.ForeignKey(orm['AiiWebs.gameuser'], null=False)),
            ('game', models.ForeignKey(orm['product.game'], null=False))
        ))
        db.create_unique('AiiWebs_gameuser_favorite_games', ['gameuser_id', 'game_id'])


    def backwards(self, orm):
        # Deleting model 'GameUser'
        db.delete_table('AiiWebs_gameuser')

        # Removing M2M table for field visited_games on 'GameUser'
        db.delete_table('AiiWebs_gameuser_visited_games')

        # Removing M2M table for field visited_links on 'GameUser'
        db.delete_table('AiiWebs_gameuser_visited_links')

        # Removing M2M table for field favorite_games on 'GameUser'
        db.delete_table('AiiWebs_gameuser_favorite_games')


    models = {
        'AiiWebs.gameuser': {
            'Meta': {'ordering': "['username', 'date_joined', 'favorite_console']", 'object_name': 'GameUser', '_ormbases': ['auth.User']},
            'favorite_console': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'favorite_games': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'Juegos Favoritos'", 'null': 'True', 'to': "orm['product.Game']"}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'visited_games': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'Juegos Visitados'", 'null': 'True', 'to': "orm['product.Game']"}),
            'visited_links': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['product.PricesGame']", 'symmetrical': 'False'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'stock': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['AiiWebs']