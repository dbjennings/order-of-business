from django.test import TestCase
from django.contrib.auth import get_user_model

class UserManagerTest(TestCase):

    def test_create_user(self):
        
        # Create a CoreUser object
        User = get_user_model()
        user = User.objects.create_user(email='user@test.com', password='foo')

        # Check attributes against expected values
        self.assertEqual(user.email, 'user@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Check successful nullification of CoreUser.username
        self.assertIsNone(user.username)

        # Check for expected error messages
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo')

    def test_create_superuser(self):

        # Create a CoreUser object
        User = get_user_model()
        user = User.objects.create_superuser(email='user@test.com', password='foo')

        # Check attributes against expected values
        self.assertEqual(user.email, 'user@test.com')
        self.assertTrue(user.is_active)        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        # Check successful nullification of CoreUser.username
        self.assertIsNone(user.username)

        # Check for expected error messages
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='user@test.com',
                                          password='foo',
                                          is_staff=False)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='user@test.com',
                                          password='foo',
                                          is_superuser=False)