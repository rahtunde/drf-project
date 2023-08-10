from rest_framework.test import APITestCase
from authentication.models import User


class TestModel(APITestCase):
    def test_create_user(self):
        user = User.objects.create_user('caddse123', 'sfcswf@gmail.com', 'shn253626!')

        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'sfcswf@gmail.com' )

    

    def test_raises_error_when_no_username_is_supplied(self):

        self.assertRaises(ValueError, User.objects.create_user, email='vafsxasg@gmail.com', username='', password='svgvsawsw')
    

    def test_raises_error_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given username must be set"):
            User.objects.create_user(username='', email='vafsxasg@gmail.com', password='svgvsawsw')


    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, email='', username='sgvxsavvxsa', password='scfsaahsax')

    
    def test_raises_error_with_message_when_no_email_is_supplied(self):
       with self.assertRaisesMessage(ValueError, "The given username must be set"):
           User.objects.create_user(email='', username='sgvxsavvxsa', password='scfsaahsax')
           
    
    def test_create_super_user_with_status_user_status(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(username='sgvxsavvxsa', email='svgsdsag@gmail.com', password='sgvxsavvxsa', is_staff=False)

    def test_create_super_user_with_status_user_status_is_superuser_false(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):
            User.objects.create_superuser(username='sgvxsavvxsa', email='svgsdsag@gmail.com', password='sgvxsavvxsa', is_superuser=False)


    def test_create_super_user(self):
        user = User.objects.create_superuser('dsfsdssa', 'dsfshsh@gmail.com', 'fasctagc4')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email,  'dsfshsh@gmail.com')

