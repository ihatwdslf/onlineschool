from django.db import models
from users.models import User


# сам курс - створює викладач
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# урок всередині курсу - посилання на ютуб відео
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()  # просто посилання на відео
    order = models.PositiveIntegerField(default=0)  # порядковий номер уроку

    class Meta:
        ordering = ['order']  # уроки завжди відсортовані по порядку

    def __str__(self):
        return f'{self.course.title} — {self.title}'


# тест до уроку
class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'Тест: {self.lesson.title}'


# одне питання в тесті
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text


# варіант відповіді на питання
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)  # правильна чи ні

    def __str__(self):
        return self.text


# запис студента на курс
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # один студент не може записатись на один курс двічі
        unique_together = ['student', 'course']

    def __str__(self):
        return f'{self.student.username} -> {self.course.title}'


# прогрес - які уроки студент вже переглянув
class LessonProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'lesson']

    def __str__(self):
        return f'{self.student.username} — {self.lesson.title}'