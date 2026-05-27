from django.contrib.auth.models import AbstractUser
from django.db import models


# розширюємо стандартну модель юзера джанго
# додаємо роль - викладач або студент
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Викладач'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # коротко про себе

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'

    def __str__(self):
        return f'{self.username} ({self.role})'