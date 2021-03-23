from apps.oob.models import project
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from unittest import mock
from datetime import timedelta

from ..models import Project, Task

class ProjectModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(email='user@test.com', password='foo')

        self.main_project = Project.objects.create(title='Test Project', user=self.user)
        self.sub_project = Project.objects.create(title='Sub Project', user=self.user, parent=self.main_project)

        self.main_task = self.main_project.tasks.create(title='Main Project Task', user=self.user)
        self.sub_task = self.sub_project.tasks.create(title='Sub Project Task', user=self.user)

    def test_project_string_representation(self):
        self.assertEqual(str(self.main_project), self.main_project.title)

    def test_project_verbose_name_plural(self):
        self.assertEqual(Project._meta.verbose_name_plural, 'projects')

    def test_project_with_no_user(self):
        with self.assertRaises(ValidationError):
            Project.objects.create(title='No User Project')
    
    def test_project_with_no_title(self):
        with self.assertRaises(ValidationError):
            Project.objects.create(user=self.user)
        with self.assertRaises(ValidationError):
            Project.objects.create(title='', user=self.user)
    
    def test_project_create_invalid_task(self):
        with self.assertRaises(ValidationError):
            self.main_project.tasks.create(user=self.user)

    def test_project_cannot_be_its_own_parent(self):
        with self.assertRaises(ValidationError):
            self.main_project.parent = self.main_project
            self.main_project.save()
    
    def test_project_task_addition_methods(self):
        # Create a new task via Project.tasks
        task_1 = self.main_project.tasks.create(title='One', user=self.user)
        # Create a new task and add it to Project.tasks
        task_2 = Task.objects.create(title='Two', user=self.user)
        self.main_project.tasks.add(task_2)
        # Create a new task and set its project
        task_3 = Task.objects.create(title='Three', user=self.user, project=self.main_project)

        self.assertEqual(task_1.project, task_2.project, task_3.project)

    def test_project_sub_project_addition_methods(self):
        # Create a sub-project through the parent project
        sub_1 = self.main_project.children.create(title='One', user=self.user)
        # Create a sub-project and add it to the parent project's children
        sub_2 = Project.objects.create(title='Two', user=self.user)
        self.main_project.children.add(sub_2)
        # Create a sub-project and set its parent project
        sub_3 = Project.objects.create(title='Three', user=self.user, parent=self.main_project)

        # All children have the same parent
        self.assertEqual(sub_1.parent, sub_2.parent, sub_3.parent)

        # Parent contains each child
        self.assertEqual(self.main_project.children.filter(title='One').get(),
                         sub_1)
        self.assertEqual(self.main_project.children.filter(title='Two').get(),
                         sub_2)
        self.assertEqual(self.main_project.children.filter(title='Three').get(),
                         sub_3)
    
    def test_project_sub_project_cannot_be_child_of_sub_project(self):
        with self.assertRaises(ValidationError):
            self.sub_project.children.create(title='Sub-Sub-Project', user=self.user)

    def test_project_sub_project_cannot_have_parent_and_children(self):
        with self.assertRaises(ValidationError):
            new_main = Project.objects.create(title='New Main Project')
            new_main.children.add(self.main_project)

    def test_project_modified_date_updated(self):
        yesterday = timezone.now() - timedelta(days=1)

        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=yesterday)):
            old_project = Project.objects.create(title='Yesterday', user=self.user)
        
        initial_date = old_project.modified_on

        old_project.title = "Today"
        old_project.save()

        modified_date = old_project.modified_on

        self.assertNotEqual(initial_date, modified_date)    