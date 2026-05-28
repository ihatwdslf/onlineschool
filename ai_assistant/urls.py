from django.urls import path
from . import views

urlpatterns = [
    path('courses/<int:course_pk>/generate-description/', views.generate_description, name='generate_description'),
]