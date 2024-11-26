from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import SignupSerializer,LoginSerializer,TodoSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo.html', {
        'user': request.user,
        'todos': todos,
    })
    
@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        Todo.objects.create(title=title, description=description, user=request.user)
    return redirect('todo')

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.completed = not task.completed  # Toggle completion status
        task.save()
    return redirect('todo')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('todo')


# class TodoListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         todos = Todo.objects.filter(user=request.user)
#         serializer = TodoSerializer(todos, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = TodoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TodoDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk, user):
#         try:
#             return Todo.objects.get(pk=pk, user=user)
#         except Todo.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         todo = self.get_object(pk, request.user)
#         if not todo:
#             return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = TodoSerializer(todo)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         todo = self.get_object(pk, request.user)
#         if not todo:
#             return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = TodoSerializer(todo, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         todo = self.get_object(pk, request.user)
#         if not todo:
#             return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
#         todo.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
