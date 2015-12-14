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


def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"


class AccountItemAdmin(admin.ModelAdmin):
    list_display=('account','tx_date','category','summary','tx_type','amount')
    search_fields = ('summary',)
    actions = [export_selected_objects]

class AccountCategoryAdmin(admin.ModelAdmin):
    list_display=('tx_type','name')

admin.site.register(Account, AccountAdmin)
admin.site.register(AccountItem, AccountItemAdmin)
admin.site.register(AccountCategory, AccountCategoryAdmin)
