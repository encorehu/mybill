#-*- coding=utf-8 -*-
import os
import json
import datetime

import StringIO

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
from django.db.models import Q
from django.db import transaction
from django.db.models import Min,Max

from django.views.generic import ListView
from django.conf import settings
from .models import Account
from .models import AccountItem
from .models import AccountCategory
from .models import Transaction
from .models import TX_TYPE

from django.core.files.base import ContentFile

def file_download(request, filename, displayname):
    filepath = filename
    if isinstance(filename, str):
        wrapper = ContentFile(open(filepath,'rb').read())
    else:
        if hasattr(filename, 'read'):
            wrapper = ContentFile(filename.read())
        else:
            raise Http404(u"File does not exists!")
    response = HttpResponse(wrapper, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = (u'attachment; filename=%s' % displayname).encode('utf-8')
    return response

# Create your views here.
class BillIndexView(ListView):
    template_name = 'mybill/index.html'

    def get_queryset(self):
        return []

    def get(self, request, *args, **kwargs):
        total_balance = Account.objects.aggregate(combined_balance=Coalesce(Sum('balance'), V(0)))['combined_balance']
        return render(request, self.template_name,
                    {
                        'account_list': Account.objects.all(),
                        'total_balance':total_balance,
                    })

class BillDoView(ListView):
    def get_queryset(self):
        return []

    def addOrUpdate(self, request, *args, **kwargs):
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
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybill/bill.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本</a>"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'


        ait_id = request.POST.get('id','')
        if not ait_id:
            #account=Account.objects.get_or_create(id=1,name=u'默认账户')
            instance = AccountItem(account=account)
            #instance.account_id = 1
            category_id = request.POST.get('categoryId','0')
            subcategory_id = request.POST.get('subCategoryId','0')
            if subcategory_id=='0':
                category, created = AccountCategory.objects.get_or_create(id=category_id, parent_id=None)
            else:
                category, created = AccountCategory.objects.get_or_create(id=subcategory_id, parent_id=category_id)
            instance.category = category
            instance.title = request.POST.get('title','')
            instance.summary = request.POST.get('note','')
            instance.amount = request.POST.get('amount','')
            if request.POST.get('recDate',''):
                instance.tx_date = datetime.datetime.strptime(request.POST.get('recDate',''),'%Y-%m-%d')
            else:
                instance.tx_date = datetime.datetime.now()
            instance.tx_type = request.POST.get('type','0')
            instance.save()
        else:
            instance = AccountItem.objects.get(id=ait_id, account=account)
            category_id = request.POST.get('categoryId','0')
            subcategory_id = request.POST.get('subCategoryId','0')
            if subcategory_id=='0':
                category, created = AccountCategory.objects.get_or_create(id=category_id, parent_id=None)
            else:
                category, created = AccountCategory.objects.get_or_create(id=subcategory_id, parent_id=category_id)
            instance.category = category
            instance.title = request.POST.get('title','')
            instance.summary = request.POST.get('note','')
            instance.amount = request.POST.get('amount','')
            if request.POST.get('recDate',''):
                instance.tx_date = datetime.datetime.strptime(request.POST.get('recDate',''),'%Y-%m-%d')
            else:
                instance.tx_date = datetime.datetime.now()
            instance.tx_type = request.POST.get('type','0')
            instance.save()
        year,month = instance.tx_date.year, instance.tx_date.month
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybill/bill.do?accountid=%s&method=listmonth&strMonth=%s-%s' class='udl fbu'>该月账本</a>" % (account.id, year, month)
        return HttpResponse(json.dumps(response))

    def listmonth(self, request, *args, **kwargs):
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        if request.method == 'GET':
            strMonth=request.GET.get('strMonth','')
        else:
            strMonth=request.POST.get('strMonth','')

        if strMonth:
            year,month = map(int, strMonth.split('-'))
        else:
            now = datetime.datetime.now()
            year,month = now.year, now.month

        accountitem_list = AccountItem.objects.select_related('category').filter(account=account, tx_date__year=year, tx_date__month=month)
        last_balance = 0
        income = accountitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        outcome = accountitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        balance = last_balance + income - outcome
        year_list=[x for x in xrange(year+1, year-3, -1)]
        return render(request, self.template_name, {
            'account': account,
            'account_list': account_list,
            'accountitem_list': accountitem_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            'year': year,
            'year_list': year_list,
            'month_list': [x for x in xrange(13)],
            'month': month,
            })

    def listyear(self, request, *args, **kwargs):
        if request.method == 'GET':
            strYear=request.GET.get('strYear','')
        else:
            strYear=request.POST.get('strYear','')

        if strYear:
            year =  int(strYear)
        else:
            now = datetime.datetime.now()
            year = now.year

        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        accountitem_list = AccountItem.objects.select_related('category').filter(account=account, tx_date__year=year)
        last_balance = 0
        income = accountitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        outcome = accountitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        balance = last_balance + income - outcome
        year_list=[x for x in xrange(year+1, year-3, -1)]
        return render(request, self.template_name, {
            'account': account,
            'account_list': account_list,
            'accountitem_list': accountitem_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            'year': year,
            'year_list': year_list,
            })

    def edit(self, request, *args, **kwargs):
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        pk = request.GET.get('id',None)
        try:
            accountitem = AccountItem.objects.get(pk=pk)
        except AccountItem.DoesNotExist:
            return Http404()
        income_category_list = AccountCategory.objects.filter(account=account, tx_type=1, parent=None).all()
        outcome_category_list = AccountCategory.objects.filter(account=account, tx_type=0, parent=None).all()
        return render(request,
                      self.template_name,
                      {
                          'account':account,
                          'account_list':account_list,
                          'accountitem': accountitem,
                          'income_category_list': income_category_list,
                          'outcome_category_list': outcome_category_list,
                      })

    def get(self, request, *args, **kwargs):
        accountid = request.GET.get('accountid', None)
        if not accountid:
            raise Http404(u"Account 不存在")
        try:
            account = Account.objects.get(id=accountid)
        except Account.DoesNotExist:
            raise Http404(u"Account 不存在")
        account_list = Account.objects.all()
        kwargs.update({
            'account':account,
            'account_list':account_list,
        })
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request, *args, **kwargs)
        elif method == 'listyear':
            return self.listyear(request, *args, **kwargs)
        elif method == 'listmonth':
            return self.listmonth(request, *args, **kwargs)
        elif method == 'edit':
            return self.edit(request, *args, **kwargs)
        elif method == 'append':
            return self.append(request, *args, **kwargs)
        elif method == 'list':
            return self.listall(request, *args, **kwargs)
        elif method == 'listsort':
            return self.listsort(request, *args, **kwargs)
        elif method == 'export':
            return self.export(request, *args, **kwargs)
        elif method == 'exportyear':
            return self.exportyear(request, *args, **kwargs)
        elif method == 'exportall':
            return self.exportall(request, *args, **kwargs)
        elif method == 'transfer':
            return self.transfer(request, *args, **kwargs)
        else:
            kwargs.update(form=None)
            return render(request, self.template_name, kwargs)

    def post(self, request, *args, **kwargs):
        accountid = request.GET.get('accountid', None)
        try:
            account = Account.objects.get(id=accountid)
        except Account.DoesNotExist:
            raise Http404("Account does not exist")
        account_list = Account.objects.all()
        kwargs.update({
            'account':account,
            'account_list':account_list,
        })
        method=request.POST.get('method', '')
        if not method:
            method = request.GET.get('method', 'list')
        self.template_name = 'mybill/%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request, *args, **kwargs)
        elif method == 'listmonth':
            return self.listmonth(request, *args, **kwargs)
        elif method == 'listyear':
            return self.listyear(request, *args, **kwargs)
        elif method == 'edit':
            return self.edit(request, *args, **kwargs)
        elif method == 'append':
            return self.append(request, *args, **kwargs)
        elif method == 'list':
            return self.listall(request, *args, **kwargs)
        elif method == 'listsort':
            return self.listsort(request, *args, **kwargs)
        elif method == 'del':
            return self.delete(request, *args, **kwargs)
        elif method == 'transfer':
            return self.transfer(request, *args, **kwargs)
        else:
            return render(request, self.template_name, {'form': ''})

    def append(self, request, *args, **kwargs):
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        income_category_list = AccountCategory.objects.filter(account=account, tx_type=1, parent=None).all()
        outcome_category_list = AccountCategory.objects.filter(account=account, tx_type=0, parent=None).all()

        return render(request,
                      self.template_name,
                      {
                      'account':account,
                      'account_list':account_list,
                      'servertime':datetime.datetime.now(),
                      'income_category_list': income_category_list,
                      'outcome_category_list': outcome_category_list,
                      })

    def listall(self, request, *args, **kwargs):
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        accountitem_list = AccountItem.objects.select_related('category').filter(account=account)
        last_balance = 0
        income = accountitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        outcome = accountitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        balance = last_balance + income - outcome
        account.balance = balance
        account.save()
        return render(request, self.template_name, {
            'account': account,
            'account_list': account_list,
            'accountitem_list': accountitem_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            })

    def listsort(self, request, *args, **kwargs):
        '''
        method:listsort
        type:0
        categoryId:50529762
        subCategoryId:0
        fromRecDate:
        toRecDate:
        '''
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
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
            income_category_list = AccountCategory.objects.filter(account=account, tx_type=1, parent=None).all()
            outcome_category_list = AccountCategory.objects.filter(account=account, tx_type=0, parent=None).all()
            fromRecDate = None #datetime.datetime(year=year, month=month, day=1)
            toRecDate = datetime.datetime.now()
            return render(request, self.template_name, {
                'account': account,
                'account_list': account_list,
                'accountitem_list': [],
                'income': 0,
                'outcome': 0,
                'balance': 0,
                'year': year,
                'month': month,
                'fromRecDate':fromRecDate,
                'toRecDate':toRecDate,
                'category_id': category_id,
                'income_category_list': income_category_list,
                'outcome_category_list': outcome_category_list,
                })

        if fromRecDate:
            fromRecDate = datetime.datetime.strptime(fromRecDate, '%Y-%m-%d')
            accountitem_list = AccountItem.objects.select_related('category').filter(tx_date__gte=fromRecDate)
            if toRecDate:
                toRecDate=datetime.datetime.strptime(toRecDate, '%Y-%m-%d')
                accountitem_list= accountitem_list.filter(tx_date__lte=toRecDate)
            else:
                toRecDate=datetime.datetime.now()
        else:
            fromRecDate = None #datetime.datetime(year=year, month=month, day=1)
            accountitem_list = AccountItem.objects.select_related('category')
            if toRecDate:
                toRecDate = datetime.datetime.strptime(toRecDate, '%Y-%m-%d')
                accountitem_list = accountitem_list.filter(tx_date__lte=toRecDate)
            else:
                toRecDate = datetime.datetime.now()

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
                subCategoryIds.insert(0, categoryId)
                accountitem_list= accountitem_list.filter(category__id__in = subCategoryIds)

        last_balance = 0
        income = accountitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        outcome = accountitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        balance = last_balance + income - outcome

        income_category_list = AccountCategory.objects.filter(account=account, tx_type=1, parent=None).all()
        outcome_category_list = AccountCategory.objects.filter(account=account, tx_type=0, parent=None).all()
        return render(request, self.template_name, {
            'account':account,
            'account_list': account_list,
            'accountitem_list': accountitem_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            'year': year,
            'month': month,
            'fromRecDate':fromRecDate,
            'toRecDate':toRecDate,
            'category_id': category_id,
            'income_category_list': income_category_list,
            'outcome_category_list': outcome_category_list,
            })

    def export(self, request, *args, **kwargs):
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        strMonth = request.GET.get('strMonth','')
        if strMonth:
            year,month = map(int, strMonth.split('-'))
        else:
            now = datetime.datetime.now()
            year,month = now.year, now.month
        accountitem_list = AccountItem.objects.select_related('category').filter(account=account, tx_date__year=year, tx_date__lt=datetime.datetime(year,month,1))
        import xlsxwriter
        output = StringIO.StringIO()

        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 16)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 26)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 12)

        # Add a bold format to use to highlight cells.
        #bold = workbook.add_format({'bold': True})
        format1 = workbook.add_format()
        format1.set_border(1)

        worksheet.write('A1', u'收支项目', format1)
        worksheet.write('B1', u'日期', format1)
        worksheet.write('C1', u'摘要', format1)
        worksheet.write('D1', u'收入金额', format1)
        worksheet.write('E1', u'支出金额', format1)
        worksheet.write('F1', u'余额', format1)




        last_month = month-1
        if last_month==0:
          year_of_last_month = year-1
          last_month = 12
        else:
          year_of_last_month = year
        accountitem_list = AccountItem.objects.select_related('category').filter(account=account, tx_date__year=year, tx_date__lt=datetime.datetime(year,month,1))
        #accountitem_list = AccountItem.objects.select_related('category').filter(tx_date__year=year_of_last_month, tx_date__month=month)
        last_balance = 0
        last_month_income = accountitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        last_month_outcome = accountitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        last_month_balance = last_balance + last_month_income - last_month_outcome
        worksheet.write('A2', u'期初余额', format1)
        worksheet.write('B2', u'%s-%02d-%02d'  % (year, month, 1), format1)
        worksheet.write('C2', u'上月底余额', format1)
        worksheet.write('D2', u'', format1)
        worksheet.write('E2', u'', format1)
        worksheet.write('F2', last_month_balance, format1)

        last_balance=last_month_balance
        balance=0
        total_income = 0
        total_outcome = 0
        start_row=3 #start from 3d row, index from 1
        i=0
        accountitem_list = AccountItem.objects.select_related('category').filter(account=account, tx_date__year=year_of_last_month, tx_date__month=month)
        for i, item  in enumerate(accountitem_list):
            category = item.category.name if item.category else ''
            worksheet.write('A%s' % (i+start_row), u' %s %s' % ('+' if item.tx_type else '-', category), format1)
            worksheet.write('B%s' % (i+start_row), item.tx_date.strftime('%Y-%m-%d'), format1)
            worksheet.write('C%s' % (i+start_row), item.summary_display(), format1)
            if item.tx_type:
                worksheet.write('D%s' % (i+start_row), item.amount, format1)
                worksheet.write('E%s' % (i+start_row), None, format1)
                income = item.amount
                outcome = 0
                total_income = total_income + income
            else:
                worksheet.write('D%s' % (i+start_row), None, format1)
                worksheet.write('E%s' % (i+start_row), item.amount, format1)
                income = 0
                outcome = item.amount
                total_outcome = total_outcome + outcome
            balance = last_balance+income-outcome
            worksheet.write('F%s' % (i+start_row), balance, format1)
            last_balance= balance

        if i >0:
            worksheet.write('C%s' % (i+start_row+1), u'合计')
            worksheet.write('D%s' % (i+start_row+1), total_income)
            worksheet.write('E%s' % (i+start_row+1), total_outcome)
            worksheet.write('F%s' % (i+start_row+1), balance)

        left = u'&L\n单位:%s' % settings.ORGNAME
        center = u'&C%s%s年%s月日记账' % (account, year, month)
        right = '' #u'&R\n打印日期:%s' % datetime.datetime.now().strftime('%Y-%m-%d')
        worksheet.set_header(left+center+right, margin=0.6)
        worksheet.set_footer('&C&P/&N', margin=0.5)
        worksheet.set_margins(top=1)

        worksheet.repeat_rows(0)
        #worksheet.hide_gridlines(0)

        workbook.set_properties({
            'title':    u'%s%s年%s月日记账' % (account, year, month),
            'subject':  u'日记账',
            'author':   settings.AUTHOR,
            'manager':  settings.MANAGER,
            'company':  settings.ORGNAME,
            'category': u'财务日记账',
            'keywords': u'财务日记账',
            'comments': u'本日记账由系统自动导出',
            'status':   'Quo',
        })




        workbook.close()
        output.seek(0)

        displayname=  u'%s%s年%s月.xlsx' % (account, year,month)
        return file_download(request, output, displayname)

    def exportyear(self, request, *args, **kwargs):
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        strMonth = request.GET.get('strMonth','')
        if strMonth:
            tmp=strMonth.split('-')
            if len(tmp)==1:
                year=int(tmp[0])
                month=None
            elif len(tmp)==2:
                year,month = map(int, strMonth.split('-'))
            else:
                now = datetime.datetime.now()
                year,month = now.year, now.month
        else:
            now = datetime.datetime.now()
            year,month = now.year, now.month
        accountitem_list = AccountItem.objects.select_related('category').filter(account=account, tx_date__year=year)
        import xlsxwriter
        # Create an new Excel file and add a worksheet.
        output = StringIO.StringIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 16)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 26)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 12)

        # Add a bold format to use to highlight cells.
        #bold = workbook.add_format({'bold': True})
        format1 = workbook.add_format()
        format1.set_border(1)

        worksheet.write('A1', u'收支项目', format1)
        worksheet.write('B1', u'日期', format1)
        worksheet.write('C1', u'摘要', format1)
        worksheet.write('D1', u'收入金额', format1)
        worksheet.write('E1', u'支出金额', format1)
        worksheet.write('F1', u'余额', format1)




        year_of_last_month = year-1
        accountitem_list = AccountItem.objects.select_related('category').filter(account=account, tx_date__lt=datetime.datetime(year,1,1))
        #accountitem_list = AccountItem.objects.select_related('category').filter(tx_date__year=year_of_last_month, tx_date__month=month)
        last_balance = 0
        last_month_income = accountitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        last_month_outcome = accountitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        last_month_balance = last_balance + last_month_income - last_month_outcome
        worksheet.write('A2', u'期初余额', format1)
        worksheet.write('B2', u'%s-01-%02d'  % (year, 1), format1)
        worksheet.write('C2', u'上月底余额', format1)
        worksheet.write('D2', u'', format1)
        worksheet.write('E2', u'', format1)
        worksheet.write('F2', last_month_balance, format1)

        last_balance=0
        balance=0
        total_income = 0
        total_outcome = 0
        start_row=3 #start from 3d row, index from 1
        i=0
        accountitem_list = AccountItem.objects.select_related('category').filter(account=account, tx_date__year=year)
        for i, item  in enumerate(accountitem_list):
            category = item.category.name if item.category else ''
            worksheet.write('A%s' % (i+start_row), u' %s %s' % ('+' if item.tx_type else '-', category), format1)
            worksheet.write('B%s' % (i+start_row), item.tx_date.strftime('%Y-%m-%d'), format1)
            worksheet.write('C%s' % (i+start_row), item.summary_display(), format1)
            if item.tx_type:
                worksheet.write('D%s' % (i+start_row), item.amount, format1)
                worksheet.write('E%s' % (i+start_row), None, format1)
                income = item.amount
                outcome = 0
                total_income = total_income + income
            else:
                worksheet.write('D%s' % (i+start_row), None, format1)
                worksheet.write('E%s' % (i+start_row), item.amount, format1)
                income = 0
                outcome = item.amount
                total_outcome = total_outcome + outcome
            balance = last_balance+income-outcome
            worksheet.write('F%s' % (i+start_row), balance, format1)
            last_balance= balance

        if i >0:
            worksheet.write('A%s' % (i+start_row+1), u'合计')
            worksheet.write('D%s' % (i+start_row+1), total_income)
            worksheet.write('E%s' % (i+start_row+1), total_outcome)
            worksheet.write('F%s' % (i+start_row+1), balance)

        left = u'&L\n单位:%s' % settings.ORGNAME
        center = u'&C%s%s年日记账' % (account, year, )
        right = '' #u'&R\n打印日期:%s' % datetime.datetime.now().strftime('%Y-%m-%d')
        worksheet.set_header(left+center+right, margin=0.6)
        worksheet.set_footer('&C&P/&N', margin=0.5)
        worksheet.set_margins(top=1)

        worksheet.repeat_rows(0)
        #worksheet.hide_gridlines(0)

        workbook.set_properties({
            'title':    u'%s%s年日记账' % (account, year, ),
            'subject':  u'日记账',
            'author':   settings.AUTHOR,
            'manager':  settings.MANAGER,
            'company':  settings.ORGNAME,
            'category': u'财务日记账',
            'keywords': u'财务日记账',
            'comments': u'本日记账由系统自动导出',
            'status':   'Quo',
        })

        workbook.close()
        output.seek(0)

        displayname=  u'%s日记账%s年.xlsx' % (account, year, )
        return file_download(request, output, displayname)

    def exportall(self, request, *args, **kwargs):
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')


        filename = u'%s.xlsx' % account

        import xlsxwriter
        output = StringIO.StringIO()
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 16)
        worksheet.set_column('C:C', 26)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 12)

        # Add a bold format to use to highlight cells.
        #bold = workbook.add_format({'bold': True})
        format1 = workbook.add_format()
        format1.set_border(1)

        worksheet.write('A1', u'日期', format1)
        worksheet.write('B1', u'收支项目', format1)
        worksheet.write('C1', u'摘要', format1)
        worksheet.write('D1', u'收入金额', format1)
        worksheet.write('E1', u'支出金额', format1)
        worksheet.write('F1', u'余额', format1)

        min_date= AccountItem.objects.filter(account=account).aggregate(Min('tx_date'))['tx_date__min']
        min_year= min_date.year
        last_month_balance = 0
        worksheet.write('A2', u'%s-01-%02d'  % (min_year, 1), format1)
        worksheet.write('B2', u'期初余额', format1)
        worksheet.write('C2', u'期初余额', format1)
        worksheet.write('D2', u'', format1)
        worksheet.write('E2', u'', format1)
        worksheet.write('F2', last_month_balance, format1)

        last_balance=0
        balance=0
        total_income = 0
        total_outcome = 0
        start_row=3 #start from 3d row, index from 1
        accountitem_list = AccountItem.objects.select_related('category').filter(account=account)
        i=0
        for i, item  in enumerate(accountitem_list):
            worksheet.write('A%s' % (i+start_row), item.tx_date.strftime('%Y-%m-%d'), format1)
            if not item.category:
                category = ''
            else:
                category = unicode(item.category.name)
            worksheet.write('B%s' % (i+start_row), category, format1)
            worksheet.write('C%s' % (i+start_row), item.summary_display(), format1)
            if item.tx_type:
                worksheet.write('D%s' % (i+start_row), item.amount, format1)
                worksheet.write('E%s' % (i+start_row), None, format1)
                income = item.amount
                outcome = 0
                total_income = total_income + income
            else:
                worksheet.write('D%s' % (i+start_row), None, format1)
                worksheet.write('E%s' % (i+start_row), item.amount, format1)
                income = 0
                outcome = item.amount
                total_outcome = total_outcome + outcome
            balance = last_balance+income-outcome
            worksheet.write('F%s' % (i+start_row), balance, format1)
            last_balance= balance

        if i >0:
            worksheet.write('C%s' % (i+start_row+1), u'合计')
            worksheet.write('D%s' % (i+start_row+1), total_income)
            worksheet.write('E%s' % (i+start_row+1), total_outcome)
            worksheet.write('F%s' % (i+start_row+1), balance)

        left = u'&L\n单位:%s' % settings.ORGNAME
        center = u'&C%s日记账' % account
        right = '' #u'&R\n打印日期:%s' % datetime.datetime.now().strftime('%Y-%m-%d')
        worksheet.set_header(left+center+right, margin=0.6)
        worksheet.set_footer('&C&P/&N', margin=0.5)
        worksheet.set_margins(top=1)

        worksheet.repeat_rows(0)
        #worksheet.hide_gridlines(0)

        workbook.set_properties({
            'title':    u'%s日记账' % account,
            'subject':  u'日记账',
            'author':   settings.AUTHOR,
            'manager':  settings.MANAGER,
            'company':  settings.ORGNAME,
            'category': u'财务日记账',
            'keywords': u'财务日记账',
            'comments': u'本日记账由系统自动导出',
            'status':   'Quo',
        })




        workbook.close()
        output.seek(0)

        displayname=  u'%s.xlsx' % account
        return file_download(request, output, displayname)

    def delete(self, request, *args, **kwargs):
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybill/bill.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本</a>"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'
        ait_id = request.POST.get('id','')
        if not ait_id:
            response['result']['message']=u"无效的id"
        else:
            try:
                item = AccountItem.objects.get(pk=ait_id)
            except:
                response['result']['message']=u"没有这个id"
            else:
                item.delete()
                response['result']['message']=u"删除记录成功"
        return HttpResponse(json.dumps(response))

    @transaction.atomic
    def transfer(self, request, *args, **kwargs):
        if request.method == 'GET':
            account = kwargs.get('account')
            account_list = kwargs.get('account_list')
            income_category_list = AccountCategory.objects.filter(account=account, tx_type=1, parent=None).all()
            outcome_category_list = AccountCategory.objects.filter(account=account, tx_type=0, parent=None).all()
            accountitemid= request.GET.get('id',None)
            if accountitemid:
                accountitem = AccountItem.objects.get(id=accountitemid, account=account)
            else:
                accountitem = None


            return render(request,
                          self.template_name,
                          {
                          'account':account,
                          'account_list':account_list,
                          'servertime':datetime.datetime.now(),
                          'income_category_list': income_category_list,
                          'outcome_category_list': outcome_category_list,
                          'accountitem':accountitem,
                          })
        else:
            account = kwargs.get('account')
            account_list = kwargs.get('account_list')
            response={}
            response['result']={}
            response['result']['success']='true'
            response['result']['message']=u"转账成功，点击这里查看<a href='/mybill/bill.do?accountid=%s&method=list' class='udl fbu'>全部收支</a>" % account.id
            response['result']['totalCount']='0'
            response['result']['pageSize']='100'

            from_account_id = request.POST.get('fromAccountId','')
            to_account_id = request.POST.get('toAccountId','')

            from_category_id = request.POST.get('fromCategoryId','')
            to_category_id = request.POST.get('toCategoryId','')

            ait_id = request.POST.get('id','') # account item id

            if not from_account_id or not to_account_id:
                raise Http404(u"Account does not exists!")

            try:
                from_account = Account.objects.get(id=from_account_id)
                to_account = Account.objects.get(id=to_account_id)
            except Account.DoesNotExist:
                raise Http404(u"Account does not exist")

            if not ait_id:
                if not from_category_id:
                    from_category = None
                else:
                    from_category, created = AccountCategory.objects.get_or_create(id=from_category_id)

                if not to_category_id:
                    to_category = None
                else:
                    to_category, created = AccountCategory.objects.get_or_create(id=to_category_id)

                title = request.POST.get('title','')
                summary = request.POST.get('note','')
                amount = request.POST.get('amount','')
                recDate = request.POST.get('recDate','')

                frInstance = AccountItem(account=from_account)
                frInstance.category = from_category
                frInstance.title = title
                frInstance.summary = summary if summary else u'转出至%s' % to_account
                frInstance.amount = amount if amount else 0
                frInstance.tx_date = datetime.datetime.now()
                if recDate:
                    try:
                        frInstance.tx_date = datetime.datetime.strptime(request.POST.get('recDate',''),'%Y-%m-%d')
                    except:
                        pass
                frInstance.tx_type = TX_TYPE[1][0]
                frInstance.save()

                toInstance = AccountItem(account=to_account)
                toInstance.category = to_category
                toInstance.title = title
                toInstance.summary = summary if summary else u'%s转入' % from_account
                toInstance.amount = amount if amount else 0
                toInstance.tx_date = datetime.datetime.now()
                if recDate:
                    try:
                        toInstance.tx_date = datetime.datetime.strptime(request.POST.get('recDate',''),'%Y-%m-%d')
                    except:
                        pass
                toInstance.tx_type = TX_TYPE[0][0]
                toInstance.save()

                tx = Transaction()
                tx.from_account=from_account
                tx.to_account=to_account
                tx.from_item = frInstance
                tx.to_item = toInstance
                tx.amount = request.POST.get('amount','0')
                if request.POST.get('recDate',''):
                    tx.tx_date = datetime.datetime.strptime(request.POST.get('recDate',''),'%Y-%m-%d')
                tx.save()

                frInstance.transaction_id = tx.id
                frInstance.save()
                toInstance.transaction_id = tx.id
                toInstance.save()

            return HttpResponse(json.dumps(response))

