from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from unittest import mock
from datetime import timedelta

from ..models import Task, Project

class TaskModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='user@test.com', password='foo')

        self.task = Task(title='Test Task', user=self.user)

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), self.task.title)

    def test_task_verbose_name_plural(self):
        self.assertEqual(Task._meta.verbose_name_plural, 'tasks')
    
    def test_task_with_no_user(self):
        with self.assertRaises(ValidationError):
            Task.objects.create(title="Test Task 2")

    def test_task_with_no_title(self):
        with self.assertRaises(ValidationError):
            Task.objects.create(title='', user=self.user)
            Task.objects.create(user=self.user)

    def test_task_modified_date_updated(self):
        yesterday = timezone.now() - timedelta(days=1)

        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=yesterday)):
            old_task = Task.objects.create(title='Yesterday', user=self.user)
        
        initial_date = old_task.modified_on

        old_task.title = "Today"
        old_task.save()

        modified_date = old_task.modified_on

        self.assertNotEqual(initial_date, modified_date)
