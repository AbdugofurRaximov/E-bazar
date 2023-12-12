from django.test import TestCase
from django.urls import reverse
from .models import CustomUser
from django.contrib.auth import get_user



class SignupTestCase(TestCase):

    def test_signup_view(self):
        response = self.client.post(
            reverse('users:signup'),
            data={
                'first_name': 'Abdugofur',
                'username': 'Admin123',
                'email': 'admin@gmail.com',
                'password1': "admin11111",
                'password2': 'admin11111',
            }
        )

        user = CustomUser.objects.get(username='Admin123')
        self.assertEqual(user.first_name, 'Abdugofur')
        self.assertEqual(user.email, 'admin@gmail.com')
        self.assertTrue(user.check_password('admin11111'))


        #profile test
        second_response = self.client.get("/users/profile/Admin123")
        self.assertEqual(second_response.status_code, 200)

        #login test

        self.client.login(username='Admin123', password="admin11111")

        # update
        third_response = self.client.post(
            reverse('users:update'),
            data={
                'username': 'Admin1234',
                "first_name": 'Abdugofur1',
                'last_name': 'Raximov',
                'email': 'Adminqwwe@gmail.com',
                'phone_number': '+998998712337',
                'tg_username': 'users',
            }
        )
        user = get_user(self.client)
        print(user.is_authenticated)
        self.assertEqual(third_response.status_code, 302)
        self.assertEqual(user.phone_number, '+998998712337')
        self.assertEqual(user.first_name, 'Abdugofur1')
        self.assertNotEqual(user.first_name, 'Abdugofur')


