from django.contrib import admin
from .models import Group, GroupMember
# Register your models here.

class GroupMemberInLine(admin.TabularInline):
    model = GroupMember

class GroupAdmin(admin.ModelAdmin):
    fields = ['slug','name','dp','description','owner']

    search_fields = ['name']

    list_filter = ['name','slug']

    list_display= ['name','slug']


admin.site.register(Group,GroupAdmin)


