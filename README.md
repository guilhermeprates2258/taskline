# Overview

As a software engineer, I wanted to get hands-on experience building a dynamic, database-backed web application using a modern server-side framework instead of only static HTML/CSS/JS. I chose Django (Python) because it is widely used in industry, has a gentle learning curve for someone who already knows Python, and demonstrates the full request/response cycle of a real web app: routing, views, templates, forms, and an ORM-backed database.

**Taskline** is a task management web app. It lets a user create, view, search, filter, edit, and delete tasks, and each task is stored permanently in a SQLite database through Django's ORM.

To run it locally:

1. Clone this repository and `cd` into the project folder.
2. (Recommended) Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Apply the database migrations: `python manage.py migrate`
5. (Optional) Load a few sample tasks: `python manage.py seed_tasks`
6. Start the development server: `python manage.py runserver`
7. Open a browser to **http://127.0.0.1:8000/** to see the task list (home page).

My purpose in writing this software was to practice building a complete CRUD (Create, Read, Update, Delete) application with Django: designing a data model, wiring up URLs and views, building HTML templates that render dynamic content, handling form submissions and validation, and persisting data in a relational database.

[Software Demo Video](https://www.loom.com/share/11ec4f7c71744bccb2eb844cbd93fc17)

# Web Pages

The app has three dynamically generated pages, plus a confirmation page, all served from Python view functions in `tasks/views.py`:

* **Home / Task List (`/`)** — Queries every `Task` row from the database and renders it as a list of "ledger entries." The content is generated dynamically from whatever tasks currently exist. This page is interactive: a search box filters tasks by title/description, filter pills narrow the list by status (`?status=DONE`, etc.), and a status "dot" button lets the user advance a task's status (To Do → In Progress → Done) without leaving the page.
* **Task Detail (`/task/<id>/`)** — Looks up a single task by its database ID (taken from the URL) and displays its full title, description, priority, status, and timestamps. Links from here lead to editing or deleting that specific task.
* **Add / Edit Task (`/task/new/` and `/task/<id>/edit/`)** — The third dynamically generated page (fulfilling the "additional (third) page" option, on top of database integration). Both routes reuse the same template and `TaskForm`; on `GET` it shows a blank or pre-filled form, and on `POST` it validates and saves the data to the database before redirecting to the task's detail page.
* **Delete Confirmation (`/task/<id>/delete/`)** — A small safety page shown before a task is permanently removed from the database, to avoid accidental deletions from a stray click.

Navigation between pages happens through standard links and form submissions: the home page links to detail pages, detail pages link to edit/delete, and successful create/edit actions redirect back to the relevant detail page.

# Development Environment

* **Editor:** Visual Studio Code
* **Version control:** Git and GitHub
* **Language:** Python 3
* **Framework:** Django 5.2 (LTS)
* **Database:** SQLite (Django's default database backend, accessed through Django's built-in ORM)
* **Other tools:** Django's built-in development server (`manage.py runserver`) and admin site (`/admin/`) for quick data inspection while developing

# Useful Websites

* [Django Documentation](https://docs.djangoproject.com/en/5.0/)
* [Django Official Tutorial (writing your first app)](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
* [Django ModelForm Reference](https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/)
* [MDN Web Docs — Django Web Framework](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)
* [Wikipedia — Django (web framework)](https://en.wikipedia.org/wiki/Django_(web_framework))

# Future Work

* Add user accounts/authentication so each user only sees their own tasks.
* Add sorting options (by due date, priority, or creation date) on the home page.
* Add pagination for when the task list grows large.
* Add automated unit tests for the views and forms.
* Improve accessibility (ARIA labels, better keyboard navigation for the status toggle button).
