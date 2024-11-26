from django.urls import path
from . import views
# from .views import TodoListView, TodoDetailView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('todo/', views.todo_page, name='todo'),
    path('add-task/', views.add_task, name='add_task'),
    path('update-task/<int:task_id>/', views.update_task, name='update_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),

]

