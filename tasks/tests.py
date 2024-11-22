from django.test import TestCase, Client
from django.urls import reverse

class SignupPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')  # URL name for the signup page

    def test_signup_page_accessible(self):
        """Test if the signup page is accessible via the URL."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "<h1>Sign Up</h1>") 
    def test_signup_page_form(self):
        """Test if the signup form renders correctly with required fields."""
        response = self.client.get(self.signup_url)
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')  
        self.assertContains(response, 'name="confirm_password"')  
        self.assertContains(response, '{% csrf_token %}')  




