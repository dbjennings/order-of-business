
from django.test import TestCase
from django.urls import reverse

from apps.oob.models import Task, Project
from apps.oob.forms import TaskCreateForm
from apps.core.models import CoreUser


class TaskIndexViewTest(TestCase):

    def setUp(self):
        test_user_1 = CoreUser.objects.create_user(email='user1@test.com', password='foo')
        test_user_2 = CoreUser.objects.create_user(email='user2@test.com', password='bar')

        test_task_1 = Task.objects.create(title='Task for User1', user=test_user_1)
        test_task_2 = Task.objects.create(title='Task for User2', user=test_user_2)

        self.client.login(email='user1@test.com',)
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task-index'))
        self.assertRedirects(response, reverse('login')+'?next=/oob/task/')

    def test_success_if_logged_in(self):
        self.client.login(email='user1@test.com',password='foo')
        response = self.client.get(reverse('task-index'))

        self.assertEqual(str(response.context['user']), 'user1@test.com')
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_used(self):
        self.client.login(email='user1@test.com',password='foo')
        response = self.client.get(reverse('task-index'))

        self.assertTemplateUsed(response, 'oob/task_list.html')

    def test_user_can_only_view_their_tasks(self):
        self.client.login(email='user1@test.com',password='foo')
        response = self.client.get(reverse('task-index'))

        self.assertEqual(len(response.context['tasks']), 1)
        
        task = response.context['tasks'].get()
        self.assertEqual(task.title, 'Task for User1')


class TaskInboxViewTest(TestCase):

    def setUp(self):
        test_user_1 = CoreUser.objects.create_user(email='user1@test.com', password='foo')
        test_user_2 = CoreUser.objects.create_user(email='user2@test.com', password='bar')

        test_project = Project.objects.create(title='User Project', user=test_user_1)

        inbox_task_1 = Task.objects.create(title='Inbox Task 1', user=test_user_1)
        inbox_task_2 = Task.objects.create(title='Inbox Task 2', user=test_user_1)
        project_task = Task.objects.create(title='Project Task', user=test_user_1, project=test_project)
        other_user_task = Task.objects.create(title='User 2 Task', user=test_user_2)

        self.client.login(email='user1@test.com', password='foo')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('inbox'))
        self.assertRedirects(response, reverse('login')+'?next=/oob/task/inbox')

    def test_success_if_logged_in(self):
        response = self.client.get(reverse('inbox'))

        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        response = self.client.get(reverse('inbox'))

        self.assertTemplateUsed(response, 'oob/task_list.html')

    def test_inbox_does_not_show_project_tasks(self):
        response = self.client.get(reverse('inbox'))

        tasks = response.context['tasks']

        # Verify only test_user_1's non-project tasks were received
        self.assertEqual(tasks.count(), 2)

        # Verify the content of the tasks
        for num, task in enumerate(tasks, start=1):
            self.assertEqual(task.title, f'Inbox Task {num}')


class TaskDetailViewTest(TestCase):

    def setUp(self):
        test_user = CoreUser.objects.create_user(email='user1@test.com', password='foo')
        other_user = CoreUser.objects.create_user(email='user2@test.com', password='bar')

        self.test_project = Project.objects.create(title='User Project', user=test_user)

        self.test_task = Task.objects.create(title='Test Task', user=test_user)
        self.project_task = Task.objects.create(title='Project Task', user=test_user, project=self.test_project)
        self.other_user_task = Task.objects.create(title='User 2 Task', user=other_user)

        self.client.login(email='user1@test.com', password='foo')

    def test_user_cannot_view_other_user_task(self):
        response = self.client.get(reverse('task-detail', args=(self.other_user_task.pk,)))

        self.assertEqual(response.status_code, 403)

    def test_user_can_view_task_detail(self):
        response = self.client.get(reverse('task-detail', args=(self.test_task.pk,)))

        self.assertEqual(response.status_code, 200)

        task = response.context['task']

        self.assertEqual(task.title, 'Test Task')


class TaskCreateViewTest(TestCase):
    
    def setUp(self):
        self.test_user = CoreUser.objects.create(email='user@test.com', password='foo')
        self.test_project = Project.objects.create(title='Test Project', user=self.test_user)
        self.client.force_login(self.test_user)

    def test_get_task_create_view_failure_on_no_login(self):
        self.client.logout()

        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 302)
    
    def test_post_task_create_view_failure_on_no_login(self):
        
        self.client.logout()
        response = self.client.post(reverse('task-create'),
                                    data={'title':'Create Test Task'})
        
        self.assertEqual(response.status_code, 302)

    def test_get_task_create_view_form(self):
        response = self.client.get(reverse('task-create'))
        
        test_form = response.context['form']
        compare_form = TaskCreateForm(self.test_user)

        self.assertEqual(test_form.fields.keys(), compare_form.fields.keys())
    
    def test_post_task_create_view(self):
        response = self.client.post(reverse('task-create'),
                                            data={'title':'Create Test Task'})
        
        test_task = Task.objects.get()

        self.assertRedirects(response, reverse('task-index'))
        self.assertEqual(test_task.title, 'Create Test Task')
        self.assertEqual(test_task.user, self.test_user)


    # def test_post_task_create_view_with_project(self):
    #     response = self.client.post(reverse('task-create'),
    #                                         data={'title':'Create Test Task',
    #                                               'project': self.test_project.title,
    #                                               })
    #     print(self.test_project.user)
    #     print(response.context['user'])

    #     test_task = Task.objects.get()

    #     self.assertEqual(test_task.title, 'Create Test Task')
    #     self.assertEqual(test_task.user, self.test_user)
    #     self.assertEqual(test_task.project, self.test_project)


