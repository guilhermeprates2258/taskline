"""
admin.py

Registers the Task model with Django's built-in admin site so tasks
can also be viewed/edited at /admin/ (useful for quick debugging and
data entry while developing).
"""

from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'due_date', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')
