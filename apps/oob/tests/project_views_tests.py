from typing import List
from django.db.models.query import EmptyQuerySet, QuerySet
from django.utils.functional import empty
from apps.oob.forms.project_forms import ProjectForm
from django.http import response
from django.test import TestCase, RequestFactory
from django.urls.base import reverse

from http import HTTPStatus

from apps.oob.models import Task, Project
from apps.core.models import CoreUser


class ProjectIndexViewTest(TestCase):
    
    def setUp(self):
        self.test_user = CoreUser.objects.create_user(email='user1@test.com', password='foo')
        self.other_user = CoreUser.objects.create_user(email='user2@test.com', password='bar')
        self.client.force_login(self.test_user)

        for proj_num in range(10):
            Project.objects.create(title=f'Project{proj_num}', user=self.test_user)
        Project.objects.create(title='Other Project', user=self.other_user)

        self.response = self.client.get(reverse('project-index'))

    def test_project_index_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('project-index'))
        self.assertRedirects(response,
                             reverse('login')+'?next=/oob/project/')

    def test_project_index_correct_template_used(self):
        self.assertTemplateUsed(self.response, 'oob/project_index.html')

    def test_project_index_is_only_user_projects(self):
        index = self.response.context['projects']
        self.assertEqual(index.count(), 10)


class ProjectDetailViewTest(TestCase):

    def setUp(self):
        self.test_user = CoreUser.objects.create_user(email='user1@test.com', password='foo')
        self.other_user = CoreUser.objects.create_user(email='user2@test.com', password='bar')
        self.client.force_login(self.test_user)

        self.test_project = Project.objects.create(title='Project', user=self.test_user)
        self.other_project = Project.objects.create(title='Other Project', user=self.other_user)

        self.response = self.client.get(reverse('project-detail', args=(self.test_project.pk,)))
    
    def test_project_detail_no_login(self):
        self.client.logout()
        response = self.client.get(reverse('project-detail',args=(self.test_project.pk,)))
        self.assertRedirects(response,
                             reverse('login')+f'?next=/oob/project/{self.test_project.pk}/')
    
    def test_project_detail_user_can_view_own_project(self):
        project = self.response.context['project']

        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(project.title, 'Project')

    def test_project_detail_user_cannot_view_others_project(self):
        response = self.client.get(reverse('project-detail', 
                                           args=(self.other_project.pk,)))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        

class ProjectCreateViewTest(TestCase):

    def setUp(self):
        self.test_user = CoreUser.objects.create_user(email='user1@test.com', password='foo')
        self.other_user = CoreUser.objects.create_user(email='user2@test.com', password='bar')
        self.client.force_login(self.test_user)

    def test_get_project_create_view_failure_no_login(self):
        self.client.logout()
        response = self.client.get(reverse('project-create'))
        self.assertRedirects(response,
                             reverse('login')+'?next=/oob/project/create')

    def test_post_project_create_view_failure_no_login(self):
        self.client.logout()
        response = self.client.post(reverse('project-create'))
        self.assertRedirects(response,
                             reverse('login')+'?next=/oob/project/create')

    def test_get_project_create_view_form(self):
        response = self.client.get(reverse('project-create'))

        test_form = response.context['form']

        self.assertEqual(tuple(test_form.fields.keys()), ('title','body','parent'))

    def test_post_project_create_view(self):
        response = self.client.post(reverse('project-create'),
                                    data={'title':'Test'})
        test_project = Project.objects.get()

        self.assertRedirects(response, reverse('project-index'))
        self.assertEqual(test_project.title, 'Test')
        self.assertEqual(test_project.user, self.test_user)

    def test_post_project_create_view_form_is_invalid(self):
        response = self.client.post(reverse('project-create'))

        self.assertContains(response, 'This field is required.')


