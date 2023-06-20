import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from apps.appProfile.models import PersonalInfo
from apps.appFiles.models import File
from config.settings import MEDIA_ROOT
from .managers import CustomUserManager
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, unique=True, verbose_name=_('username'))
    email = models.EmailField(null=True, unique=True, verbose_name=_('email'))
    is_staff = models.BooleanField(default=False, verbose_name=_('staff status'))
    is_active = models.BooleanField(default=True,verbose_name=_('active status'))
    date_joined = models.DateTimeField(default=timezone.now)
    icon = models.ForeignKey('appFiles.File', on_delete=models.SET_NULL, null=True, related_name='icon',
                             verbose_name=_('icon'))

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @staticmethod
    def create_user_with_personal_info(username: str, password: str, email: str):
        """
        Создает объекты User и PersonalInfo и возвращает их в кортеже.

        Args:
            login (str): логин пользователя\n
            password (str): пароль пользователя\n
            email (str): адрес электронной почты пользователя

        Returns:
            tuple: кортеж из созданных объектов User и PersonalInfo
        """
        user = CustomUser.objects.create_user(username, password, email)
        personal_info = PersonalInfo.objects.create(user=user)
        return user, personal_info

    def delete(self, using=None, keep_parents=False):
        """
        Удаляет пользователя и все загруженные пользователем файлы.
        """
        directory = f'user_{self.id}'
        file_instances = File.objects.filter(directory=directory)
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
        super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ("username",)
