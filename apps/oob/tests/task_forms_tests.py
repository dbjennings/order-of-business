from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from apps.oob.models import Project
from apps.oob.forms import TaskForm
from apps.core.models import CoreUser


class TaskFormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.test_user = CoreUser.objects.create(email='user@test.com', password='foo')
        self.other_user = CoreUser.objects.create(email='other@test.com', password='bar')
        self.client.force_login(self.test_user)

        self.request = self.factory.get(reverse('task-create'))
        self.request.user = self.test_user


    def test_form_is_valid(self):

        data = {
            'title': 'Test',
            'body': '',
            'project': None,
        }

        test_form = TaskForm(request=self.request, data=data)

        self.assertTrue(test_form.is_valid())
    

    def test_form_is_invalid(self):

        data = {
            'title': '',
            'body': '',
            'project': None
        }

        test_form = TaskForm(request=self.request, data=data)
        
        self.assertFalse(test_form.is_valid())

    def test_form_has_user_projects_queryset(self):

        # Create 20 Projects for comparison
        for proj_num in range(20):
            Project.objects.create(title=f'Test{proj_num}', user=self.test_user)
        # Create one project not owned by test_user
        Project.objects.create(title='Test', user=self.other_user)

        data = {
            'title': 'Test',
            'body': '',
            'project': None,
        }

        test_form = TaskForm(request=self.request, data=data)

        test_queryset = test_form.fields['project'].queryset
        compare_queryset = Project.objects.filter(user=self.test_user)

        self.assertEqual(test_queryset.first(), compare_queryset.first())
        self.assertEqual(test_queryset.count(), compare_queryset.count())