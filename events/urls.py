from django.urls import path
from events.views import create_event, home, event_list, dashboard, event_detail, event_update, event_delete
urlpatterns = [
    path('create_event/', create_event, name='create_event'),
    path('', home, name='home'),
    path('event_list/', event_list, name='event_list'),
    path('dashboard/', dashboard, name='dashboard'),
    path('event_detail/', event_detail, name='event_detail'),
    path('event_update/<int:id>/', event_update, name = 'event_update'),
    path('event_delete/<int:id>/', event_delete, name='event_delete')
]
