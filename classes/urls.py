from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('favorites', views.favorites),
    path('<int:course_id>', views.class_details),
    path('<int:course_id>/favorite', views.favorite),
    path('<int:course_id>/unfavorite', views.unfavorite),
    path('interests/<int:interest_id>', views.interest_classes),

]