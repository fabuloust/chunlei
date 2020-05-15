from django.contrib import admin
from reversion.admin import VersionAdmin

from api.models import Dispatch, DispatchUser

admin.site.site_header = '春雷健康医问通管理平台'
admin.site.site_title = '春雷健康医问通管理平台'
admin.site.index_title = '春雷健康医问通管理平台'

@admin.register(Dispatch)
class DispatchAdmin(VersionAdmin):

    list_display = ['remark', 'limit_num', 'used_num', 'url']
    readonly_fields = ['url', 'dispatch_name']


@admin.register(DispatchUser)
class DispatchUserAdmin(VersionAdmin):

    list_display = ['remark', 'cellphone']
