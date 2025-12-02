from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'time_required', 'assigned_to','due_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'time_required': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3 hours'}),
            'assigned_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ali'}),
            'due_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

