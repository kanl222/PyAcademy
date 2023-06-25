import os
from config.settings import MEDIA_ROOT
from django.test import TestCase
from django.core.files.base import ContentFile
from users.models import CustomUser
from .models import File


class FileTestCase(TestCase):

    def setUp(self):
        self.file_data = b'test_file_data'
        self.extension = 'txt'
        self.test_user = CustomUser.objects.create_user(username='test_user',
                                                   email='kan3l22fdd@gamil.co',
                                                   password='test_password')
        self.directory = f"user_{self.test_user.id}"

    def tearDown(self):
        file_instances = File.objects.filter(directory=self.directory)
        for file_instance in file_instances:
            try:
                file_instance.delete()
            except Exception as e:
                print(f"Error while deleting file instance: {e}")

        user_directory = os.path.join(MEDIA_ROOT, f'user_{self.test_user.id}')
        if os.path.exists(user_directory):
            try:
                os.rmdir(user_directory)
            except Exception as e:
                print(f"Error while deleting directory: {e}")

        self.test_user.delete()

    def test_file_upload(self):
        file_instance = File.upload(id_user=self.test_user.id, file=ContentFile(self.file_data, name='test_file.txt'),
                                    extension=self.extension)
        self.assertTrue(file_instance.url_to_upload != '')
        with open(file_instance.local_url.path, 'rb') as f:
            self.assertEqual(self.file_data, f.read())

    def test_file_delete(self):
        file_instance = File.upload(id_user=self.test_user.id, file=ContentFile(self.file_data, name='test_file.txt'),
                                    extension=self.extension)
        path = file_instance.local_url.path
        file_instance.delete()
        self.assertFalse(os.path.exists(path))

    def test_get_uuid_name_with_extension(self):
        extension = 'jpg'
        uuid_name = File.get_uuid_name_with_extension(extension)
        self.assertEqual(len(uuid_name), 33 + len(extension))
        self.assertEqual(uuid_name.count('.'), 1)
        self.assertTrue(uuid_name.endswith(extension))
