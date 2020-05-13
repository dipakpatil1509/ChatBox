from django.contrib import admin
from .models import UserInf
# Register your models here.

class UserInfAdmin(admin.ModelAdmin):

    fields = ('first_name','last_name','email','username')

admin.site.register(UserInf)