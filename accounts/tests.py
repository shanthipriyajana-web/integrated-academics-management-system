from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class SwitchAccountFlowTests(TestCase):
    def setUp(self):
        self.assistant = User.objects.create_user(
            email='assistant@vsu.edu',
            password='Admin@123',
            full_name='Assistant User',
            role='assistant',
        )
        self.student = User.objects.create_user(
            email='student@vsu.edu',
            password='Student@123',
            full_name='Student User',
            role='student',
        )

    def test_switch_account_signs_out_current_user(self):
        self.client.force_login(self.assistant)

        response = self.client.post(
            reverse('login'),
            {'action': 'switch_account'},
            follow=True,
        )

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_switch_account_allows_login_as_different_role(self):
        self.client.force_login(self.assistant)

        self.client.post(reverse('login'), {'action': 'switch_account'})
        response = self.client.post(
            reverse('login'),
            {
                'action': 'login',
                'username': self.student.email,
                'password': 'Student@123',
            },
        )

        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.student.pk)