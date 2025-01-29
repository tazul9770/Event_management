from django.urls import path
from users.views import sign_up, sign_in, sign_out, home

urlpatterns = [
    path('home/', home, name='home'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_out/', sign_out, name='logout')
]
