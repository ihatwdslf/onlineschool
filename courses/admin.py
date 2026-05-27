from django.contrib import admin
from .models import Course, Lesson, Quiz, Question, Answer, Enrollment, LessonProgress

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)