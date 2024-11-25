from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .serializers import SignupSerializer,LoginSerializer
from django.contrib.auth.decorators import login_required


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
            # Login the user after successful signup
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
                messages.error(request, 'Invalid credentials, please try again.')
                return redirect('login')
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            return redirect('login')

    return render(request, 'login.html')


@login_required
def todo_page(request):
    return render(request, 'todo.html')