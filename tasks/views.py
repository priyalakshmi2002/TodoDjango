from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import SignupSerializer, LoginSerializer, TodoSerializer
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
                return render(request, 'login.html', {
                    'form_data': request.POST,
                    'errors': {'non_field_errors': ["Invalid username or password."]}
                })

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
        'edit_task': edit_task,
    })

@login_required
def add_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description', ''),
            'completed': request.POST.get('completed', 'false') == 'true',  # Handle completion as a boolean
            'user': request.user.id,
        }

        if task_id:
            task = get_object_or_404(Todo, id=task_id, user=request.user)
            data['user'] = task.user.id
            serializer = TodoSerializer(task, data=data)
        else:
            serializer = TodoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return redirect('todo')
        else:
            todos = Todo.objects.filter(user=request.user)
            return render(request, 'todo.html', {
                'todos': todos,  
                'form_data': data,
                'errors': serializer.errors,
            })

    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo.html', {
        'todos': todos,
    })

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, user=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
    return redirect('todo')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('todo')

@login_required
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('login') 
