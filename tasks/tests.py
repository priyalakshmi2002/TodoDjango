from django.test import TestCase
from django.urls import reverse
from .serializers import SignupSerializer
from django.contrib.auth.models import User
from tasks.models import Todo
from django.test import Client

class SignupPageTests(TestCase):
    def test_signup_page_renders_correctly(self):
        """
        Ensures the signup page renders correctly.
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_html_structure(self):
        """
        Testing if the signup page contains the expected HTML elements.
        """
        response = self.client.get(reverse('signup'))
        self.assertContains(response, '<h1>Sign In</h1>', html=True, status_code=200)
        self.assertContains(response, '<form', status_code=200)
        self.assertContains(response, '<input', status_code=200)
        self.assertContains(response, 'type="text"', status_code=200)
        self.assertContains(response, 'type="email"', status_code=200)
        self.assertContains(response, 'type="password"', status_code=200)
        self.assertContains(response, 'csrfmiddlewaretoken', status_code=200) 
        self.assertContains(response, '<label for="username">Username</label>', html=True)
        self.assertContains(response, '<label for="email">Email</label>', html=True)
        self.assertContains(response, '<label for="password1">Password</label>', html=True)
        self.assertContains(response, '<label for="password2">Confirm Password</label>', html=True)
        self.assertContains(response,' <button type="submit" class="btn">Sign in</button>',html=True)
        self.assertContains(response, 'href="/auth/login/"') 
        
    def test_signup_valid_data(self):
        """
        Testing the successful validation of the signup fields with valid data
        """
        data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'password123',
        'password2': 'password123',
        }
        serializer = SignupSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('login'))

    def test_signup_password_mismatch(self):
        """
        Testing the validation of the signup fields with mismatch of password
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password321',
        }
        serializer = SignupSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password2', serializer.errors)
        self.assertEqual(serializer.errors['password2'][0], "Passwords do not match")

    def test_signup_missing_fields(self):
        """
        Testing the validation of the signup fields with empty input
        """
        data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
        }
        serializer = SignupSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertEqual(serializer.errors['email'][0], 'This field is required.')
          
    def test_signup_valid_email_fields(self):
        """
        Testing the validation of the signup email with invalid email input
        """
        data = {
            'username': 'testuser',
            'email': 'test2137',
            'password1': 'password123',
            'password2': 'password123',
        }
        serializer = SignupSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertEqual(serializer.errors['email'][0], 'Enter a valid email address.')

    def test_signup_existing_username(self):
        """
        Testing the validation of the signup fields for unique username input 
        """
        User.objects.create_user(username='testuser', email='test@example.com', password='password123')

        data = {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        serializer = SignupSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertEqual(serializer.errors['username'][0], "A user with that username already exists.")

    def test_signup_existing_email(self):
        """
        Testing the validation of the signup fields for unique email-id as input 
        """
        from django.contrib.auth.models import User
        User.objects.create_user(username='anotheruser', email='test@example.com', password='password123')

        data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        serializer = SignupSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertEqual(serializer.errors['email'][0], "A user with this email already exists")
        
    def test_signup_password_strength(self):
        """
        Testing the validation of password strength
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'pass',
            'password2': 'pass',
        }
        serializer = SignupSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password1', serializer.errors)
        self.assertEqual(serializer.errors['password1'][0], "Password must be at least 6 characters long")

class LoginTests(TestCase):
    def test_login_page_renders_correctly(self):
        """
        Ensure the login page renders correctly.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_page_html_structure(self):
        """
        Testing the html structure of the login page.
        """
        response = self.client.get(reverse('login'))
        self.assertContains(response, '<h1>Login</h1>', html=True, status_code=200)
        self.assertContains(response, '<form', status_code=200)
        self.assertContains(response, '<input', status_code=200)
        self.assertContains(response, 'type="text"', status_code=200)
        self.assertContains(response, 'type="password"', status_code=200)
        self.assertContains(response, 'csrfmiddlewaretoken', status_code=200) 
        self.assertContains(response, '<label for="username">Username</label>', html=True)
        self.assertContains(response, '<label for="password">Password</label>', html=True)
        self.assertContains(response,' <button type="submit" class="btn">Login</button>',html=True)
        self.assertContains(response, 'href="/auth/signup/"') 
    
    def setUp(self):
        """Create a test user for login testing"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_successful_login_redirects_to_todo_no_errors(self):
        """Test that a successful login redirects to the todo page"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        },
        follow=True)
        self.assertRedirects(response, reverse('todo'))
        self.assertTrue(self.client.login(username='testuser', password='testpassword'))
        self.assertNotContains(response, "Username is required.")
        self.assertNotContains(response, "Password is required.")
        self.assertNotContains(response, "Invalid username or password.")
            
    def test_missing_username_error(self):
        """
        Test that an error message is displayed when the username is missing.
        """
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': 'testpassword',
        })
        self.assertContains(response, "Username is required.")
        self.assertEqual(response.status_code, 200)

    def test_missing_password_error(self):
        """
        Test that an error message is displayed when the password is missing.
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '',
        })
        self.assertContains(response, "Password is required.")
        self.assertEqual(response.status_code, 200)

    def test_invalid_credentials_error(self):
        """
        Test that an error message is displayed for invalid credentials.
        """
        response = self.client.post(reverse('login'), {
            'username': 'jqskdj',
            'password': 'wrongpassword'
        })
        self.assertContains(response, "Invalid username or password.")
        self.assertEqual(response.status_code, 200)

class TodoAppTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="otheruser", password="password123")
        self.client.login(username="testuser", password="password123")

        # Create tasks for the test user
        self.task1 = Todo.objects.create(title="Task 1", description="Description 1", user=self.user,completed=False)
        self.task2 = Todo.objects.create(title="Task 2", description="Description 2", user=self.user, completed=True)
        
        # Create a task for the other user
        self.other_task = Todo.objects.create(title="Other Task", description="Other Description", user=self.other_user)

    def test_todo_html_structure(self):
        """Test for successful login and the html structure of the todo page"""
        response = self.client.get(reverse('todo'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Your Todo List')
        self.assertContains(response, "Logged in as: <strong>testuser</strong>", html=True)
        self.assertContains(response, '<form', status_code=200)
        self.assertContains(response, '<input', status_code=200)
        self.assertContains(response, 'type="text"', status_code=200)
        self.assertContains(response, '<textarea name="description"',status_code=200)
        self.assertContains(response, '<button type="submit">Add Task</button>')
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')
        self.assertContains(response, 'Done')
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Delete')
        self.assertContains(response, f'href="{reverse("todo")}?edit_task_id={self.task1.id}"')
        self.assertContains(response, f'action="{reverse("delete_task", args=[self.task1.id])}"')
        self.assertContains(response, f'action="{reverse("toggle_task", args=[self.task1.id])}"')
        
    def test_add_task(self):
        """Test for adding task in the todo form"""
        response = self.client.post(reverse('add_task'), {'title': 'New Task', 'description': 'New Description'})
        self.assertEqual(response.status_code, 302)  # Should redirect back to the todo page
        self.assertTrue(Todo.objects.filter(title="New Task", user=self.user).exists())
   
    def test_update_task(self):
        """Test for updating the existing task in the todo form"""
        update_url = reverse('todo') + f'?edit_task_id={self.task1.id}'
        # Perform the GET request to pre-fill the form
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Task')  # Ensure we see the Edit form
        update_data = {
            'title': 'Updated Task 1',
            'description': 'Updated Description 1',
            'task_id': self.task1.id,
        }
        response = self.client.post(reverse('add_task'), update_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task 1')
        self.assertEqual(self.task1.description, 'Updated Description 1')
    
    def test_toggle_completed(self):
        """Testing the toggle and completed status of the task"""
        response = self.client.post(reverse('toggle_task', args=[self.task1.id]), {
            'toggle_completed': '1',
        })
        self.assertEqual(response.status_code, 302)
        toggle_task = Todo.objects.get(id=self.task1.id)
        self.assertTrue(toggle_task.completed)  # Task should now be marked as completed

    def test_delete_task(self):
        """Testing the deletion of a task from the todo list"""
        response = self.client.post(reverse('delete_task', args=[self.task1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(id=self.task1.id).exists())  # Task should be deleted

    def test_tasks_are_user_specific(self):
        """Testing the lists of tasks displayed of that particular user logged in"""
        response = self.client.get(reverse('todo'))
        self.assertEqual(response.status_code, 200)
        tasks = response.context['todos']
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)
        self.assertNotIn(self.other_task, tasks)  # Tasks from other users should not appear
        
    def test_edit_task_missing_title(self):
        todo = Todo.objects.create(title='Test Task', description='Test description', user=self.user)
        response = self.client.post(reverse('add_task'), {
            'task_id': todo.id,
            'title': '',  # Empty title
            'description': 'Updated description'
        })
        self.assertContains(response, 'This field may not be blank.')

    
    def test_logout_redirects_to_login(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('todo'))
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))   
