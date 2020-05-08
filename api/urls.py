from django.urls import path

from api.view import check_user_validity

urlpatterns = [
    # 附近活动
    path('check_user_validity/', check_user_validity),
]
