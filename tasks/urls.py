"""
urls.py (app-level)

Maps URL patterns that belong to the 'tasks' app to the view
functions in views.py. This file is included by the project-level
task_manager/urls.py.
"""

from django.urls import path
from . import views

app_name = 'tasks'  # Namespace so we can write tasks:task_detail etc. in templates.

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/toggle/', views.task_toggle_status, name='task_toggle_status'),
]
