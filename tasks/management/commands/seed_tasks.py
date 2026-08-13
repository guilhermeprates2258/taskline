"""
Custom management command: seed_tasks

Populates the database with a handful of example tasks so the app has
something to show right after a fresh `python manage.py migrate`.
Run it with:

    python manage.py seed_tasks
"""

from django.core.management.base import BaseCommand
from tasks.models import Task


class Command(BaseCommand):
    help = "Creates a few sample Task rows for demo purposes."

    def handle(self, *args, **options):
        sample_tasks = [
            {
                'title': 'Set up Django project',
                'description': 'Install Django, run startproject/startapp, wire up settings.py.',
                'priority': 'HIGH',
                'status': 'DONE',
            },
            {
                'title': 'Design the Task model',
                'description': 'Add title, description, priority, status, and due_date fields.',
                'priority': 'MED',
                'status': 'DONE',
            },
            {
                'title': 'Build task list and detail pages',
                'description': 'The two dynamically generated pages required by the module.',
                'priority': 'HIGH',
                'status': 'DOING',
                'due_date': '2026-08-14',
            },
            {
                'title': 'Write README.md',
                'description': 'Document setup steps and features for the GitHub repo.',
                'priority': 'LOW',
                'status': 'TODO',
                'due_date': '2026-08-20',
            },
            {
                'title': 'Record demo video',
                'description': 'Record a 4-5 minute walkthrough of the app and the code.',
                'priority': 'HIGH',
                'status': 'TODO',
                'due_date': '2026-08-22',
            },
        ]

        created_count = 0
        for data in sample_tasks:
            _, created = Task.objects.get_or_create(title=data['title'], defaults=data)
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Created {created_count} new sample task(s).'
        ))
