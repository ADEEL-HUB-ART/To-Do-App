from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add/', views.TaskCreateView.as_view(), name='add_task'),
    path('task/<int:task_id>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:task_id>/update/', views.TaskUpdateView.as_view(), name='update_task'),
    path('task/<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='delete_task'),
]
