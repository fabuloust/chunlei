import requests
from django.db import models


class Dispatch(models.Model):
    """
    分发方配置
    """
    class Meta:
        verbose_name = u'分发方配置'

    remark = models.CharField(default='', max_length=100, help_text=u'渠道名', unique=True)
    limit_num = models.IntegerField(default=0, help_text=u'限制数量')
    used_num = models.IntegerField(default=0, help_text=u'已使用数量')
    need_check = models.IntegerField(default=False, help_text=u'是否需要校验')
    dispatch_name = models.CharField(default='', max_length=100, null=True, blank=True, unique=True)
    url = models.CharField(default='', max_length=100, null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # try:
        #     old_obj = Dispatch.objects.get(id=self.id)
        # except:
        #     old_obj = None
        # if not self.id or old_obj.limit_num != self.limit_num:
        #     # 需要更新的情况
        #     from api.manager.manager import get_basic_data
        #     base_data = get_basic_data()
        #     base_data.update({'partner': 'chunleiyiwentong', 'limit_num': self.limit_num, 'remark': self.remark})
        #     result = requests.post('https://www.chunyuyisheng.com/cooperation/wap/business/create_dispatch/',
        #                            data=base_data, headers={'User-Agent': 'Mozilla/5.0'}).json()
        #     self.dispatch_name = result['dispatch']
        #     self.url = 'https://www.chunyuyisheng.com/cooperation/wap/business/info_page/{}/'.format(self.dispatch_name)
        return super(Dispatch, self).save(force_insert, force_update, using, update_fields)


class DispatchUser(models.Model):
    """
    第三方用户
    """
    class Meta:
        verbose_name = '分发方的用户'
    remark = models.CharField(default='', max_length=100, help_text=u'渠道名')
    cellphone = models.CharField(default='', max_length=50, help_text=u'手机号')
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
