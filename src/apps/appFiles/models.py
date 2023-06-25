import os
import uuid
from django.db import models
from ..utils.Uploader import Uploader
from io import BytesIO
from PIL import Image
from django.core.files import File as DjangoFile
from django.utils.translation import gettext_lazy as _


def compress_image(image: DjangoFile) -> DjangoFile:
    """
    Сжимает указанный файл изображения.

    Args:
        image (DjangoFile): Файл изображения для сжатия.

    Returns:
        DjangoFile: Сжатый файл изображения.
    """
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=70)
    new_image = DjangoFile(im_io, name=image.name)
    return new_image


def upload_to(instance: 'File', filename: str) -> str:
    """
    Преобразует поле 'url_to_upload' в имя файла.

    Args:
        instance (File): Экземпляр модели File.
        filename (str): Оригинальное имя файла.

    Returns:
        str: Преобразованное имя файла.
    """
    relative_path = instance.url_to_upload.find(instance.directory)
    return instance.url_to_upload[relative_path:]


class File(models.Model):
    directory = models.CharField(max_length=50, default='', verbose_name=_('directory'))
    local_url = models.FileField(upload_to=upload_to, verbose_name=_('local URL'))
    url_to_upload = models.CharField(max_length=200, default='', verbose_name=_('URL to Upload'))

    @staticmethod
    def upload(id_user: int, file: DjangoFile, extension: str, is_commit: bool = True) -> 'File':
        """
        Загружает файл на сервер и создает экземпляр модели File.

        Args:
            id_user (int): Идентификатор пользователя.
            file (DjangoFile): Файл для загрузки.
            extension (str): Расширение файла.
            is_commit (bool, optional): Определяет, нужно ли сохранить экземпляр в базе данных. По умолчанию True.

        Returns:
            File: Созданный экземпляр модели File.
        """
        directory = f"user_{id_user}"
        if extension.lower() in ('jpg', 'jpeg', 'png'):
            extension = 'JPEG'
        image_name = File.get_uuid_name_with_extension(extension)
        file_path = Uploader.get_path(directory, image_name)
        print(directory)
        file_instance = File(directory=directory, local_url=file, url_to_upload=str(file_path))
        if is_commit:
            file_instance.save()
        return file_instance

    def save(self, *args, **kwargs):
        """
        Переопределяет метод save для сжатия файла изображения, если его расширение поддерживается.
        """
        if self.local_url.name is not None and self.local_url.name.lower().endswith(('jpg', 'jpeg', 'png')):
            self.local_url = compress_image(self.local_url)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """
        Удаляет файл из хранилища.
        """
        self.local_url.delete()
        super().delete(using=using, keep_parents=keep_parents)

    @staticmethod
    def get_uuid_name_with_extension(extension: str) -> str:
        """
        Генерирует уникальное имя файла с указанным расширением.

        Args:
            extension (str): Расширение файла.

        Returns:
            str: Сгенерированное имя файла.
        """
        uuid_name = uuid.uuid4().hex
        return f"{uuid_name}.{extension}"

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
        ordering = ("directory",)
