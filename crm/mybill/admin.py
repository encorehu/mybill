from django.contrib import admin

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

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
    actions = ['changeCategory']
    categorySuccess = Template('{{ count }} link{{ count|pluralize }}`s category changed to {{ category.name }}')

    class CategoryForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        category = forms.ModelChoiceField(AccountCategory.objects)

    def changeCategory(self, request, queryset):
        form = None
        print request.POST

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

class AccountCategoryAdmin(admin.ModelAdmin):
    list_display=('tx_type','name')

admin.site.register(Account, AccountAdmin)
admin.site.register(AccountItem, AccountItemAdmin)
admin.site.register(AccountCategory, AccountCategoryAdmin)
