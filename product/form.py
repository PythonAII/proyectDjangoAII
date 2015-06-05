#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class Multiurls(forms.Form):
    urls = forms.CharField(label='Urls', widget=forms.Textarea)


class LoginForm(forms.Form):
    user = forms.CharField(label='user')
    password = forms.PasswordInput(label='password')