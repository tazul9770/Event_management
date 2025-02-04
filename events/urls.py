from django.urls import path
from events.views import create_event, event_list, dashboard, event_update, event_delete, view_event, view_detail
urlpatterns = [
    path('create_event/', create_event, name='create_event'),
    path('event_list/', event_list, name='event_list'),
    path('dashboard/', dashboard, name='dashboard'),
    path('event_update/<int:id>/', event_update, name = 'event_update'),
    path('event_delete/<int:id>/', event_delete, name='event_delete'),
    path('view_event/', view_event, name='view_event'),
    path('view_detail/<int:id>/', view_detail, name='view_detail')
]
