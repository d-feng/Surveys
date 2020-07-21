from django.contrib import admin
from .models import Choice, Question,TestModel

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text','was_published_recently']
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    # ...
    list_display = ('question_text', 'pub_date')

#admin.site.register(Question)
admin.site.register(TestModel)
admin.site.register(Question, QuestionAdmin)
# Register your models here.
