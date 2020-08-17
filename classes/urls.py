from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('', views.index, name="index"),
    path('new', views.get_class, name='get_class'),
    path('<int:course_id>/rate', views.rate_class, name="rate_class"),
    path('<int:course_id>/update', views.update_class, name="update_class"),
    path('<int:course_id>', views.class_details, name="class_details"),

    path('<int:course_id>/enroll', views.enroll, name="enroll"),
    path('<int:course_id>/unenroll', views.unenroll, name="unenroll"),

    path('<int:course_id>/favorite', views.favorite, name="favorite"),
    path('<int:course_id>/unfavorite', views.unfavorite, name="unfavorite"),
    path('interests', views.interests, name="interests"),
    path('interests/new', views.get_interest, name="get_interest"),
    path('interests/<int:interest_id>/update', views.update_interest, name="update_interest"),
    path('interests/<int:interest_id>/add', views.add_interest, name="add_interest"),
    path('interests/<int:interest_id>/remove', views.remove_interest, name="remove_interest"),
    path('interests/<int:interest_id>', views.interest_classes, name="interest_classes"),
    
    path('favorites', views.favorites, name="favorite_classes"),
    path('search', views.search_classes, name="search_classes"),
]