from django.contrib import admin

from .models import Account
from .models import AccountItem

class AccountAdmin(admin.ModelAdmin):
	pass

class AccountItemAdmin(admin.ModelAdmin):
	list_display=('tx_date','debit','credit')

admin.site.register(Account, AccountAdmin)
admin.site.register(AccountItem, AccountItemAdmin)
