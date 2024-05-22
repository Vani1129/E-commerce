from django.contrib import admin
from .models import Accounts, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html


# Register your models here
@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username' , 'email',  'last_login' , 'date_of_joining', 'phone_no')
    list_display_links = ('first_name', 'last_name' , 'email')
    readonly_fields = ('last_login' , 'date_of_joining')
    ordering = ('-date_of_joining',)

    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    
class UserProfileAdmin(admin.ModelAdmin):
   def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    # thumbnail.short_description = 'Profile Picture'
list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(UserProfile, UserProfileAdmin)
UserProfileAdmin.thumbnail.short_description = 'Profile Picture'

    