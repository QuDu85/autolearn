from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('login', views.log_in, name="login"),
    path('login/forgot', views.forget_passwd, name="forget_passwd"),
    path('signout', views.signout, name="signout"),
    path('student/home', views.home_student, name="home_student"),
    path('student/edit', views.edit_profile, name="edit_profile"),
    path('student/change', views.change_passwd, name="change_pass"),
    path('student/letters/<str:chart>', views.student_letter, name="letters_student"),
    path('student/letters/<str:chart>/<str:letter>', views.letter_detail, name="letter_detail"),
    path('student/reference', views.student_reference, name="reference_student"),
    path('student/reference/<int:id>', views.reference_detail, name="reference_detail"),
    path('student/quiz/<str:level>', views.student_quiz, name="quiz_student"),
    path('student/quiz_detail/<int:id>', views.quiz_detail, name="quiz_detail"),
]