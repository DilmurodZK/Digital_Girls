from django.urls import path
from .views import *


urlpatterns = [
    path("", home_view, name='dashboard-url'),
    path("slider/", slider_view, name='slider-url'),
    path("create-slider/", create_slider, name='create-slider-url'),
    path("activate-slider/<int:pk>/", activate_slider, name="activate-slider-url"),
    path("delete-slider/<int:pk>/", delete_slider, name="delete-slider-url"),
]