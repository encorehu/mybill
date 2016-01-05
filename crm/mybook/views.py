#-*- coding=utf-8 -*-
import os
import json
import datetime

from django.shortcuts import render
from django.http import HttpResponse, Http404

from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
from django.db.models import Q

from django.views.generic import ListView
from django.conf import settings

from mybill.models import Account
from mybill.models import AccountBook

from django.core.servers.basehttp import FileWrapper

def file_download(request, filename, displayname):
    filepath = filename
    wrapper = FileWrapper(open(filepath,'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = (u'attachment; filename=%s' % displayname).encode('utf-8')
    return response

# Create your views here.
class BookIndexView(ListView):
    template_name = 'mybook/index.html'

    def get_queryset(self):
        return []

    def get(self, request, bookid=1):
        try:
            book = AccountBook.objects.get(id=bookid)
        except AccountBook.DoesNotExist:
            raise Http404("AccountBook does not exist")
        return render(request, self.template_name, {
                'book': book,
                'book_list':  AccountBook.objects.all(),
                    })

class BookDoView(ListView):
    def get_queryset(self):
        return []

    def addOrUpdate(self, request, *args, **kwargs):
        '''
        {"result":
            {
                "success":"true",
                "message":"新增记录成功，点击这里查看<a href='\/mybook\/book.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本<\/a>",
                "totalCount":"0",
                "pageIndex":"0",
                "pageSize":"100"
            }
        }
'''
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybook/book.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本</a>"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'


        ait_id = request.POST.get('id','')
        if not ait_id:
            # 新建账目条目
            #book=AccountBook.objects.get_or_create(id=1,name=u'默认账户')
            #book,created=AccountBook.objects.get_or_create(id=1)
            instance = AccountBookItem(book=book)
            #instance.book_id = 1
            category_id = request.POST.get('categoryId','0')
            subcategory_id = request.POST.get('subCategoryId','0')
            if subcategory_id=='0':
                category, created = AccountBookCategory.objects.get_or_create(id=category_id, parent_id=None)
            else:
                category, created = AccountBookCategory.objects.get_or_create(id=subcategory_id, parent_id=category_id)
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
            #book,created=AccountBook.objects.get_or_create(id=1)
            instance = AccountBookItem.objects.get(id=ait_id, book=book)
            category_id = request.POST.get('categoryId','0')
            subcategory_id = request.POST.get('subCategoryId','0')
            if subcategory_id=='0':
                category, created = AccountBookCategory.objects.get_or_create(id=category_id, parent_id=None)
            else:
                category, created = AccountBookCategory.objects.get_or_create(id=subcategory_id, parent_id=category_id)
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
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybook/%s/book.do?method=listmonth&strMonth=%s-%s' class='udl fbu'>该月账本</a>" % (book.id, year, month)
        return HttpResponse(json.dumps(response))

    def listmonth(self, request, *args, **kwargs):
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
        if request.method == 'GET':
            strMonth=request.GET.get('strMonth','')
        else:
            strMonth=request.POST.get('strMonth','')

        if strMonth:
            year,month = map(int, strMonth.split('-'))
        else:
            now = datetime.datetime.now()
            year,month = now.year, now.month

        bookitem_list = AccountBookItem.objects.select_related('category').filter(book=book, tx_date__year=year, tx_date__month=month)
        last_balance = 0
        income = bookitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        outcome = bookitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        balance = last_balance + income - outcome
        return render(request, self.template_name, {
            'book': book,
            'book_list': book_list,
            'bookitem_list': bookitem_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            'year': year,
            'month': month,
            })

    def edit(self, request, *args, **kwargs):
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
        pk = request.GET.get('id','1')
        bookitem = AccountBookItem.objects.get(pk=pk)
        income_category_list = AccountBookCategory.objects.filter(book=book, tx_type=1, parent=None).all()
        outcome_category_list = AccountBookCategory.objects.filter(book=book, tx_type=0, parent=None).all()
        return render(request,
                      self.template_name,
                      {
                          'book':book,
                          'book_list':book_list,
                          'bookitem': bookitem,
                          'income_category_list': income_category_list,
                          'outcome_category_list': outcome_category_list,
                      })

    def get(self, request, bookid=1, *args, **kwargs):
        try:
            book = AccountBook.objects.get(id=bookid)
        except AccountBook.DoesNotExist:
            raise Http404("AccountBook does not exist")
        book_list = AccountBook.objects.all()
        kwargs.update({
            'book':book,
            'book_list':book_list,
        })
        method=request.GET.get('method', 'list')
        self.template_name = 'mybook/%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request, *args, **kwargs)
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
        else:
            kwargs.update(form=None)
            return render(request, self.template_name, kwargs)

    def post(self, request, bookid=1, *args, **kwargs):
        try:
            book = AccountBook.objects.get(id=bookid)
        except AccountBook.DoesNotExist:
            raise Http404("AccountBook does not exist")
        book_list = AccountBook.objects.all()
        kwargs.update({
            'book':book,
            'book_list':book_list,
        })
        method=request.POST.get('method', '')
        if not method:
            method = request.GET.get('method', 'list')
        self.template_name = 'mybook/%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request, *args, **kwargs)
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
        elif method == 'del':
            return self.delete(request)
        else:
            return render(request, self.template_name, {'form': ''})

    def append(self, request, *args, **kwargs):
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
        income_category_list = AccountBookCategory.objects.filter(book=book, tx_type=1, parent=None).all()
        outcome_category_list = AccountBookCategory.objects.filter(book=book, tx_type=0, parent=None).all()

        return render(request,
                      self.template_name,
                      {
                      'book':book,
                      'book_list':book_list,
                      'servertime':datetime.datetime.now(),
                      'income_category_list': income_category_list,
                      'outcome_category_list': outcome_category_list,
                      })

    def listall(self, request, *args, **kwargs):
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
        if request.method == 'GET':
            strMonth=request.GET.get('strMonth','')
        else:
            strMonth=request.POST.get('strMonth','')

        if strMonth:
            year,month = map(int, strMonth.split('-'))
        else:
            now = datetime.datetime.now()
            year,month = now.year, now.month

        account_list = Account.objects.filter(accountbook=book)
        last_balance = 0
        income = 0
        outcome = 0
        balance = 0
        return render(request, self.template_name, {
            'book': book,
            'book_list': book_list,
            'account_list': account_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            'year': year,
            'month': month,
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
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
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
            income_category_list = AccountBookCategory.objects.filter(tx_type=1, parent=None).all()
            outcome_category_list = AccountBookCategory.objects.filter(tx_type=0, parent=None).all()
            return render(request, self.template_name, {
                'book': book,
                'book_list': book_list,
                'bookitem_list': [],
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
            bookitem_list = AccountBookItem.objects.select_related('category').filter(tx_date__gte=datetime.datetime.strptime(fromRecDate, '%Y-%m-%d'))
            if toRecDate:
                bookitem_list= bookitem_list.filter(tx_date__lte=datetime.datetime.strptime(toRecDate, '%Y-%m-%d'))
        else:
            bookitem_list = AccountBookItem.objects.select_related('category')
            if toRecDate:
                bookitem_list= bookitem_list.filter(tx_date__lte=datetime.datetime.strptime(toRecDate, '%Y-%m-%d'))

        if tx_type:
            bookitem_list= bookitem_list.filter(tx_type = tx_type)

        if subCategoryId:
            #如果子分类不为空, 即选中子分类, 就只过滤子分类
            bookitem_list= bookitem_list.filter(category__id = subCategoryId)
            category_id = subCategoryId
        else:
            #否则过滤父分类和所有的子分类
            if categoryId:
                subCategoryIds= list(AccountBookCategory.objects.filter(parent__id=categoryId).values_list('id', flat=True).all())
                subCategoryIds.insert(0, categoryId)
                bookitem_list= bookitem_list.filter(category__id__in = subCategoryIds)

        last_balance = 0
        income = bookitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        outcome = bookitem_list.filter(~Q(tx_type=1)).aggregate(
                     combined_credit=Coalesce(Sum('amount'), V(0)))['combined_credit']
        balance = last_balance + income - outcome

        income_category_list = AccountBookCategory.objects.filter(tx_type=1, parent=None).all()
        outcome_category_list = AccountBookCategory.objects.filter(tx_type=0, parent=None).all()
        return render(request, self.template_name, {
            'book':book,
            'bookitem_list': bookitem_list,
            'income': income,
            'outcome': outcome,
            'balance': balance,
            'year': year,
            'month': month,
            'category_id': category_id,
            'income_category_list': income_category_list,
            'outcome_category_list': outcome_category_list,
            })

    def export(self, request, *args, **kwargs):
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
        strMonth = request.GET.get('strMonth','')
        if strMonth:
            year,month = map(int, strMonth.split('-'))
        else:
            now = datetime.datetime.now()
            year,month = now.year, now.month
        bookitem_list = AccountBookItem.objects.select_related('category').filter(book=book, tx_date__year=year, tx_date__lt=datetime.datetime(year,month,1))
        import xlsxwriter
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(strMonth+'.xlsx')
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
        bookitem_list = AccountBookItem.objects.select_related('category').filter(book=book, tx_date__year=year, tx_date__lt=datetime.datetime(year,month,1))
        #bookitem_list = AccountBookItem.objects.select_related('category').filter(tx_date__year=year_of_last_month, tx_date__month=month)
        last_balance = 0
        last_month_income = bookitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        last_month_outcome = bookitem_list.filter(~Q(tx_type=1)).aggregate(
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
        bookitem_list = AccountBookItem.objects.select_related('category').filter(book=book, tx_date__year=year_of_last_month, tx_date__month=month)
        for i, item  in enumerate(bookitem_list):
            worksheet.write('A%s' % (i+start_row), unicode(item.category), format1)
            worksheet.write('B%s' % (i+start_row), item.tx_date.strftime('%Y-%m-%d'), format1)
            worksheet.write('C%s' % (i+start_row), item.summary, format1)
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


        # Write some numbers, with row/column notation.
        #worksheet.write(2, 0, 123)
        #worksheet.write(3, 0, 123.456)

        # Insert an image.
        # worksheet.insert_image('B5', 'logo.png')
        left = u'&L\n单位:%s' % settings.ORGNAME
        center = u'&C%s%s年%s月日记账' % (book, year, month)
        right = '' #u'&R\n打印日期:%s' % datetime.datetime.now().strftime('%Y-%m-%d')
        worksheet.set_header(left+center+right, margin=0.6)
        worksheet.set_footer('&C&P/&N', margin=0.5)
        worksheet.set_margins(top=1)

        worksheet.repeat_rows(0)
        #worksheet.hide_gridlines(0)

        workbook.set_properties({
            'title':    u'%s%s年%s月日记账' % (book, year, month),
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
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybook/book.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本</a>"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'
        #return HttpResponse(json.dumps(response))

        filename = strMonth+'.xlsx'
        displayname=  u'%s%s年%s月.xlsx' % (book, year,month)
        return file_download(request, filename, displayname)

    def exportyear(self, request, *args, **kwargs):
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
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
        bookitem_list = AccountBookItem.objects.select_related('category').filter(book=book, tx_date__year=year)
        import xlsxwriter
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(strMonth+'.xlsx')
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
        bookitem_list = AccountBookItem.objects.select_related('category').filter(book=book, tx_date__year=year)
        #bookitem_list = AccountBookItem.objects.select_related('category').filter(tx_date__year=year_of_last_month, tx_date__month=month)
        last_balance = 0
        last_month_income = bookitem_list.filter(tx_type=1).aggregate(
                     combined_debit=Coalesce(Sum('amount'), V(0)))['combined_debit']
        last_month_outcome = bookitem_list.filter(~Q(tx_type=1)).aggregate(
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
        bookitem_list = AccountBookItem.objects.select_related('category').filter(book=book, tx_date__year=year)
        for i, item  in enumerate(bookitem_list):
            worksheet.write('A%s' % (i+start_row), unicode(item.category), format1)
            worksheet.write('B%s' % (i+start_row), item.tx_date.strftime('%Y-%m-%d'), format1)
            worksheet.write('C%s' % (i+start_row), item.summary, format1)
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


        # Write some numbers, with row/column notation.
        #worksheet.write(2, 0, 123)
        #worksheet.write(3, 0, 123.456)

        # Insert an image.
        # worksheet.insert_image('B5', 'logo.png')
        left = u'&L\n单位:%s' % settings.ORGNAME
        center = u'&C%s年日记账' % (year, )
        right = '' #u'&R\n打印日期:%s' % datetime.datetime.now().strftime('%Y-%m-%d')
        worksheet.set_header(left+center+right, margin=0.6)
        worksheet.set_footer('&C&P/&N', margin=0.5)
        worksheet.set_margins(top=1)

        worksheet.repeat_rows(0)
        #worksheet.hide_gridlines(0)

        workbook.set_properties({
            'title':    u'%s年日记账' % (year, ),
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
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybook/book.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本</a>"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'
        #return HttpResponse(json.dumps(response))

        filename = strMonth+'.xlsx'
        displayname=  u'%s年.xlsx' % (year, )
        return file_download(request, filename, displayname)

    def delete(self, request, *args, **kwargs):
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybook/book.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本</a>"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'
        ait_id = request.POST.get('id','')
        if not ait_id:
            response['result']['message']=u"无效的id"
        else:
            try:
                item = AccountBookItem.objects.get(pk=ait_id)
            except:
                response['result']['message']=u"没有这个id"
            else:
                item.delete()
                response['result']['message']=u"删除记录成功"
        return HttpResponse(json.dumps(response))

class BookCategoryDoView(ListView):
    def get_queryset(self):
        return []

    def get(self, request, bookid=1, *args, **kwargs):
        try:
            book = AccountBook.objects.get(id=bookid)
        except AccountBook.DoesNotExist:
            raise Http404("AccountBook does not exist")
        book_list = AccountBook.objects.all()
        kwargs.update({
            'book':book,
            'book_list':book_list,
        })
        method=request.GET.get('method', 'list')
        self.template_name = 'mybook/category_%s.html' % method
        if method == 'addOrUpdate':
            return self.addOrUpdate(request, *args, **kwargs)
        elif method == 'list':
            return self.listall(request, *args, **kwargs)
        elif method == 'append':
            return self.append(request, *args, **kwargs)
        else:
            return render(request, self.template_name, {'form': ''})

    def post(self, request, bookid=1, *args, **kwargs):
        try:
            book = AccountBook.objects.get(id=bookid)
        except AccountBook.DoesNotExist:
            raise Http404("AccountBook does not exist")
        method=request.GET.get('method', 'list')
        self.template_name = 'mybook/category_%s.html' % method
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
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
        response={}
        response['result']={}
        response['result']['success']='true'
        response['result']['message']=u"新增记录成功，点击这里查看<a href='/mybook/book.do?method=listmonth&strMonth=2015-10' class='udl fbu'>该月账本</a>"
        response['result']['totalCount']='0'
        response['result']['pageSize']='100'

        category_id = request.POST.get('id','')
        if category_id=='0':
            name = request.POST.get('categoryName','无名')
            tx_type = request.POST.get('type','0')
            parent_id = request.POST.get('parentId','0')
            if parent_id=='0':
                category, created = AccountBookCategory.objects.get_or_create(parent_id=None, name=name, tx_type=tx_type)
            else:
                category, created = AccountBookCategory.objects.get_or_create(parent_id=parent_id, name=name, tx_type=tx_type)
        else:
            category=AccountBookCategory.objects.get(id=category_id)
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
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
        income_category_list = AccountBookCategory.objects.filter(book=book, tx_type=1, parent=None).all()
        outcome_category_list = AccountBookCategory.objects.filter(book=book, tx_type=0, parent=None).all()

        return render(request, self.template_name, {
            'book': book,
            'book_list': book_list,
            'income_category_list': income_category_list,
            'outcome_category_list': outcome_category_list,
            })

    def append(self, request, *args, **kwargs):
        book = kwargs.get('book')
        book_list = kwargs.get('book_list')
        income_category_list = AccountBookCategory.objects.filter(tx_type=1, parent=None).all()
        outcome_category_list = AccountBookCategory.objects.filter(tx_type=0, parent=None).all()

        return render(request,
                      self.template_name,
                      {
                      'book':book,
                      'book_list':book_list,
                      'servertime':datetime.datetime.now(),
                      'income_category_list': income_category_list,
                      'outcome_category_list': outcome_category_list,
                      })