
import pprint
import os
from django.test import TestCase
from config.settings import MEDIA_ROOT
from ..utils.Uploader import Uploader
from django.core.files.base import ContentFile
from ..appProfile.models import User 
from .models import File
from pathlib import Path 
import pprint



class FileTestCase(TestCase):

    file_data = b'west_file_data'
    extension = 'txt'
    test_user = User.objects.create(login='test_user',password='test_password')
    test_user.save()


    @classmethod
    def tearDownClass(cls):
        file_instances = File.objects.filter(user=cls.test_user)
        for file_instance in file_instances:
            try:
                file_instance.delete()
            except Exception as e:
                print(f"Error while deleting file instance: {e}")
        try:
            os.rmdir(os.path.join(MEDIA_ROOT, f'user_{cls.test_user.id}'))
        except Exception as e:
            print(f"Error while deleting directory: {e}")
        cls.test_user.delete()



    def test_file_upload(self):
        file_instance = File.upload(self.test_user, ContentFile(self.file_data,name='adasdas.txt'), self.extension)
        self.assertTrue(file_instance.url_to_upload != '')
        with open(file_instance.local_url.name, 'rb') as f:
            self.assertEqual(self.file_data, f.read())
        file_instance.delete()
    
    def test_get_uuid_name_with_extension(self):
        extension = 'jpg'
        uuid_name = File.get_uuid_name_with_extension(extension)
        self.assertEqual(len(uuid_name), 33 + len(extension))
        self.assertEqual(uuid_name.count('.'), 1)
        self.assertTrue(uuid_name.endswith(extension))


