from django.urls import path
from account import views as account_views

app_name = 'account'

urlpatterns = [
    path('', account_views.index, name='index'),
    path('register', account_views.user_register, name="user_register"),
    path('login', account_views.user_login, name="user_login"),
    path('logout', account_views.user_logout, name="user_logout"),
]
