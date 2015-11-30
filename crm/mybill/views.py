#-*- coding=utf-8 -*-
from django.shortcuts import render

from django.views.generic import ListView

# Create your views here.
class BillIndexView(ListView):
    template_name = 'mybill/index.html'

    def get_queryset(self):
        return []

class BillDoView(ListView):
    def get_queryset(self):
        return []

    def get(self, request, *args, **kwargs):
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/%s.html' % method
        print method
        return render(request, self.template_name, {'form': ''})

    def post(self, request, *args, **kwargs):
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/%s.html' % method
        print method
        return render(request, self.template_name, {'form': ''})

class BillCategoryDoView(ListView):
    def get_queryset(self):
        return []

    def get(self, request, *args, **kwargs):
        print 'ff'
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/category_%s.html' % method
        return render(request, self.template_name, {'form': ''})
