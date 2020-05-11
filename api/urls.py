from django.urls import path

from api.view import check_user_validity, upload_excel

urlpatterns = [
    # 附近活动
    path('check_user_validity/', check_user_validity),
    path('upload_excel/', upload_excel),
]
