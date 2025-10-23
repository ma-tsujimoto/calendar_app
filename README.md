
# Django カレンダーアプリ

## 概要
Djangoで作成した予定管理カレンダーアプリです。  
月ごとのカレンダー表示、予定の追加・編集・削除が可能です。  
予定には開始日・終了日・時間帯・色分けを設定できます。

## 主な機能
- カレンダーの月表示（日曜始まり）
- 予定の追加・編集・削除
- 予定期間を日ごとに表示
- 祝日・土日の自動色分け
- 予定の詳細ページ表示

## 使用技術
- Django
- Python 3.x
- HTML / CSS
- jpholiday（祝日判定ライブラリ）
- dateutil（期間計算）

## フォルダ構成
calendar_project/
├── manage.py
├── README.md
├── .gitignore
├── calendar_app/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── __init__.py
│
└── calendar_app_main/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── templatetags/
    │   └── dict_extras.py
    └── templates/
        └── calendar_app_main/
            ├── calendar.html
            ├── add_event.html
            ├── edit_event.html
            ├── event_detail.html
            ├── delete_event.html