class ProjectUpdateViewTest(TestCase):

    def setUp(self):
        self.test_user = CoreUser.objects.create(email='user@test.com', password='foo')
        self.other_user = CoreUser.objects.create(email='other@test.com', password='bar')
        self.client.force_login(self.test_user)

        self.test_project_1 = Project.objects.create(title='Test Project 1',
                                                     user=self.test_user)
        self.test_project_2 = Project.objects.create(title='Test Project 2',
                                                     user=self.test_user)
        self.test_sub_project = Project.objects.create(title='Test Project 1',
                                                       user=self.test_user,
                                                       parent=self.test_project_1)
        self.other_project = Project.objects.create(title='Other Project',
                                                    user=self.other_user)

    def test_project_update_view_no_login(self):
        '''Tests both GET and POST requests'''
        self.client.logout()

        response_1 = self.client.get(reverse('project-update',
                                             args=(self.test_project_1.pk,)))
        response_2 = self.client.post(reverse('project-update',
                                              args=(self.test_project_1.pk,)))

        self.assertEqual(response_1.status_code, HTTPStatus.FOUND)
        self.assertEqual(response_2.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response_1,
                             reverse('login')+'?next=/oob/project/1/update')
        self.assertRedirects(response_2,
                             reverse('login')+'?next=/oob/project/1/update')
        self.assertEqual(response_1.content, response_2.content)                             

    def test_project_update_view_get_form(self):
        response = self.client.get(reverse('project-update',
                                           args=(self.test_project_1.pk,)))
        test_form = response.context['form']

        self.assertIsInstance(test_form, ProjectForm)

    def test_project_update_view_post_form(self):

        data = {
            'title': 'Updated Title',
        }
        response = self.client.post(reverse('project-update',
                                            args=(self.test_project_1.pk,)),
                                            data=data)
        self.test_project_1.refresh_from_db()

        self.assertEqual(self.test_project_1.title, 'Updated Title')
        self.assertRedirects(response,reverse('project-index'))

    def test_project_update_view_fails_from_other_user(self):
        response_1 = self.client.get(reverse('project-update',
                                             args=(self.other_project.pk,)))
        response_2 = self.client.post(reverse('project-update',
                                              args=(self.other_project.pk,)))
        
        self.assertEqual(response_1.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response_2.status_code, HTTPStatus.NOT_FOUND)

    def test_project_update_view_switch_sub_project_parent(self):
        data = {
            'title': self.test_sub_project.title,
            'parent': self.test_project_2.pk
        }
        response = self.client.post(reverse('project-update',
                                            args=(self.test_sub_project.pk,)),
                                            data=data)
        self.test_project_1.refresh_from_db()
        self.test_project_2.refresh_from_db()
        self.test_sub_project.refresh_from_db()

        self.assertRedirects(response, reverse('project-index'))
        self.assertEqual(self.test_project_1.children.all().count(), 0)
        self.assertEqual(self.test_project_2.children.get(), self.test_sub_project)
        self.assertEqual(self.test_sub_project.parent, self.test_project_2)

class ProjectDeleteViewTest(TestCase):

    def setUp(self):
        self.test_user = CoreUser.objects.create(email='user@test.com', password='foo')
        self.other_user = CoreUser.objects.create(email='other@test.com', password='bar')
        self.client.force_login(self.test_user)

        self.test_project = Project.objects.create(title='To Be Deleted',
                                                   user=self.test_user)
        self.test_sub_project = Project.objects.create(title='A Victim of Cascade',
                                                       user=self.test_user,
                                                       parent=self.test_project)                                           
        self.other_project = Project.objects.create(title='To Be Deleted',
                                                    user=self.other_user)
        self.test_task = Task.objects.create(title='Also A Victim of Cascade',
                                             user=self.test_user,
                                             project=self.test_project)

    def test_project_delete_view_no_login(self):
        '''Tests both GET and POST requests'''
        self.client.logout()

        response_1 = self.client.get(reverse('project-delete',
                                             args=(self.test_project.pk,)))
        response_2 = self.client.post(reverse('project-delete',
                                              args=(self.test_project.pk,)))

        self.assertEqual(response_1.status_code, HTTPStatus.FOUND)
        self.assertEqual(response_2.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response_1,
                             reverse('login')+'?next=/oob/project/1/delete')
        self.assertRedirects(response_2,
                             reverse('login')+'?next=/oob/project/1/delete')
        self.assertEqual(response_1.content, response_2.content)
    
    def test_project_delete_view_get(self):
        response = self.client.get(reverse('project-delete',
                                           args=(self.test_project.pk,)))
        self.assertTemplateUsed(response,'oob/project_delete.html')
    
    def test_project_delete_view_fails_other_user_project(self):
        response = self.client.get(reverse('project-delete',
                                           args=(self.other_project.pk,)))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_project_delete_view_post(self):
        response = self.client.post(reverse('project-delete',
                                            args=(self.test_project.pk,)))
        
        self.assertRedirects(response, reverse('project-index'))
        with self.assertRaises(Project.DoesNotExist):
            self.test_project.refresh_from_db()
        with self.assertRaises(Project.DoesNotExist):
            self.test_sub_project.refresh_from_db()
        with self.assertRaises(Task.DoesNotExist):
            self.test_task.refresh_from_db()

        