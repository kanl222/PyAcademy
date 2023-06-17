from io import BufferedReader
import uuid
import os
from django.db import models
from ..utils.Uploader import Uploader
from config.settings import MEDIA_URL
from django.core.files import File as File_
from django.http.request import HttpRequest

def upload_to(instance:'File', filename:str) -> str:
    """Функция конвертирует url_to_upload в имя файла

    Args:
        instance (File): экземпляр модели Picture
        filename (str): имя файла

    Returns:
        str: имя файла из относительного пути
    """
    relative_path = instance.url_to_upload.find('media') + 6
    return instance.url_to_upload[relative_path:]


class File(models.Model):
    user = models.ForeignKey('appProfile.User', on_delete=models.CASCADE, related_name="user")
    local_url = models.FileField(upload_to=upload_to)
    url_to_upload = models.CharField(max_length=200, default='')
    
    @staticmethod
    def upload(user:'User', file, extension: str) -> 'File':
        """Метод загружает файла на сервер

        Args:
            User (User): пользователь
            file (bytes): байт файла
            extension (str): тип расширения

        Returns:
            Picture: созданный экземпляр модели Picture
        """
        owner = f'user_{user.id}'
        image_name = str(uuid.uuid4().hex)
        file_path = Uploader.get_path(owner, extension, image_name)

        picture = File.objects.create(user=user,local_url = file,url_to_upload=str(file_path))
        picture.save()
        return picture

    def delete(self, using=None, keep_parents=False):
        """Метод удаляет файла

        Args:
            using (type, optional): опциональный аргумент. По умолчанию None.
            keep_parents (bool, optional): наследуемый. По умолчанию False.
        """
        self.local_url.delete()
        super().delete(using=using, keep_parents=keep_parents)

    @staticmethod
    def get_uuid_name_with_extension(extension: str) -> str:
        """Метод возвращает имя файла из уникального идентификатора с расширением

        Args:
            image (bytes): байт изображения

        Returns:
            str: имя файла
        """
        return f"{uuid.uuid4().hex}.{extension}"
