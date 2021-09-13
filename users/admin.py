from django.contrib import admin

from .models import User



class UserAdmin(admin.ModelAdmin):

	list_display = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'email_verified']


admin.site.register(User, UserAdmin)