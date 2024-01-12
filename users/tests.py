from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class SignUpTestCase(TestCase):
    def test_signup_view(self):
        response = self.client.post(
            reverse('users:signup'),
            data={
                'firstname': 'Muhammadalixon',
                'Username': 'muhammadalixon',
                'email': 'muhammadalixonabdullayev40@gmail.com',
                'password1': 'alixon1212',
                'password2': 'alixon1212'
            }
        )
        user = CustomUser.objects.get(username='muhammadalixon')
        self.assertEqual(user.firstname, 'Muhammadalixon')
        self.assertEqual(user.email, 'muhammadalixonabdullayev40@gmail.com')
        self.assertTrue(user.check_password('alixon1212'),)

        second_responce = self.client.get("user/profile/muhammadalixon")
        self.assertEqual(second_responce.status_code, 200)

        self.client.login(username='akbarjon', password='chalamulla')

        third_response = self.client.post(
            reverse('users:update'),
            data={
                'username': 'muhammadlixon',
                'first_name': 'Muhammadalixon',
                'email': 'muhammadalixonabdullayev40@gmail.com',
                'phone_number': '8941795268',
                'tg_username': 'alixon1212',
                })
        user = get_user(self.client)
        print(user.is_authenticated)
        self.assertEqual(third_response.status_code, 302)
        self.assertEqual(user.phone_number, '8941795268')
        self.assertEqual(user.first_name, 'Muhammadalixon')
        self.assertNotEqual(user.first_name, 'muhammadalixon')
