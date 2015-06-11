#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from AiiWebs.models import GameUser

class Multiurls(forms.Form):
    urls = forms.CharField(label='Urls', widget=forms.Textarea)


class LoginForm(forms.Form):
    user = forms.CharField(label=u'Usuario')
    password = forms.CharField(label=u'Contraseña', widget=forms.PasswordInput())


class UserRegisterForm(ModelForm):
    class Meta:
         model = GameUser
         fields = ['username', 'first_name', 'last_name', 'email', 'password', 'favorite_console']