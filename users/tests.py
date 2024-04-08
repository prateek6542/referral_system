# users/tests.py

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserProfile

class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'referral_code': 'abcd1234'  # Optional field
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify if user is created in the database
        self.assertTrue(User.objects.filter(username='testuser').exists())

class UserDetailsTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, referral_code='abcd1234')

    def test_user_details(self):
        # Authenticate the test user
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify if user details are returned correctly
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

class ReferralsTestCase(APITestCase):
    def setUp(self):
        # Create test users and user profiles
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='testpassword1')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword2')
        self.user_profile1 = UserProfile.objects.create(user=self.user1, referral_code='abcd1234')
        self.user_profile2 = UserProfile.objects.create(user=self.user2, referral_code='abcd1234')

    def test_referrals(self):
        # Authenticate one of the test users
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/referrals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify if the correct referrals are returned
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser2')
        self.assertEqual(response.data[0]['email'], 'test2@example.com')
