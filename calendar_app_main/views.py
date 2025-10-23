from django.shortcuts import render, get_object_or_404, redirect
from datetime import date, timedelta
import calendar
import jpholiday
from .models import Event
from .forms import EventForm
from dateutil.relativedelta import relativedelta

def calendar_view(request, year=None, month=None):
    today = date.today()
    if year is None or month is None:
        year = today.year
        month = today.month

    # カレンダー準備
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)  # 週ごとの日配列
    week_days = ['日', '月', '火', '水', '木', '金', '土']

    start_of_month = date(year, month, 1)
    end_of_month = (start_of_month + relativedelta(months=1)) - timedelta(days=1)

    # この表示月に一部でもかかるイベントを取得
    events = Event.objects.filter(
        end_date__gte=start_of_month,
        start_date__lte=end_of_month
    )

    # 日付→イベントリスト の辞書を作る
    event_dict = {}
    for e in events:
        vis_start = max(e.start_date, start_of_month)
        vis_end = min(e.end_date, end_of_month)
        current = vis_start
        while current <= vis_end:
            d = current.day
            event_dict.setdefault(d, []).append(e)
            current += timedelta(days=1)

        # 補助プロパティ（テンプレートで使えるように）
        e._display_start_day = vis_start.day
        e._span_days = (vis_end - vis_start).days + 1

    # 前後の月
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    # 祝日等の色づけ情報を month_info として用意
    month_info = []
    for week in month_days:
        week_info = []
        for i, day in enumerate(week):
            if day == 0:
                week_info.append({'day': '', 'color': 'black'})
            else:
                this_date = date(year, month, day)
                if jpholiday.is_holiday(this_date):
                    color = 'red'
                elif i == 0:
                    color = 'red'
                elif i == 6:
                    color = 'blue'
                else:
                    color = 'black'
                week_info.append({'day': day, 'color': color})
        month_info.append(week_info)

    context = {
        'year': year,
        'month': month,
        'weeks': month_info,
        'week_days': week_days,
        'today': today.day if year == today.year and month == today.month else 0,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'month_days': month_days,
        'event_dict': event_dict,
        'events': events,  # テンプレートで直接イベントを参照したい場合に備えて
    }
    return render(request, 'calendar_app_main/calendar.html', context)


def add_event(request, year, month, day):
    selected_date = date(year, month, day)
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar_app_main:calendar_by_month', year=year, month=month)
    else:
        form = EventForm(initial={'start_date': selected_date, 'end_date': selected_date})
    return render(request, "calendar_app_main/add_event.html", {"form": form, "year": year, "month": month, "day": day})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "calendar_app_main/event_detail.html", {"event": event})


def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            ev = form.save()
            return redirect('calendar_app_main:calendar_by_month', year=ev.start_date.year, month=ev.start_date.month)
    else:
        form = EventForm(instance=event)
    return render(request, 'calendar_app_main/edit_event.html', {'form': form, 'event': event})


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        year = event.start_date.year
        month = event.start_date.month
        event.delete()
        return redirect('calendar_app_main:calendar_by_month', year=year, month=month)
    return render(request, 'calendar_app_main/delete_confirm.html', {'event': event})
