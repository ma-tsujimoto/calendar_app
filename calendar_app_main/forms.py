# Djangoのフォーム機能を使うためにインポート
from django import forms

# models.pyで定義したEventモデルをインポート
from .models import Event


# ===============================
# 📝 EventFormクラス（予定入力フォーム）
# ===============================
# このクラスは、Eventモデルのデータを入力・編集するためのフォームを自動生成します。
class EventForm(forms.ModelForm):

    # Metaクラスは、このフォームがどのモデルに基づいて作られるかを指定する部分です。
    class Meta:
        model = Event  # Eventモデルと紐づける
        # フォームに表示するフィールドを指定（モデルの中から選ぶ）
        fields = ['title', 'detail', 'start_date', 'end_date', 'start_time', 'end_time', 'color']

        # 各フィールドの入力形式（HTMLタグの属性）を設定
        widgets = {
            # 📅 開始日と終了日は <input type="date"> でカレンダー入力に
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),

            # ⏰ 開始時間と終了時間は <input type="time"> で時刻入力に
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
