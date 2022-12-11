from django.urls import path, include

from users import views

urlpatterns = [
    path('', views.profile, name="profile"),
    path('change_profile/', views.change_profile, name="change_profile"),
]