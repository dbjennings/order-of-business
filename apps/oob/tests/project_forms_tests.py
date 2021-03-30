from django.http import request
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from apps.oob.models import Project
from apps.oob.forms import ProjectForm
from apps.core.models import CoreUser


class ProjectFormTest(TestCase):

    def setUp(self):
        self.test_user = CoreUser.objects.create(email='user@test.com', password='foo')
        self.other_user = CoreUser.objects.create(email='other@test.com', password='bar')
        self.client.force_login(self.test_user)

        self.factory = RequestFactory()
        self.request = self.factory.get(reverse('task-create'))
        self.request.user = self.test_user
        
    def test_project_form_is_valid(self):

        data = {
            'title': 'Test',
            'body': '',
            'parent': None,
        }

        test_form = ProjectForm(request=self.request, data=data)

        self.assertTrue(test_form.is_bound)
        self.assertTrue(test_form.is_valid())

    def test_project_form_is_invalid(self):

        data = {
            'title': '',
            'body': '',
            'parent': None,
        }

        test_form = ProjectForm(request=self.request, data=data)

        self.assertTrue(test_form.is_bound)
        self.assertFalse(test_form.is_valid())

    def test_project_form_has_user_projects_queryset(self):

        for proj_num in range(3):
            Project.objects.create(title=f'Test{proj_num}', user=self.test_user)
        
        for sub_proj_num in range(3):
            Project.objects.create(title=f'Sub-Test{sub_proj_num}',
                                   user = self.test_user,
                                   parent = Project.objects.first())
        
        Project.objects.create(title='Other', user=self.other_user)

        data = {
            'title': 'Test'
        }

        test_form = ProjectForm(request=self.request, data=data)

        test_queryset = test_form.fields['parent'].queryset
        compare_queryset = Project.objects.filter(user=self.test_user,
                                                  parent=None)
        
        self.assertEqual(test_queryset.first(), compare_queryset.first())
        self.assertEqual(test_queryset.count(), compare_queryset.count())