
import requests
from django.views.decorators.http import require_GET

from api.manager.manager import get_basic_data
from api.models import DispatchUser, Dispatch
from utilities.response import json_http_response, json_http_success


def main_view(request):
    """
    主接口，查看各个合作方使用情况
    """
    result = requests.get('https://www.chunyuyisheng.com/cooperation/wap/business/get_dispatch_info/',
                          params=get_basic_data(), headers={'User-Agent': 'Mozilla/5.0'}).json()
    info_list = result['result']
    for info in info_list:
        obj = Dispatch.objects.get(dispatch_name=info['name'])
        obj.used_num = info['used_num']
        obj.save()
    return json_http_response(info_list)


@require_GET
def check_user_validity(request):
    """
    URL[GET]: /api/check_user_validity/
    :return: 1 or 0
    """
    dispatch = request.GET.get('dispatch')
    cellphone = request.GET.get('cellphone')
    try:
        obj = Dispatch.objects.get(dispatch_name=dispatch)
    except:
        obj = None
    return json_http_success({'available': 1 if (not obj or not obj.need_check or DispatchUser.objects.filter(remark=dispatch, cellphone=cellphone).exists()) else 0})