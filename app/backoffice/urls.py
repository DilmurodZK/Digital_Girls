from django.urls import path
from .views import *


urlpatterns = [
    # URL for Dashboard
    path("sign-in/", signin_view, name="login-url"),
    path("log-out/", logout_view, name="logout-url"),
    path("password/", password_view, name="password-url"),
    path("", home_view, name='dashboard-url'),
    path("search/", search_view, name="search-url"),
    # URLs for Contact
    path("contact/", contact_view, name='contact-url'),
    path("create-contact/", create_contact_view, name='create-contact-url'),
    path("update-contact/<int:pk>/", update_contact_view, name="update-contact-url"),
    path("delete-contact/<int:pk>/", delete_contact_view, name='delete-contact-url'),
    # URLs for Info
    path("info/", info_view, name='info-url'),
    path("create-info/", create_info_view, name='create-info-url'),
    path("update-info/<int:pk>/", update_info_view, name="update-info-url"),
    path("delete-info/<int:pk>/", delete_info_view, name='delete-info-url'),
    # URLs for Application
    path("application/", application_view, name='application-url'),
    path('export-write-xls', export_write_xls, name='export-write-xls-url'),
    # URLs for Slider
    path("slider/", slider_view, name='slider-url'),
    path("create-slider/", create_slider_view, name='create-slider-url'),
    path("edit-slider/", edit_slider_view, name='edit-slider-url'),
    path("activate-slider/<int:pk>/", activate_slider_view, name="activate-slider-url"),
    path("delete-slider/<int:pk>/", delete_slider_view, name="delete-slider-url"),
    # URLs for Result & ResultItem
    path("result/", result_view, name="result-url"),
    path("delete-result/<int:pk>/", delete_result_view, name="delete-result-url"),
    path("create-result/", create_result_view, name="create-result-url"),
    path("update-result/", update_result_view, name="update-result-url"),
    path("delete-resultitem/<int:pk>/", delete_resultitem_view, name="delete-resultitem-url"),
    path("create-resultitem/", create_resultitem_view, name="create-resultitem-url"),
    path("update-resultitem/", update_resultitem_view, name="update-resultitem-url"),
    path("activate-resultitem/<int:pk>/", activate_resultitem_view, name="activate-resultitem-url"),
    path("resultitem-modal/<int:pk>/", resultitem_modal_view, name="resultitem-modal-url"),
    # URLs for Task
    path("task/", task_view, name="task-url"),
    path("delete-task/<int:pk>/", delete_task_view, name="delete-task-url"),
    path("delete-taskitem/<int:pk>/", delete_taskitem_view, name="delete-taskitem-url"),
    path("create-task/", create_task_view, name="create-task-url"),
    path("update-task/", update_task_view, name="update-task-url"),
    path("create-taskitem/", create_taskitem_view, name="create-taskitem-url"),
    path("update-taskitem/", update_taskitem_view, name="update-taskitem-url"),
    path("activate-taskitem/<int:pk>/", activate_taskitem_view, name="activate-taskitem-url"),
    path("taskitem-modal/<int:pk>/", taskitem_modal_view, name="taskitem-modal-url"),
    # URLs for Course
    path("course/", course_view, name="course-url"),
    path("course/item/", course_item_view, name="course-item-url"),
    path("delete-course/<int:pk>/", delete_course_view, name="delete-course-url"),
    path("delete-courseitem/<int:pk>/", delete_courseitem_view, name="delete-courseitem-url"),
    path("create-course/", create_course_view, name="create-course-url"),
    path("update-course/", update_course_view, name="update-course-url"),
    path("create-courseitem/", create_courseitem_view, name="create-courseitem-url"),
    path("update-courseitem/", update_courseitem_view, name="update-courseitem-url"),
    path("activate-courseitem/<int:pk>/", activate_courseitem_view, name="activate-courseitem-url"),
    path("courseitem-modal/<int:pk>/", courseitem_modal_view, name="courseitem-modal-url"),
    # URLs for About
    path("about/", about_view, name="about-url"),
    path("about/item/", about_item_view, name="about-item-url"),
    path("delete-about/<int:pk>/", delete_about_view, name="delete-about-url"),
    path("delete-aboutitem/<int:pk>/", delete_aboutitem_view, name="delete-aboutitem-url"),
    path("create-about/", create_about_view, name="create-about-url"),
    path("update-about/", update_about_view, name="update-about-url"),
    path("create-aboutitem/", create_aboutitem_view, name="create-aboutitem-url"),
    path("update-aboutitem/", update_aboutitem_view, name="update-aboutitem-url"),
    path("activate-aboutitem/<int:pk>/", activate_aboutitem_view, name="activate-aboutitem-url"),
    path("aboutitem-modal/<int:pk>/", aboutitem_modal_view, name="aboutitem-modal-url"),
]