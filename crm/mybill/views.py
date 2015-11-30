#-*- coding=utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import AccountItem

# Create your views here.
class BillIndexView(ListView):
    template_name = 'mybill/index.html'

    def get_queryset(self):
        return []

class BillDoView(ListView):
    def get_queryset(self):
        return []

    def addOrUpdate(self, request):
        '''
        {"result":
            {
                "success":"true",
                "message":"新增记录成功，点击这里查看<a href='\/mybill\/bill.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本<\/a>",
                "totalCount":"0",
                "pageIndex":"0",
                "pageSize":"100"
            }
        }
'''
        print request.POST
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybill/bill.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本</a>"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'

        ait = AccountItem()
        ait.summary = request.POST.get('note','')
        ait.summary = request.POST.get('id','')
        ait.summary = request.POST.get('subCategoryId','0')
        ait.summary = request.POST.get('amount','')
        ait.summary = request.POST.get('recDate','')
        ait.summary = request.POST.get('categoryId','')
        ait.summary = request.POST.get('type','0')

        return HttpResponse(json.dumps(response))

    def get(self, request, *args, **kwargs):
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/%s.html' % method
        print method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request)
        else:
            return render(request, self.template_name, {'form': ''})

    def post(self, request, *args, **kwargs):
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/%s.html' % method
        print method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request)
        return render(request, self.template_name, {'form': ''})

class BillCategoryDoView(ListView):
    def get_queryset(self):
        return []

    def get(self, request, *args, **kwargs):
        print 'ff'
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/category_%s.html' % method
        return render(request, self.template_name, {'form': ''})
