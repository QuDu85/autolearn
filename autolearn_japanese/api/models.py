from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
class Topic(models.Model):
    topic = models.CharField(max_length=20)
    
    def __str__(self):
        return self.topic

class Language(models.Model):
    language = models.CharField(max_length=20)
    
    def __str__(self):
        return self.language
    
class Skill(models.Model):
    skill = models.CharField(max_length=20)
    
    def __str__(self):
        return self.skill
    
class Level(models.Model):
    level = models.CharField(max_length=20)

    def __str__(self):
        return self.level
    
class Material(models.Model):
    title = models.CharField(max_length=30)
    skill = models.ManyToManyField(Skill)
    length = models.IntegerField()
    link = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    topic = models.ManyToManyField(Topic)
    language = models.ManyToManyField(Language)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
class Question(models.Model):
    question = models.CharField(max_length=200, default='Select the correct answer')
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    OPTIONS = [
        ('A', 'op1'),
        ('B', 'op2'),
        ('C', 'op3'),
        ('D', 'op4')
    ]
    ans = models.CharField(
        max_length=1,
        choices=OPTIONS,
        default = 'A',
    )
    
    def __str__(self):
        return self.question
    
class QuizPack(models.Model):
    name = models.CharField(max_length=100, null=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    questions = models.ManyToManyField(Question)
    
    def __str__(self):
        return self.name
    
class StudentProgress(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    quizCompleted = models.ManyToManyField(QuizPack)
    
    
class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    
class QuestionAttempt(models.Model):
    quizAttempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200,null=True)
    status = models.BooleanField(null=True)
    