import os
import google.generativeai as genai
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')


@login_required
def generate_description(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)

    if request.user != course.teacher:
        print(f"Не той викладач! request.user={request.user}, teacher={course.teacher}")
        return redirect('course_detail', pk=course_pk)

    try:
        print(f"Генеруємо опис для курсу: {course.title}")

        response = model.generate_content(
            f'Напиши короткий опис онлайн курсу "{course.title}" українською мовою. 2-3 речення. Без форматування'
        )

        generated_text = response.text
        print(f"Отримали відповідь: {generated_text}")

        course.description = generated_text
        course.save()
        print("Збережено!")

    except Exception as e:
        print(f"Gemini помилка: {e}")

    return redirect('course_detail', pk=course_pk)