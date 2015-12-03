#-*- coding=utf-8 -*-
import json
import datetime

from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
from django.db.models import Q

from django.views.generic import ListView
from .models import Account
from .models import AccountItem
from .models import AccountCategory

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


        ait_id = request.POST.get('id','')
        print 'ait_id', ait_id
        if not ait_id:
            #account=Account.objects.get_or_create(id=1,name=u'默认账户')
            account,created=Account.objects.get_or_create(id=1)
            instance = AccountItem(account=account)
            #instance.account_id = 1
            category_id = request.POST.get('categoryId','0')
            subcategory_id = request.POST.get('subCategoryId','0')
            if subcategory_id=='0':
                category, created = AccountCategory.objects.get_or_create(id=category_id, parent_id=None)
            else:
                category, created = AccountCategory.objects.get_or_create(id=subcategory_id, parent_id=category_id)
            instance.category = category
            instance.summary = request.POST.get('note','')
            #instance.summary = request.POST.get('subCategoryId','0')
            instance.amount = request.POST.get('amount','')
            if request.POST.get('recDate',''):
                instance.tx_date = datetime.datetime.strptime(request.POST.get('recDate',''),'%Y-%m-%d')
            else:
                instance.tx_date = datetime.datetime.now()
            #instance.summary = request.POST.get('categoryId','')
            instance.tx_type = request.POST.get('type','0')
            instance.save()
        else:
            account,created=Account.objects.get_or_create(id=1)
            instance = AccountItem.objects.get(id=ait_id, account=account)
            category_id = request.POST.get('categoryId','0')
            subcategory_id = request.POST.get('subCategoryId','0')
            if subcategory_id=='0':
                category, created = AccountCategory.objects.get_or_create(id=category_id, parent_id=None)
            else:
                category, created = AccountCategory.objects.get_or_create(id=subcategory_id, parent_id=category_id)
            instance.category = category
            instance.summary = request.POST.get('note','')
            #instance.summary = request.POST.get('subCategoryId','0')
            instance.amount = request.POST.get('amount','')
            if request.POST.get('recDate',''):
                instance.tx_date = datetime.datetime.strptime(request.POST.get('recDate',''),'%Y-%m-%d')
            else:
                instance.tx_date = datetime.datetime.now()
            #instance.summary = request.POST.get('categoryId','')
            instance.tx_type = request.POST.get('type','0')
            instance.save()
        year,month = instance.tx_date.year, instance.tx_date.month
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybill/bill.do?method=listmonth&strMonth=%s-%s' class='udl fbu'>该月账本</a>" % (year, month)
        return HttpResponse(json.dumps(response))

    def listmonth(self, request):
        if request.method == 'GET':
            strMonth=request.GET.get('strMonth','')
        else:
            strMonth=request.POST.get('strMonth','')

        if strMonth:
            year,month = map(int, strMonth.split('-'))
        else:
            now = datetime.datetime.now()
            year,month = now.year, now.month

        accountitem_list = AccountItem.objects.select_related('category').filter(tx_date__year=year, tx_date__month=month)
        last_balance = 0
        print type(accountitem_list)
        income = accountitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        outcome = accountitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        balance = last_balance + income - outcome
        return render(request, self.template_name, {'accountitem_list': accountitem_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            'year': year,
            'month': month,
            })

    def edit(self, request):
        pk = request.GET.get('id','1')
        accountitem = AccountItem.objects.get(pk=pk)
        income_category_list = AccountCategory.objects.filter(tx_type=1, parent=None).all()
        outcome_category_list = AccountCategory.objects.filter(tx_type=0, parent=None).all()
        return render(request,
                      self.template_name,
                      {
                          'accountitem': accountitem,
                          'income_category_list': income_category_list,
                          'outcome_category_list': outcome_category_list,
                      })

    def get(self, request, *args, **kwargs):
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/%s.html' % method
        print method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request)
        elif method == 'listmonth':
            return self.listmonth(request)
        elif method == 'edit':
            return self.edit(request)
        elif method == 'append':
            return self.append(request)
        elif method == 'list':
            return self.listall(request)
        elif method == 'listsort':
            return self.listsort(request)
        else:
            return render(request, self.template_name, {'form': ''})

    def post(self, request, *args, **kwargs):
        method=request.POST.get('method', '')
        if not method:
            method = request.GET.get('method', 'list')
        self.template_name = 'mybill/%s.html' % method
        print method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request)
        elif method == 'listmonth':
            return self.listmonth(request)
        elif method == 'edit':
            return self.edit(request)
        elif method == 'append':
            return self.append(request)
        elif method == 'list':
            return self.listall(request)
        elif method == 'listsort':
            return self.listsort(request)
        else:
            return render(request, self.template_name, {'form': ''})

    def append(self, request):
        income_category_list = AccountCategory.objects.filter(tx_type=1, parent=None).all()
        outcome_category_list = AccountCategory.objects.filter(tx_type=0, parent=None).all()

        return render(request,
                      self.template_name,
                      {
                      'servertime':datetime.datetime.now(),
                      'income_category_list': income_category_list,
                      'outcome_category_list': outcome_category_list,
                      })

    def listall(self, request):
        strMonth=request.GET.get('strMonth','')
        if strMonth:
            year,month = map(int, strMonth.split('-'))
        else:
            now = datetime.datetime.now()
            year,month = now.year, now.month

        accountitem_list = AccountItem.objects.select_related('category').filter(tx_date__year=year, tx_date__month=month)
        last_balance = 0
        print year, month
        print type(accountitem_list)
        income = accountitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        outcome = accountitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        balance = last_balance + income - outcome
        return render(request, self.template_name, {'accountitem_list': accountitem_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            'year': year,
            'month': month,
            })

    def listsort(self, request):
        '''
        method:listsort
        type:0
        categoryId:50529762
        subCategoryId:0
        fromRecDate:
        toRecDate:
        '''
        fromRecDate=request.POST.get('fromRecDate','')
        toRecDate=request.POST.get('toRecDate','')
        tx_type=request.POST.get('type','')
        categoryId=request.POST.get('categoryId','0')
        subCategoryId=request.POST.get('subCategoryId','0')
        strMonth=request.POST.get('strMonth','')

        categoryId = int(categoryId)
        subCategoryId = int(subCategoryId)
        category_id = categoryId

        if strMonth:
            year,month = map(int, strMonth.split('-'))
        else:
            now = datetime.datetime.now()
            year,month = now.year, now.month

        if request.method == 'GET':
            income_category_list = AccountCategory.objects.filter(tx_type=1, parent=None).all()
            outcome_category_list = AccountCategory.objects.filter(tx_type=0, parent=None).all()
            return render(request, self.template_name, {'accountitem_list': [],
                'income': 0,
                'outcome': 0,
                'balance': 0,
                'year': year,
                'month': month,
                'category_id': category_id,
                'income_category_list': income_category_list,
                'outcome_category_list': outcome_category_list,
                })

        if fromRecDate:
            print datetime.datetime.strptime(toRecDate, '%Y-%m-%d')
            accountitem_list = AccountItem.objects.select_related('category').filter(tx_date__gte=datetime.datetime.strptime(fromRecDate, '%Y-%m-%d'))
            if toRecDate:
                print '1',toRecDate
                print datetime.datetime.strptime(toRecDate, '%Y-%m-%d')
                accountitem_list= accountitem_list.filter(tx_date__lte=datetime.datetime.strptime(toRecDate, '%Y-%m-%d'))
        else:
            accountitem_list = AccountItem.objects.select_related('category')
            if toRecDate:
                print '2',toRecDate
                print datetime.datetime.strptime(toRecDate, '%Y-%m-%d')
                accountitem_list= accountitem_list.filter(tx_date__lte=datetime.datetime.strptime(toRecDate, '%Y-%m-%d'))

        if tx_type:
            accountitem_list= accountitem_list.filter(tx_type = tx_type)

        if subCategoryId:
            #如果子分类不为空, 即选中子分类, 就只过滤子分类
            accountitem_list= accountitem_list.filter(category__id = subCategoryId)
            category_id = subCategoryId
        else:
            #否则过滤父分类和所有的子分类
            if categoryId:
                subCategoryIds= list(AccountCategory.objects.filter(parent__id=categoryId).values_list('id', flat=True).all())
                print 'subCategoryIds', subCategoryIds
                subCategoryIds.insert(0, categoryId)
                accountitem_list= accountitem_list.filter(category__id__in = subCategoryIds)

        last_balance = 0
        print year, month
        print type(accountitem_list)
        income = accountitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        outcome = accountitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        balance = last_balance + income - outcome
        print self.template_name, '00000000000000000000000000000000000000000000000000'

        income_category_list = AccountCategory.objects.filter(tx_type=1, parent=None).all()
        outcome_category_list = AccountCategory.objects.filter(tx_type=0, parent=None).all()
        print outcome_category_list
        return render(request, self.template_name, {'accountitem_list': accountitem_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            'year': year,
            'month': month,
            'category_id': category_id,
            'income_category_list': income_category_list,
            'outcome_category_list': outcome_category_list,
            })