class TaskUpdateViewTest(TestCase):

    def setUp(self):
        self.test_user = CoreUser.objects.create(email='user@test.com', password='foo')
        self.other_user = CoreUser.objects.create(email='other@test.com', password='bar')

        self.test_task = Task.objects.create(title='Initial Title',
                                             body='Initial Body',
                                             project=None,
                                             user=self.test_user)
        self.other_task = Task.objects.create(title='Other User Task',
                                              user=self.other_user)

        self.test_project = Project.objects.create(title='Test Project',
                                                   user=self.test_user)
        self.other_project = Project.objects.create(title='Other Project',
                                                    user=self.other_user)

        self.client.force_login(self.test_user)


    def test_get_task_update_view_no_login(self):
        self.client.logout()

        response = self.client.get(reverse('task-update', args=(self.test_task.pk,)))

        self.assertEqual(response.status_code, 302)


    def test_post_task_update_view_no_login(self):
        self.client.logout()

        response = self.client.post(reverse('task-update', args=(self.test_task.pk,)),
                                    data={'title':'Final Title'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 
                             reverse('login')+'?next=/oob/task/1/update')


    def test_get_task_update_view(self):
        response = self.client.get(reverse('task-update', args=(self.test_task.id,)))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oob/task_update.html')


    def test_post_task_update_view(self):
        response = self.client.post(reverse('task-update', args=(self.test_task.pk,)),
                                    data={'title':'Final Title',
                                          'body':'Final Body',})
        
        self.test_task.refresh_from_db()

        self.assertEqual(self.test_task.title, 'Final Title')
        self.assertEqual(self.test_task.body, 'Final Body')
        self.assertRedirects(response, reverse('task-index'))


    def test_get_task_update_view_from_other_user(self):
        response = self.client.get(reverse('task-update', args=(self.other_task.pk,)))

        self.assertEqual(response.status_code, 403)


    # def test_post_task_update_view_with_project_update(self):
    #     response = self.client.post(reverse('task-update', args=(self.test_task.pk,)),
    #                                 data={'project': self.test_project})
        
    #     self.test_task.refresh_from_db()

    #     self.assertEqual(self.test_task.project, self.test_project)


class TaskCompleteViewTest(TestCase):
    
    def setUp(self):
        self.test_user = CoreUser.objects.create(email='user@test.com', password='foo')
        self.other_user = CoreUser.objects.create(email='other@test.com', password='bar')

        self.test_task = Task.objects.create(title='To Be Completed',
                                             user=self.test_user)
        self.other_task = Task.objects.create(title='Other User Task',
                                              user=self.other_user)

        self.client.force_login(self.test_user)

    def test_get_complete_view_no_login(self):
        self.client.logout()

        response = self.client.get(reverse('task-complete', args=(self.test_task.pk,)))

        self.assertRedirects(response,
                             reverse('login')+'?next=/oob/task/1/complete')

    def test_post_complete_view_no_login(self):
        self.client.logout()

        response = self.client.post(reverse('task-complete', args=(self.test_task.pk,)))

        self.assertRedirects(response,
                             reverse('login')+'?next=/oob/task/1/complete')

    def test_get_complete_view_is_update_form(self):
        response = self.client.get(reverse('task-complete', args=(self.test_task.pk,)))

        self.assertTemplateUsed(response, 'oob/task_update.html')

    def test_post_complete_view_working_toggle(self):
        response = self.client.post(reverse('task-complete', args=(self.test_task.pk,)))

        self.test_task.refresh_from_db()
        self.assertTrue(self.test_task.completed_on)

        response = self.client.post(reverse('task-complete', args=(self.test_task.pk,)))

        self.test_task.refresh_from_db()
        self.assertFalse(self.test_task.completed_on)

    def test_post_complete_view_forbidden_on_other_user_task(self):
        response = self.client.post(reverse('task-complete', args=(self.other_task.pk,)))

        self.assertEqual(response.status_code, 403)

    def test_get_complete_view_forbidden_on_other_user_task(self):
        response = self.client.get(reverse('task-complete', args=(self.other_task.pk,)))

        self.assertEqual(response.status_code, 403)

    
class TaskDeleteViewTest(TestCase):
    
    def setUp(self):
        self.test_user = CoreUser.objects.create(email='user@test.com', password='foo')
        self.other_user = CoreUser.objects.create(email='other@test.com', password='bar')

        self.test_task = Task.objects.create(title='To Be Completed',
                                             user=self.test_user)
        self.other_task = Task.objects.create(title='Other User Task',
                                              user=self.other_user)

        self.client.force_login(self.test_user)

    def test_post_delete_view_no_login(self):
        self.client.logout()

        response = self.client.post(reverse('task-delete', args=(self.test_task.pk,)))

        self.assertRedirects(response,
                             reverse('login')+'?next=/oob/task/1/delete')

    def test_post_delete_view(self):
        response = self.client.post(reverse('task-delete', args=(self.test_task.pk,)))

        with self.assertRaises(Task.DoesNotExist):
            self.test_task.refresh_from_db()
        
        self.assertRedirects(response, reverse('task-index'))

    