class BillCategoryDoView(ListView):
    def get_queryset(self):
        return []

    def get(self, request, *args, **kwargs):
        accountid = request.GET.get('accountid', None)
        if not accountid:
            raise Http404(u"Account 不存在")

        try:
            account = Account.objects.get(id=accountid)
        except Account.DoesNotExist:
            raise Http404("Account does not exist")
        account_list = Account.objects.all()
        kwargs.update({
            'account':account,
            'account_list':account_list,
        })
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/category_%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request, *args, **kwargs)
        elif method == 'list':
            return self.listall(request, *args, **kwargs)
        elif method == 'edit':
            return self.edit(request, *args, **kwargs)
        elif method == 'append':
            return self.append(request, *args, **kwargs)
        else:
            return render(request, self.template_name, {'form': ''})

    def post(self, request, *args, **kwargs):
        accountid = request.GET.get('accountid', None)
        if not accountid:
            #js ajax accountId, in a attrs
            accountid = request.POST.get('accountId', None)
            if not accountid:
                raise Http404(u"Account does not exist")

        try:
            account = Account.objects.get(id=accountid)
        except Account.DoesNotExist:
            raise Http404("Account does not exist")
        account_list = Account.objects.all()
        kwargs.update({
            'account':account,
            'account_list':account_list,
        })
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/category_%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request, *args, **kwargs)
        elif method == 'edit':
            return self.edit(request, *args, **kwargs)
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
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"已经成功保存收支项目信息!"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'

        category_id = request.POST.get('id','')
        name = request.POST.get('categoryName','无名')
        tx_type = request.POST.get('type','0')
        parent_id = request.POST.get('parentId','0')
        if category_id=='0':
            if parent_id=='0':
                category, created = AccountCategory.objects.get_or_create(account=account, parent_id=None, name=name, tx_type=tx_type)
            else:
                category, created = AccountCategory.objects.get_or_create(account=account, parent_id=parent_id, name=name, tx_type=tx_type)
            response['result']['data']={
                    "@class":"categoryform",
                    "id":category.id,
                    "categoryName":name,
                    "parentId":"0" if not category.parent else str(category.parent.id),
                    "type":tx_type,
                }
        else:
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
            response['result']['data']={
                    "@class":"categoryform",
                    "id":category_id,
                    "categoryName":name,
                    "parentId":"0" if not category.parent else str(category.parent.id),
                    "type":tx_type,
                }
        return HttpResponse(json.dumps(response))

    def listall(self, request, *args, **kwargs):
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        income_category_list = AccountCategory.objects.filter(account=account, tx_type=1, parent=None).all()
        outcome_category_list = AccountCategory.objects.filter(account=account, tx_type=0, parent=None).all()

        return render(request, self.template_name, {
            'account': account,
            'account_list': account_list,
            'income_category_list': income_category_list,
            'outcome_category_list': outcome_category_list,
            })

    def edit(self, request, *args, **kwargs):
        '''
        {"result":{
            "success":"true",
            "message":"已经成功保存收支项目信息!",
            "totalCount":"0",
            "data":{
                "@class":"categoryform",
                "id":"57845394",
                "categoryName":"大笑1",
                "parentId":"0",
                "type":"0"
            },
            "pageIndex":"0",
            "pageSize":"100"}
        }
        '''
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        pk = request.GET.get('id',None)
        try:
            accountcategory = AccountCategory.objects.get(pk=pk)
        except AccountCategory.DoesNotExist:
            return Http404()

        if request.method == 'GET':
            return render(request,
                   self.template_name,
                   {
                       'account': account,
                       'account_list': account_list,
                       'accountcategory': accountcategory,
                   })

    def append(self, request, *args, **kwargs):
        account = kwargs.get('account')
        account_list = kwargs.get('account_list')
        income_category_list = AccountCategory.objects.filter(account=account, tx_type=1, parent=None).all()
        outcome_category_list = AccountCategory.objects.filter(account=account, tx_type=0, parent=None).all()

        return render(request,
                      self.template_name,
                      {
                      'account':account,
                      'account_list':account_list,
                      'servertime':datetime.datetime.now(),
                      'income_category_list': income_category_list,
                      'outcome_category_list': outcome_category_list,
                      })

