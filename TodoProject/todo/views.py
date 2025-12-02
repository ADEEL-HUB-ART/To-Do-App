from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import SignUpForm, TaskForm

# Sign up View

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'todo/signup.html', {'form': form})

# Login View

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Logged in successfully .")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'todo/login.html')

# Logout View

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')

# Home Page

# def home(request):
#     tasks = Task.objects.all()
#     return render(request, 'todo/home.html', {'tasks': tasks})

@login_required
def home(request):
    query = request.GET.get('q')
    tasks = Task.objects.filter(user=request.user)

    if query:
        tasks = tasks.filter(title__icontains=query)

    return render(request, 'todo/home.html', {'tasks': tasks, 'query': query})



@login_required
def add_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'todo/add_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect('home')



@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'todo/task_detail.html', {'task': task})


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # if task.user != request.user:
    #     messages.error(request, "You do not have permission to edit this task.")
    #     return redirect('home')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'todo/update_task.html', {'form': form, 'task': task})


