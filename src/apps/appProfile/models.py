from django.db import models
from django.utils.translation import gettext_lazy as _

class PersonalInfo(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name="personal_info")
    first_name = models.CharField(max_length=250, null=True, default=None, verbose_name=_("first name"))
    last_name = models.CharField(max_length=250, null=True, default=None, verbose_name=_("last name"))
    patronymic = models.CharField(max_length=250, null=True, default=None, verbose_name=_("patronymic"))
    date_of_birth = models.DateField(null=True, default=None, verbose_name=_("date of birth"))
    telephone = models.CharField(max_length=20, null=True, unique=True, verbose_name=_("telephone"))

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def full_name(self) -> str:
        """
        Возвращает полное имя объекта в формате "Фамилия Имя Отчество".

        Returns:
            str: Полное имя объекта.
        """
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    class Meta:
        verbose_name = _("personal info")
        verbose_name_plural = _("personal info")


class Notification(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name="notifications", verbose_name=_("user"))
    text = models.TextField(verbose_name=_("text"))
    type = models.CharField(max_length=50, verbose_name=_("type"))
    link = models.URLField(null=True, verbose_name=_("link"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("date"))

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
