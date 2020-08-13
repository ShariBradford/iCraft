from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('validate', views.validate_fields),
    path('users/<int:profiled_user_id>', views.user_profile),
    path('testing', views.testdata),
    path('createusers', views.create_users),
]