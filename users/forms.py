from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# форма реєстрації - розширюємо стандартну джанго форму
class RegisterForm(UserCreationForm):
    # додаємо вибір ролі при реєстрації
    role = forms.ChoiceField(
        choices=[('student', 'Студент'), ('teacher', 'Викладач')],
        label='Я є'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
        labels = {
            'username': 'Імʼя користувача',
            'email': 'Email',
        }