class BillCategoryDoView(ListView):
    def get_queryset(self):
        return []

    def get(self, request, *args, **kwargs):
        print 'ff'
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/category_%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request)
        elif method == 'list':
            return self.listall(request)
        else:
            return render(request, self.template_name, {'form': ''})

    def post(self, request, *args, **kwargs):
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/category_%s.html' % method
        print method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request)
        return render(request, self.template_name, {'form': ''})

    def addOrUpdate(self, request, *args, **kwargs):
        '''
        {"result":
            {
                "success":"true",
                "message":"已经成功保存收支项目信息!",
                "totalCount":"0",
                "data":{
                    "@class":"categoryform",
                    "id":"12345",
                    "categoryName":"租金",
                    "parentId":"0",
                    "type":"1"
                },
                "pageIndex":"0",
                "pageSize":"100"
            }
        }
        '''
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybill/bill.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本</a>"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'

        category_id = request.POST.get('id','')
        print 'category_id', category_id
        if category_id=='0':
            name = request.POST.get('categoryName','无名')
            tx_type = request.POST.get('type','0')
            parent_id = request.POST.get('parentId','0')
            if parent_id=='0':
                category, created = AccountCategory.objects.get_or_create(parent_id=None, name=name, tx_type=tx_type)
            else:
                category, created = AccountCategory.objects.get_or_create(parent_id=parent_id, name=name, tx_type=tx_type)
        else:
            print 'category_id', category_id
            category=AccountCategory.objects.get(id=category_id)
            if parent_id=='0':
              category.parent_id = None
              category.tx_type = tx_type
              category.name = name
              category.save()
            else:
              category.parent_id = parent_id
              category.tx_type = tx_type
              category.name = name
              category.save()
        return HttpResponse(json.dumps(response))

    def listall(self, request, *args, **kwargs):
        income_category_list = AccountCategory.objects.filter(tx_type=1, parent=None).all()
        outcome_category_list = AccountCategory.objects.filter(tx_type=0, parent=None).all()

        return render(request, self.template_name, {
            'income_category_list': income_category_list,
            'outcome_category_list': outcome_category_list,
            })
