# Djangoの便利関数をインポート
from django.shortcuts import render, get_object_or_404, redirect  # ページ描画・データ取得・リダイレクト用
from datetime import date, timedelta  # 日付操作のための標準ライブラリ
import calendar                       # カレンダーを生成するためのライブラリ
import jpholiday                      # 日本の祝日判定ライブラリ
from .models import Event             # Eventモデル（予定データ）をインポート
from .forms import EventForm          # Eventフォーム（予定追加・編集用フォーム）をインポート
from dateutil.relativedelta import relativedelta  # 月単位で日付をずらすための便利クラス


# ========================
# 📅 カレンダー表示ビュー
# ========================
def calendar_view(request, year=None, month=None):
    today = date.today()  # 今日の日付を取得
    if year is None or month is None:  # 年月が指定されていない場合は今月を表示
        year = today.year
        month = today.month

    # ==== カレンダー構造を作成 ====
    cal = calendar.Calendar(firstweekday=6)  # 日曜始まりのカレンダーを生成
    month_days = cal.monthdayscalendar(year, month)  # 月の各週をリスト化（例: [[0,1,2,...], [7,8,9,...]]）
    week_days = ['日', '月', '火', '水', '木', '金', '土']  # 曜日名リスト

    start_of_month = date(year, month, 1)  # 月初日
    end_of_month = (start_of_month + relativedelta(months=1)) - timedelta(days=1)  # 月末日

    # ==== イベント取得 ====
    # 表示中の月に「一部でも」かかっているイベントを取得
    events = Event.objects.filter(
        end_date__gte=start_of_month,   # 終了日が月初以降
        start_date__lte=end_of_month    # 開始日が月末以前
    )

    # ==== 日付ごとのイベント辞書を作成 ====
    event_dict = {}  # {日付: [イベント, イベント, ...]} 形式
    for e in events:
        # 表示範囲内にイベントを切り取る（開始日・終了日が月をまたぐ場合対応）
        vis_start = max(e.start_date, start_of_month)
        vis_end = min(e.end_date, end_of_month)
        current = vis_start

        # イベントが続く日数分を日付単位で辞書に登録
        while current <= vis_end:
            d = current.day
            event_dict.setdefault(d, []).append(e)
            current += timedelta(days=1)

        # テンプレートで期間バーを描くための補助データを一時的に持たせる
        e._display_start_day = vis_start.day       # 表示開始日
        e._span_days = (vis_end - vis_start).days + 1  # 表示日数（バーの長さ用）

    # ==== 前月・翌月の計算 ====
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    # ==== カレンダーに曜日ごとの色づけ情報をつける ====
    month_info = []
    for week in month_days:
        week_info = []
        for i, day in enumerate(week):
            if day == 0:  # その週に存在しない日
                week_info.append({'day': '', 'color': 'black'})
            else:
                this_date = date(year, month, day)
                # 祝日・日曜・土曜を色分け
                if jpholiday.is_holiday(this_date):
                    color = 'red'
                elif i == 0:  # 日曜
                    color = 'red'
                elif i == 6:  # 土曜
                    color = 'blue'
                else:
                    color = 'black'
                week_info.append({'day': day, 'color': color})
        month_info.append(week_info)

    # ==== テンプレートに渡すデータ ====
    context = {
        'year': year, 'month': month,
        'weeks': month_info,          # カレンダー構造
        'week_days': week_days,       # 曜日名
        'today': today.day if year == today.year and month == today.month else 0,  # 今日の日付（今月のみ表示）
        'prev_year': prev_year, 'prev_month': prev_month,  # 前月へのリンク用
        'next_year': next_year, 'next_month': next_month,  # 翌月へのリンク用
        'month_days': month_days,     # 週ごとの日付配列
        'event_dict': event_dict,     # 日付ごとのイベント辞書
        'events': events,             # 全イベントリスト（テンプレートで直接参照可能）
    }

    # calendar.html に context のデータを渡して画面を表示
    return render(request, 'calendar_app_main/calendar.html', context)


# ========================
# ➕ イベント追加ビュー
# ========================
def add_event(request, year, month, day):
    selected_date = date(year, month, day)  # 選択された日付を取得
    if request.method == "POST":  # フォームが送信された場合
        form = EventForm(request.POST)
        if form.is_valid():  # 入力チェックOKなら保存
            form.save()
            # 保存後は該当月のカレンダーに戻る
            return redirect('calendar_app_main:calendar_by_month', year=year, month=month)
    else:
        # 初期値として選択日を設定
        form = EventForm(initial={'start_date': selected_date, 'end_date': selected_date})
    # イベント追加画面を表示
    return render(request, "calendar_app_main/add_event.html", {"form": form, "year": year, "month": month, "day": day})


# ========================
# 🔍 イベント詳細ビュー
# ========================
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # IDが存在しない場合は404エラー
    return render(request, "calendar_app_main/event_detail.html", {"event": event})


# ========================
# ✏️ イベント編集ビュー
# ========================
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # 編集対象のイベントを取得
    if request.method == 'POST':  # フォーム送信時
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            ev = form.save()  # 編集内容を保存
            # 編集後はイベントの開始月に戻る
            return redirect('calendar_app_main:calendar_by_month', year=ev.start_date.year, month=ev.start_date.month)
    else:
        # ページ初回表示時は既存データをフォームに表示
        form = EventForm(instance=event)
    return render(request, 'calendar_app_main/edit_event.html', {'form': form, 'event': event})


# ========================
# ❌ イベント削除ビュー
# ========================
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # 削除対象のイベントを取得
    if request.method == 'POST':  # 確認画面で「削除」ボタンが押された場合
        year = event.start_date.year
        month = event.start_date.month
        event.delete()  # データベースから削除
        return redirect('calendar_app_main:calendar_by_month', year=year, month=month)
    # 削除確認画面を表示
    return render(request, 'calendar_app_main/delete_confirm.html', {'event': event})
