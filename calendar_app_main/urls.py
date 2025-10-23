from django.urls import path
from . import views

app_name = 'calendar_app_main'

urlpatterns = [
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),

    path('add/<int:year>/<int:month>/<int:day>/', views.add_event, name='add_event'),
    path('<int:year>/<int:month>/', views.calendar_view, name='calendar_by_month'),
    path('', views.calendar_view, name='calendar_home'),
]
