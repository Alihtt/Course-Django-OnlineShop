from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm,UserCreationForm
from .models import User
from django.contrib.auth.models import Group

# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('email','phone_number','is_admin')
    search_fields = ('email','full_name')
    filter_horizontal = ()
    list_filter = ('is_admin',)
    ordering = ('full_name',)
    
    fieldsets = (
        (None,{'fields':('email','full_name','phone_number','password')}),
        ('Permissions',{'fields':('is_active','is_admin','last_login')})
    )
    add_fieldsets = (
        (None,{'fields':('phone_number','email','full_name','password1','password2')}),
    )
    
admin.site.unregister(Group)
admin.site.register(User,UserAdmin)
    
    
    
    