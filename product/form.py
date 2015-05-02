#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class Multiurls(forms.Form):
    urls = forms.CharField(label='Urls', widget=forms.Textarea)
