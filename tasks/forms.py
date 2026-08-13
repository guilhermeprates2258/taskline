"""
forms.py

Defines the web forms used to create and edit Task objects.
Using a ModelForm means Django automatically builds form fields
that match the Task model and validates the data the user submits
before it ever touches the database.
"""

from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Form used on both the 'create task' and 'edit task' pages."""

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date']
        widgets = {
            # Widgets control how each field is rendered as HTML.
            # Adding the 'form-control' class lets our CSS style every
            # field consistently without repeating markup in the template.
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Finish CSE 310 module report',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add any extra detail (optional)',
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def clean_title(self):
        """
        Custom validation: strip stray whitespace and make sure the
        title was not left blank after trimming.
        """
        title = self.cleaned_data['title'].strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title
