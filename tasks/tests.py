from django.test import TestCase
from django.urls import reverse
from .serializers import SignupSerializer
from django.urls import reverse
from django.contrib.auth.models import User



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

    def test_signup_existing_username(self):
        """
        Testing the validation of the signup fields for unique username input 
        """
        from django.contrib.auth.models import User
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

class LoginPageTests(TestCase):        
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
        

class LoginTests(TestCase):

    def setUp(self):
        """Create a test user for login testing"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_successful_login_redirects_to_todo(self):
        """Test that a successful login redirects to the todo page"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        # Check if the user is redirected to the 'todo' page after successful login
        self.assertRedirects(response, reverse('todo'))
        # Check if the user is authenticated (logged in)
        self.assertTrue(self.client.login(username='testuser', password='testpassword'))

    def test_invalid_username_or_password(self):
        """Test that invalid credentials return an error message"""
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword',
        })
        # Check if the user is redirected back to the login page
        self.assertRedirects(response, reverse('login'))
        # Check if the error message is shown
        self.assertContains(response, 'Invalid credentials, please try again.')

    def test_missing_username(self):
        """Test that login fails when the username is missing"""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': 'testpassword',
        })
        # Check if the error message for the missing username is shown
        self.assertContains(response, 'Both fields are required.')

    def test_missing_password(self):
        """Test that login fails when the password is missing"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '',
        })
        # Check if the error message for the missing password is shown
        self.assertContains(response, 'Both fields are required.')

    def test_missing_both_username_and_password(self):
        """Test that login fails when both username and password are missing"""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': '',
        })
        # Check if the error message for missing fields is shown
        self.assertContains(response, 'Both fields are required.')

    def test_invalid_username(self):
        """Test that login fails when the username is incorrect"""
        response = self.client.post(reverse('login'), {
            'username': 'nonexistentuser',
            'password': 'testpassword',
        })
        # Check if the error message for invalid credentials is shown
        self.assertContains(response, 'Invalid credentials, please try again.')

    def test_invalid_password(self):
        """Test that login fails when the password is incorrect"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        # Check if the error message for invalid credentials is shown
        self.assertContains(response, 'Invalid credentials, please try again.')

    def test_error_message_for_login_validation(self):
        """Test that error messages are shown for invalid login"""
        # Simulate missing password (without providing a password)
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '',
        })
        # Check if the error message about missing fields is shown
        self.assertContains(response, 'Both fields are required.')



