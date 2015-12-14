#-*- coding=utf-8 -*-
from django.contrib import admin

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import django.forms as forms
from django.template import Template, Context, RequestContext
from django.utils.translation import ungettext, ugettext_lazy as _

def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))


from .models import Account
from .models import AccountItem
from .models import AccountCategory

class AccountAdmin(admin.ModelAdmin):
    pass

class AccountItemAdmin(admin.ModelAdmin):
    list_display=('account','tx_date','category','summary','tx_type','amount')
    search_fields = ('summary',)
    actions = ['changeCategory', 'changeAccount']
    categorySuccess = Template('{{ count }} link{{ count|pluralize }}`s category changed to {{ category.name }}')
    accountSuccess = Template('{{ count }} link{{ count|pluralize }}`s account changed to {{ account.name }}')

    class CategoryForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        category = forms.ModelChoiceField(AccountCategory.objects)

    def changeCategory(self, request, queryset):
        form = None
        if 'cancel' in request.POST:
            self.message_user(request, 'Canceled link categorization')
            return
        elif 'categorize' in request.POST:
            #do the categorization
            form = self.CategoryForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['category']
            for link in queryset:
                link.category = category
                link.save()
            self.message_user(request, self.categorySuccess.render(Context({'count':queryset.count(), 'category':category})))
            return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.CategoryForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render_to_response('mybill/change_category.html',
                                  {'links': queryset, 'form': form, 'path':request.get_full_path()},
                                  context_instance=RequestContext(request))
    changeCategory.short_description = 'change category'

    class AccountForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        account = forms.ModelChoiceField(Account.objects)

    def changeAccount(self, request, queryset):
        form = None
        if 'cancel' in request.POST:
            self.message_user(request, 'Canceled link account')
            return
        elif 'categorize' in request.POST:
            #do the categorization
            form = self.AccountForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                queryset.update(account=account)
            else:
                print form.errors()
            self.message_user(request, self.accountSuccess.render(Context({'count':queryset.count(), 'account':account})))
            return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.AccountForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render_to_response('mybill/change_account.html',
                                  {'links': queryset, 'form': form, 'path':request.get_full_path()},
                                  context_instance=RequestContext(request))
    changeAccount.short_description = u'change Account'


class AccountCategoryAdmin(admin.ModelAdmin):
    list_display=('tx_type','name')

admin.site.register(Account, AccountAdmin)
admin.site.register(AccountItem, AccountItemAdmin)
admin.site.register(AccountCategory, AccountCategoryAdmin)
