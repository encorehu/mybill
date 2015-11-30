#-*- coding=utf-8 -*-
from django.shortcuts import render

from django.views.generic import ListView

# Create your views here.
class BillIndexView(ListView):
    template_name = 'mybill/index.html'

    def get_queryset(self):
        return []
