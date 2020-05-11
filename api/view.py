import json

import requests
import xlrd as xlrd
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from api.manager.manager import get_basic_data, create_dispatch_user
from api.models import DispatchUser, Dispatch
from utilities.encoding import ensure_unicode
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


class ExcelForm(forms.Form):
    excel = forms.FileField()


@csrf_exempt
def upload_excel(request):
    """
    URL: /api/upload_excel/
    一次上传多张图片，每次最多上传16张(实际客户端可能会限制为9张)
    会上传到CDN，目前主要是社区在使用
    PARA:
            upload_method:     上传方式
                weinxin_mini 从微信小程序api将文件上传至至七牛服务器
                alipay_mini  从支付宝小程序api将文件上传至七牛服务器
    TODO:之前只有h5和小程序在用，现在h5转为直传方式，小程序在用。
    """
    if request.method == "POST":
        form = ExcelForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponseBadRequest(content=json.dumps(form.errors, ensure_ascii=False))
        file = form.cleaned_data["excel"]
        excel = xlrd.open_workbook(file_contents=file.read())
        sheet = excel.sheets()[0]
        rows = sheet.nrows
        error_list = []
        all_remarks = Dispatch.objects.values_list('remark', flat=True).distinct()
        for i in range(rows):
            row_values = sheet.row_values(i)
            remark = row_values[0]
            cellphone = row_values[1]
            error_msg = create_dispatch_user(remark, cellphone, all_remarks)
            if error_msg:
                error_list.append([remark, cellphone, error_msg])

        return HttpResponse(json.dumps({"files": error_list}),
                            content_type="application/json")
    else:
        form = ExcelForm()
        return render_to_response("excelupload.html", {"form": form})
