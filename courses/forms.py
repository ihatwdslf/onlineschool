from django import forms
from .models import Course, Lesson, Quiz, Question, Answer


# форма створення курсу
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'cover']
        labels = {
            'title': 'Назва курсу',
            'description': 'Опис',
            'cover': 'Обкладинка',
        }


# форма додавання уроку
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'youtube_url', 'order']
        labels = {
            'title': 'Назва уроку',
            'youtube_url': 'Посилання на YouTube відео',
            'order': 'Порядковий номер',
        }


# форма створення тесту
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']
        labels = {
            'title': 'Назва тесту',
        }


# форма додавання питання
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        labels = {
            'text': 'Текст питання',
        }