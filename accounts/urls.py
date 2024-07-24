from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]