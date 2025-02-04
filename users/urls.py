from django.urls import path
from users.views import group_list, sign_up, sign_in, sign_out, activate_user, assign_role, admin_dashboard, create_group, rsvp_event, cancel_rsvp

urlpatterns = [
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_out/', sign_out, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/<int:user_id>/assign_role/', assign_role, name='assign_role'),
    path('admin/create_group/', create_group, name='create_group'),
    path('admin/group_list/', group_list, name='group_list'),
    path('rsvp_event/<int:id>/', rsvp_event, name='rsvp_event'),
    path('cancel_rsvp/<int:id>/', cancel_rsvp, name='cancel_rsvp')
]
