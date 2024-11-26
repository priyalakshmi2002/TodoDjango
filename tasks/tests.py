from django.test import TestCase
from django.urls import reverse
from .serializers import SignupSerializer
from django.contrib.auth.models import User
from tasks.models import Todo

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
          
    def test_signup_valid_emial_fields(self):
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

class TodoTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Create initial tasks
        self.task1 = Todo.objects.create(title="Task 1", completed=False, user=self.user)
        self.task2 = Todo.objects.create(title="Task 2", completed=True, user=self.user)

    def test_todo_page_loads(self):
        """Testing the structure of the todo page"""
        response = self.client.get(reverse('todo'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Your Todo List")
        self.assertContains(response, "<h1>Welcome to Your Todo List</h1>", html=True)

        # Check if the form for adding tasks exists
        self.assertContains(response, '<input type="text" name="title" placeholder="Task Title" required>', html=False)
        self.assertContains(response, '<textarea name="description" placeholder="Task Description (optional)"></textarea>', html=False)
        self.assertContains(response, '<button type="submit">Add Task</button>', html=False)

    def test_add_task(self):
        """ Test to add new task"""
        response = self.client.post(reverse('add_task'), {
            'title': 'New Task',
            'description': 'Description of the new task'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after creation
        self.assertTrue(Todo.objects.filter(title='New Task').exists())

    def test_update_task(self):
        """Test to update a new task"""
        response = self.client.post(reverse('update_task', args=[self.task1.id]), {
            'title': 'Updated Task 1',
            'description': 'Updated description',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after update
        updated_task = Todo.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.title, 'Updated Task 1')

    def test_toggle_task_completion(self):
        """Test to toggle a task to completed"""
        response = self.client.post(reverse('update_task', args=[self.task1.id]))
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)  # Completion status should toggle

    def test_delete_task(self):
        """Test to delete a task"""
        response = self.client.post(reverse('delete_task', args=[self.task2.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        self.assertFalse(Todo.objects.filter(id=self.task2.id).exists())

    def test_list_tasks(self):
        """Test to list all the tasks"""
        response = self.client.get(reverse('todo'))
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Task 2")

