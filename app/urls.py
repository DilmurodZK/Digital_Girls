from django.urls import path
from .views import *


urlpatterns = [
    path('contact/', contact),
    path("course/", course),
    path("course-item/", course_item),
    path('info/', info),
    path('slider/', slider),
    path("about/", about),
    path("about-item/", about_item),
    path("task/", task),
    path("task-item/", task_item),
    path("result/", result),
    path("result-item/", result_item),
    path("create-application/",create_application),
]