# users/urls.py
from django.urls import path
from .views import register_user, user_details, referrals

urlpatterns = [
    path('register/', register_user),
    path('details/', user_details),
    path('referrals/', referrals),
]
