#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class Multiurls(forms.Form):
    urls = forms.CharField(label='Urls', widget=forms.Textarea)


class LoginForm(forms.Form):
    user = forms.CharField(label=u'Usuario')
    password = forms.CharField(label=u'Contraseña', widget=forms.PasswordInput())