from django.db import models  # Djangoのモデル機能を使うためにmodelsをインポート

# Event（予定）を表すモデルクラス
class Event(models.Model):
    # 予定のタイトル（最大200文字）
    title = models.CharField(max_length=200)
    
    # 予定の詳細説明（空欄でもOK）
    detail = models.TextField(blank=True)  # ←ここ、全角カッコ「）」が入っていたので修正しています！
    
    # 予定の開始日（必須）
    start_date = models.DateField()
    
    # 予定の終了日（必須）
    end_date = models.DateField()
    
    # 予定の開始時間（空でもOK）
    start_time = models.TimeField(null=True, blank=True)
    
    # 予定の終了時間（空でもOK）
    end_time = models.TimeField(null=True, blank=True)
    
    # 予定の色（カレンダー上での表示色、デフォルトは青 #0078d7）
    color = models.CharField(max_length=20, default="#0078d7")
    
    # 管理画面などでこのモデルを文字列として表示するときの形式を定義
    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"
