from django.contrib import admin

from quiz.models import User, Quiz, Choice


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz']
    # fields = ['pub_date', 'question_text']

# admin.site.register(Question, QuestionAdmin)
admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Choice, ChoiceAdmin)