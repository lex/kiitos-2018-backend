from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from observations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('observation-points/', views.list_observation_points),
    path('observation-points/<int:pk>/', views.show_observation_point_details),
    path('observations/<int:pk>/', views.add_observation),
]
