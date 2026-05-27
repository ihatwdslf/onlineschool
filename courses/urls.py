from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_pk>/lessons/add/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('quiz/<int:quiz_pk>/submit/', views.quiz_submit, name='quiz_submit'),
    path('courses/<int:course_pk>/certificate/', views.certificate, name='certificate'),
]