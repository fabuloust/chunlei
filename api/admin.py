from django.contrib import admin
from reversion.admin import VersionAdmin

from api.models import Dispatch, DispatchUser


@admin.register(Dispatch)
class DispatchAdmin(VersionAdmin):

    list_display = ['remark', 'limit_num', 'used_num', 'url']
    readonly_fields = ['url', 'dispatch_name']


@admin.register(DispatchUser)
class DispatchUserAdmin(VersionAdmin):

    list_display = ['remark', 'cellphone']
