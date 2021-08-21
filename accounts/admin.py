from django.contrib import admin

from .models import Account



class AccountAdmin(admin.ModelAdmin):

	list_display = ['user', 'public_id', 'currency', 'balance', 'created_at', 'updated_at']


admin.site.register(Account, AccountAdmin)