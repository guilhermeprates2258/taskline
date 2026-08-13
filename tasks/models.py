"""
models.py

Defines the database structure for the Task Management app.
Django turns each class below into a table in the SQLite database
(see DATABASES in task_manager/settings.py). Every time the model
changes, we generate a migration with:

    python manage.py makemigrations
    python manage.py migrate
"""

from django.db import models
from django.urls import reverse


class Task(models.Model):
    """A single to-do item that a user wants to track."""

    # Choices restrict a field to a fixed set of valid values.
    # The first item in each tuple is stored in the database,
    # the second item is the human-readable label shown on screen.
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MED', 'Medium'),
        ('HIGH', 'High'),
    ]

    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('DOING', 'In Progress'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(
        max_length=100,
        help_text="Short name for the task."
    )
    description = models.TextField(
        blank=True,
        help_text="Optional details about what needs to be done."
    )
    priority = models.CharField(
        max_length=4,
        choices=PRIORITY_CHOICES,
        default='MED',
        help_text="How urgent this task is."
    )
    status = models.CharField(
        max_length=5,
        choices=STATUS_CHOICES,
        default='TODO',
        help_text="Current progress of the task."
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Optional deadline for the task."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # Set once, automatically, when the row is first created.
        help_text="Timestamp of when the task was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # Updated automatically every time the row is saved.
        help_text="Timestamp of the last edit."
    )

    class Meta:
        # Newest / most urgent tasks appear first by default.
        ordering = ['status', '-priority', 'due_date']

    def __str__(self):
        """String shown in the Django admin and shell (e.g. Task.objects.all())."""
        return self.title

    def get_absolute_url(self):
        """
        Central place that defines where a Task 'lives'.
        Used by templates and by generic views after a successful
        create/update to redirect the user to the detail page.
        """
        return reverse('tasks:task_detail', kwargs={'pk': self.pk})

    @property
    def is_done(self):
        """Convenience flag used in templates to style completed tasks differently."""
        return self.status == 'DONE'
