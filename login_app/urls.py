from django.urls import path
from . import views

app_name = 'login_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('validate', views.validate_fields, name="validate_fields"),
    path('users/<int:profiled_user_id>', views.user_profile, name="user_profile"),
    path('users/<int:profiled_user_id>/update', views.update_user_profile, name="update_user_profile"),
    path('testing', views.testdata, name="test_data"),
    path('createusers', views.create_users, name="create_users"),
    path('resetusers', views.reset_users, name="reset_users"),
]