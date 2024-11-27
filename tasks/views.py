from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import SignupSerializer,LoginSerializer
from django.contrib.auth.decorators import login_required
from .models import Todo

def signup(request):
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password1': request.POST.get('password1'),
            'password2': request.POST.get('password2'),
        }

        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=data['username'])
            login(request, user)
            return redirect('login')  
        else:
            return render(request, 'signup.html', {
                'errors': serializer.errors,
                'form_data': data,
            })

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.POST)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('todo')
            else:
                # Add authentication error message
                return render(request, 'login.html', {
                    'form_data': request.POST,
                    'errors': {'non_field_errors': ["Invalid username or password."]}
                })

        # Validation errors from the serializer
        return render(request, 'login.html', {
            'form_data': request.POST,
            'errors': serializer.errors,
        })

    return render(request, 'login.html', {
        'form_data': {},
        'errors': {}
    })
    
@login_required
def todo_page(request):
    edit_task_id = request.GET.get('edit_task_id')
    edit_task = None
    if edit_task_id:
        edit_task = get_object_or_404(Todo, id=edit_task_id, user=request.user)

    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo.html', {
        'todos': todos,
        'edit_task': edit_task,  # Pass the task for pre-filling the form
    })

@login_required
def add_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')  # Check if task_id is provided
        if task_id:  # Update existing task
            task = get_object_or_404(Todo, id=task_id, user=request.user)
            task.title = request.POST.get('title', task.title)
            task.description = request.POST.get('description', task.description)
            task.save()
        else:  # Add new task
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            Todo.objects.create(title=title, description=description, user=request.user)
        return redirect('todo')

    # Render the task list with an empty form for adding new tasks
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo.html', {'todos': todos})

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, user=request.user)
    if request.method == 'POST':
        task.completed = not task.completed  # Toggle completion
        task.save()
    return redirect('todo')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('todo')

