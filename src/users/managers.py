from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Менеджер пользователей для пользовательской модели пользователя,
    """

    def create_user(self, username: str, email: str, password: str, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным логином, email и паролем.

        Args:
            username (str): Логин пользователя.
            email (str): Email пользователя.
            password (str): Пароль пользователя.
            extra_fields : Дополнительные поля пользователя.
        Returns:
            user (User): Созданный экземпляр модели пользователя.
        """
        if not username:
            raise ValueError(_("Необходимо указать логин"))
        if not email:
            raise ValueError(_("Необходимо указать email"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,  username: str, email: str, password: str, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным логином, email и паролем.

        Args:
            username (str): Логин пользователя.
            email (str): Email пользователя.
            password (str): Пароль пользователя.
            extra_fields : Дополнительные поля пользователя.
        Returns:
            user (User): Созданный экземпляр модели суперпользователя .
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_superuser=True."))
        return self.create_user(username, email, password, **extra_fields)
