from django.db import models


class User(models.Model):
    login = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    icon = models.ForeignKey('appFiles.File', on_delete=models.SET_NULL, null=True, related_name="users")

    def __str__(self):
        return self.login

    @staticmethod
    def create_user_with_personal_info(login: str, password:str, email:str):
        """
        Создает объекты User и PersonalInfo и возвращает их в кортеже.

        Args:
            login (str): логин пользователя\n
            password (str): пароль пользователя\n
            email (str): адрес электронной почты пользователя

        Returns:
            tuple: кортеж из созданных объектов User и PersonalInfo
        """
        user = User.objects.create(login=login, password=password)
        personal_info = PersonalInfo.objects.create(user=user, email=email)
        return user, personal_info



    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class PersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personal_info")
    first_name = models.CharField(max_length=250,null=True)
    last_name = models.CharField(max_length=250,null=True)
    patronymic = models.CharField(max_length=250,null=True)
    date_of_birth = models.DateField(null=True)
    telephone = models.CharField(max_length=20,null=True)
    email = models.EmailField(null=True)

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
        verbose_name = "Персональная информация"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    text = models.TextField()
    type = models.CharField(max_length=50)
    link = models.URLField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
