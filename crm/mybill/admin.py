from django.contrib import admin

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import django.forms as forms
from django.template import Template, Context, RequestContext
from django.utils.translation import ungettext, ugettext_lazy as _
from .models import Account
from .models import AccountItem
from .models import AccountCategory

class AccountAdmin(admin.ModelAdmin):
    pass

class AccountItemAdmin(admin.ModelAdmin):
    list_display=('account','tx_date','category','title','summary','tx_type','amount')
    list_filter=('tx_type', 'account','category')
    search_fields = ('summary',)
    actions = ['change_tx_type0','change_tx_type1', 'changeCategory', 'changeAccount']
    categorySuccess = Template('{{ count }} item{{ count|pluralize }}`s category changed to {{ category.name }}')
    accountSuccess = Template('{{ count }} item{{ count|pluralize }}`s account changed to {{ account.name }}')

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
                queryset.update(category=category)
            self.message_user(request, self.categorySuccess.render(Context({'count':queryset.count(), 'category':category})))
            return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.CategoryForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render_to_response('mybill/change_category.html',
                                  {'objects': queryset, 'form': form, 'path':request.get_full_path()},
                                  context_instance=RequestContext(request))
    changeCategory.short_description = 'change category'

    class AccountForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        account = forms.ModelChoiceField(Account.objects)

    def changeAccount(self, request, queryset):
        form = None
        if 'cancel' in request.POST:
            self.message_user(request, 'Canceled change item account')
            return
        elif 'newaccount' in request.POST:
            #do the categorization
            form = self.AccountForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                queryset.update(account=account)
            else:
                print form.errors
            self.message_user(request, self.accountSuccess.render(Context({'count':queryset.count(), 'account':account})))
            return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.AccountForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render_to_response('mybill/change_account.html',
                                  {'objects': queryset, 'form': form, 'path':request.get_full_path()},
                                  context_instance=RequestContext(request))
    changeAccount.short_description = u'change Account'

    def change_tx_type0(self, request, queryset):
        queryset.update(tx_type=0)

    change_tx_type0.short_description = u'change tx_type as outcome'

    def change_tx_type1(self, request, queryset):
        queryset.update(tx_type=1)

    change_tx_type1.short_description = u'change tx_type as income'


class AccountCategoryAdmin(admin.ModelAdmin):
    list_display=('account', 'tx_type', 'parent', 'name')

admin.site.register(Account, AccountAdmin)
admin.site.register(AccountItem, AccountItemAdmin)
admin.site.register(AccountCategory, AccountCategoryAdmin)
