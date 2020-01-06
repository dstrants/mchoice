from django.contrib import admin
from .models import Test, Question, Choice, Attempt, Aswer


admin.site.register(Choice)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Attempt)
admin.site.register(Aswer)
