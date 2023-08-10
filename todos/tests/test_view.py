from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from todos.models import Todo


class TodosAPITestCase(APITestCase):
    
    def create_todo(self):
        create_data= {
            'title':'hello world',
            'description': 'This is a testing'
        }

        response = self.client.post(reverse('list-create'), create_data )

        return response
    
    def authenticate(self):
        self.client.post(reverse('register'), {
            'username':'username',
            'email': 'email@gmail.com',
            'password':'password1234'
        })
        response = self.client.post(reverse('login'), {'email': 'email@gmail.com',
            'password':'password1234'})
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")



class TestListCreateTodos(TodosAPITestCase):
    
    def test_should_not_creat_todos_if_user_not_auth(self):
        response = self.create_todo()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_todos(self):
        self.authenticate()

        response = self.create_todo()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.all().count(), 1)
        self.assertEqual(response.data['title'], 'hello world')
        self.assertEqual(response.data['description'], 'This is a testing')
    
    def test_retrieve_all_todos(self):

        self.authenticate()

        response= self.client.get(reverse('list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

        
        self.create_todo()

        response = self.client.get(reverse('list-create'))

        self.assertIsInstance(response.data['count'], int)
        self.assertEqual(response.data['count'], 1)


class TestTodoUpdate(TodosAPITestCase):

    def test_retrieve_one_item(self):
        self.authenticate()
        response = self.create_todo()
        
        new_response = self.client.get(reverse('update', kwargs= {'id': response.data['id']}))

        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
        
        todo = Todo.objects.get(id=response.data['id'])

        self.assertEqual(todo.title, response.data['title'])

    def test_update_one_item(self):
        self.authenticate()
        response = self.create_todo()

        patch_data = {'title': 'new Title', 
                      'is_complete': True}

        new_response = self.client.patch(reverse('update', kwargs={'id': response.data['id']}), patch_data)

        self.assertEqual(new_response.status_code, status.HTTP_200_OK)

        update_todo = Todo.objects.get(id=response.data['id'])

        self.assertEqual(update_todo.is_complete, True)
        self.assertEqual(update_todo.title, 'new Title')


    def test_delete_one_item(self):
        self.authenticate()

        response = self.create_todo()

        next_db_count = Todo.objects.all().count()

        self.assertGreater(next_db_count, 0)
        self.assertEqual(next_db_count, 1)

        new_response = self.client.delete(reverse('update', kwargs={'id': response.data['id']}))

        self.assertEqual(new_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.all().count(), 0)

    