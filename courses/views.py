from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Course, Lesson, Enrollment, LessonProgress, Quiz, Question, Answer
from .forms import CourseForm, LessonForm, QuizForm, QuestionForm


# головна сторінка - список всіх курсів
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


# сторінка одного курсу
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all()

    # перевіряємо чи студент вже записаний на курс
    is_enrolled = False
    completed_lessons = []
    if request.user.is_authenticated and request.user.is_student():
        is_enrolled = Enrollment.objects.filter(
            student=request.user, course=course
        ).exists()
        # які уроки вже пройшов
        completed_lessons = LessonProgress.objects.filter(
            student=request.user, completed=True
        ).values_list('lesson_id', flat=True)

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'completed_lessons': completed_lessons,
    })


# записатись на курс
@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # тільки студент може записатись
    if request.user.is_student():
        Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('course_detail', pk=pk)


# створити новий курс (тільки для викладача)
@login_required
def course_create(request):
    if not request.user.is_teacher():
        return redirect('/')
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Створити курс'})


# додати урок до курсу
@login_required
def lesson_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if not request.user.is_teacher():
        return redirect('/')
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', pk=course_pk)
    else:
        form = LessonForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Додати урок'})


# сторінка уроку
@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    # відмічаємо урок як переглянутий
    if request.user.is_student():
        progress, created = LessonProgress.objects.get_or_create(
            student=request.user, lesson=lesson
        )
        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()

    # перетворюємо звичайне ютуб посилання на embed
    youtube_url = lesson.youtube_url
    if 'watch?v=' in youtube_url:
        video_id = youtube_url.split('watch?v=')[1].split('&')[0]
        youtube_url = f'https://www.youtube.com/embed/{video_id}'
    elif 'youtu.be/' in youtube_url:
        video_id = youtube_url.split('youtu.be/')[1].split('?')[0]
        youtube_url = f'https://www.youtube.com/embed/{video_id}'

    # перевіряємо чи є тест до цього уроку
    quiz = getattr(lesson, 'quiz', None)

    print(f"youtube_url: {youtube_url}")

    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'quiz': quiz,
        'youtube_url': youtube_url,
    })


# пройти тест
@login_required
def quiz_submit(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    if request.method == 'POST':
        questions = quiz.questions.all()
        correct = 0
        total = questions.count()

        for question in questions:
            # беремо відповідь яку вибрав студент
            answer_id = request.POST.get(f'question_{question.pk}')
            if answer_id:
                answer = Answer.objects.filter(pk=answer_id, is_correct=True).first()
                if answer:
                    correct += 1

        score = int((correct / total) * 100) if total > 0 else 0
        return render(request, 'courses/quiz_result.html', {
            'quiz': quiz,
            'correct': correct,
            'total': total,
            'score': score,
        })
    return redirect('lesson_detail', pk=quiz.lesson.pk)


# сертифікат після завершення курсу
@login_required
def certificate(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    total_lessons = course.lessons.count()
    completed = LessonProgress.objects.filter(
        student=request.user,
        lesson__course=course,
        completed=True
    ).count()

    # сертифікат тільки якщо пройшов всі уроки
    if completed < total_lessons:
        return redirect('course_detail', pk=course_pk)

    return render(request, 'courses/certificate.html', {
        'course': course,
        'user': request.user,
        'date': timezone.now().date(),
    })