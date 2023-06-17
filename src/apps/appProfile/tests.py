from django.test import TestCase
from appFiles.models import File
from appProfile.models import User

class UserModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create file object to link with user

        # Create user object for testing
        cls.test_user = User.objects.create(
            login='test_user',
            password='test_password'
        )

    def test_login_field(self):
        field_label = self.test_user._meta.get_field('login').verbose_name
        self.assertEquals(field_label, 'login')

    def test_password_field(self):
        field_label = self.test_user._meta.get_field('password').verbose_name
        self.assertEquals(field_label, 'password')

    def test_icon_field(self):
        field_label = self.test_user._meta.get_field('icon').verbose_name
        self.assertEquals(field_label, 'icon')
