"""
views.py

Each function here is a "view": it receives an incoming HTTP request,
talks to the database through the Task model, and returns an HTTP
response — usually by rendering an HTML template with some context
data. urls.py maps each URL pattern to one of these functions.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Task
from .forms import TaskForm


def task_list(request):
    """
    Home page (Requirement: dynamically generated HTML page #1).

    Displays every task and lets the user interactively filter the
    list using the search box and status buttons in the URL's query
    string, e.g. /?status=TODO or /?q=report. Because the page's
    content changes based on that user input, this also fulfills the
    'interactive functionality' requirement.
    """
    tasks = Task.objects.all()

    # Read optional query-string parameters submitted by the user.
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    if search_query:
        # Q objects let us search more than one field with a single OR query.
        tasks = tasks.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Task.STATUS_CHOICES,
        'total_count': Task.objects.count(),
        'done_count': Task.objects.filter(status='DONE').count(),
    }
    return render(request, 'tasks/task_list.html', context)


def task_detail(request, pk):
    """
    Task details page (Requirement: dynamically generated HTML page #2).

    'pk' (primary key) comes from the URL, e.g. /tasks/3/, and is used
    to look up exactly one Task row. get_object_or_404 automatically
    returns a friendly 404 page if no task with that id exists.
    """
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_create(request):
    """
    Handles the 'add a new task' form.

    GET  -> show a blank form.
    POST -> validate the submitted data and, if valid, save a new
            Task row to the SQLite database (database integration
            requirement) then redirect to that task's detail page.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" was created.')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'heading': 'Add a New Task',
        'button_label': 'Create Task',
    })


def task_edit(request, pk):
    """
    Handles editing an existing task. Works the same way as
    task_create, except the form is pre-filled with (instance=task)
    the row that already exists in the database.
    """
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" was updated.')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'heading': f'Edit "{task.title}"',
        'button_label': 'Save Changes',
        'task': task,
    })


def task_delete(request, pk):
    """
    Confirms and performs deletion of a task.

    GET  -> show a confirmation page (so a task is never deleted by
            accident from a stray click or a search engine crawler).
    POST -> the user confirmed, so remove the row from the database.
    """
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" was deleted.')
        return redirect('tasks:task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def task_toggle_status(request, pk):
    """
    Small interactive helper used by the 'quick complete' button on the
    home page: cycles a task through To Do -> In Progress -> Done
    without needing to open the full edit form.
    """
    task = get_object_or_404(Task, pk=pk)
    next_status = {'TODO': 'DOING', 'DOING': 'DONE', 'DONE': 'TODO'}
    task.status = next_status[task.status]
    task.save()
    return redirect(request.META.get('HTTP_REFERER', 'tasks:task_list'))
