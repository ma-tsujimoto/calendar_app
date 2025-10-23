from django.urls import path   # URLパターンを定義するための関数pathをインポート
from . import views            # 同じフォルダ内の views.py を読み込む

# アプリ名を定義（テンプレートでURLを逆引きするときに使う名前空間）
app_name = 'calendar_app_main'

# このアプリ内で使うURLパターン一覧
urlpatterns = [
    # 予定詳細ページ
    # 例: /event/3/ → event_id=3 の予定を表示
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),

    # 予定編集ページ
    # 例: /event/3/edit/ → event_id=3 の予定を編集
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),

    # 予定削除ページ
    # 例: /event/3/delete/ → event_id=3 の予定を削除
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),

    # 予定追加ページ
    # 例: /add/2025/10/23/ → 2025年10月23日に新しい予定を追加
    path('add/<int:year>/<int:month>/<int:day>/', views.add_event, name='add_event'),

    # 指定された年月のカレンダーを表示
    # 例: /2025/10/ → 2025年10月のカレンダーを表示
    path('<int:year>/<int:month>/', views.calendar_view, name='calendar_by_month'),

    # トップページ（URL指定なし）は今月のカレンダーを表示
    # 例: / → 現在の年月のカレンダーを表示
    path('', views.calendar_view, name='calendar_home'),
]
