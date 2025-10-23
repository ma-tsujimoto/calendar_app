from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理画面URL
    path('', include('calendar_app_main.urls')),  # カレンダーアプリのルーティング
]
