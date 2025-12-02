from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Task
from .forms import SignUpForm, TaskForm


class SignUpView(View):
    """User registration view"""
    template_name = 'todo/signup.html'
    form_class = SignUpForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """User login view"""
    template_name = 'todo/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please fill in all fields.")
        
        return render(request, self.template_name)


class LogoutView(View):
    """User logout view"""
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, "You have been logged out successfully.")
        return redirect('home')


class HomeView(ListView):
    """Home page with task list and search"""
    model = Task
    template_name = 'todo/home.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Task.objects.none()
        
        queryset = Task.objects.filter(user=self.request.user).order_by('-created')
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(assigned_to__icontains=query)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_tasks = Task.objects.filter(user=self.request.user)
            context['total_tasks'] = user_tasks.count()
            context['pending_tasks'] = user_tasks.filter(status='pending').count()
            context['completed_tasks'] = user_tasks.filter(status='completed').count()
        else:
            context['total_tasks'] = 0
            context['pending_tasks'] = 0
            context['completed_tasks'] = 0
        
        context['query'] = self.request.GET.get('q', '')
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Create new task"""
    model = Task
    form_class = TaskForm
    template_name = 'todo/add_task.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    """Task detail view"""
    model = Task
    template_name = 'todo/task_detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing task"""
    model = Task
    form_class = TaskForm
    template_name = 'todo/update_task.html'
    pk_url_kwarg = 'task_id'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'task_id': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """Delete task"""
    model = Task
    template_name = 'todo/delete_task.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'task_id'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Task deleted successfully!")
        return super().delete(request, *args, **kwargs)