class BillAccountDoView(ListView):
    def get_queryset(self):
        return []

    def get(self, request, *args, **kwargs):
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/account_%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request, *args, **kwargs)
        elif method == 'edit':
            return self.edit(request, *args, **kwargs)
        elif method == 'append':
            return self.append(request, *args, **kwargs)
        elif method == 'list':
            return self.listall(request, *args, **kwargs)
        else:
            kwargs.update({'account_list': Account.objects.all()})
            return render(request, self.template_name, kwargs)
        return render(request, self.template_name, {'account_list': Account.objects.all()})

    def post(self, request, *args, **kwargs):
        method=request.GET.get('method', 'list')
        self.template_name = 'mybill/account_%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request, *args, **kwargs)
        elif method == 'edit':
            return self.edit(request, *args, **kwargs)
        elif method == 'append':
            return self.append(request, *args, **kwargs)
        elif method == 'list':
            return self.listall(request, *args, **kwargs)
        else:
            kwargs.update({'account_list': Account.objects.all()})
            return render(request, self.template_name, kwargs)
        return render(request, self.template_name, {'account_list': Account.objects.all()})

    def append(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                      {
                      'servertime':datetime.datetime.now(),
                      })

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
        response['result']['message']=u"已经成功保存账户信息!"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'

        account_id = request.POST.get('id','0')
        name = request.POST.get('accountName','无名')
        number = request.POST.get('accountNumber','无名')
        account_type = request.POST.get('accountType','无名')
        display_name = request.POST.get('accountDisplayname','无名')
        tx_type = request.POST.get('type','0')
        parent_id = request.POST.get('parentId','0')
        if account_id=='0':
            account, created = Account.objects.get_or_create(number=number, name=name, account_type=account_type, display_name=display_name)
            response['result']['data']={
                    "@class":"categoryform",
                    "id":account.id,
                    "accountName":name,
                    "type":account_type,
                }
        else:
            account=AccountCategory.objects.get(id=account_id)
            account.display_name = display_name
            account.account_type = account_type
            account.name = name
            account.save()
            response['result']['data']={
                    "@class":"categoryform",
                    "id":account_id,
                    "accountName":name,
                    "type":account_type,
                }
        return HttpResponse(json.dumps(response))
