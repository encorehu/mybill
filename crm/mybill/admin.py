from django.contrib import admin

from .models import Account
from .models import AccountItem
from .models import AccountCategory

class AccountAdmin(admin.ModelAdmin):
    pass

class AccountItemAdmin(admin.ModelAdmin):
    list_display=('tx_date','summary','tx_type','amount')

class AccountCategoryAdmin(admin.ModelAdmin):
    list_display=('tx_type','name')

admin.site.register(Account, AccountAdmin)
admin.site.register(AccountItem, AccountItemAdmin)
admin.site.register(AccountCategory, AccountCategoryAdmin)
