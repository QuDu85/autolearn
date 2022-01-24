from django.contrib import admin
from .models import Question, QuizPack, User, Material, Topic, Language

# Register your models here.
admin.site.register(User)
admin.site.register(Material)
admin.site.register(Topic)
admin.site.register(Language)
admin.site.register(Question)
admin.site.register(QuizPack)
