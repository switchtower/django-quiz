from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from quiz.models import Quiz, Category, Progress
from multichoice.models import Question, Answer

class QuestionInline(admin.TabularInline):
    model = Question.quiz.through
    filter_horizontal = ('content',)


class AnswerInline(admin.TabularInline):
    model = Answer 

"""
below is from 
http://stackoverflow.com/questions/11657682/django-admin-interface-using-horizontal-filter-with-inline-manytomany-field
"""

class QuizAdminForm(forms.ModelForm):
    class Meta:
        model = Quiz
    
    questions = forms.ModelMultipleChoiceField(
                                               queryset=Question.objects.all(),
                                               required=False,
                                               widget=FilteredSelectMultiple(verbose_name=('Questions'),
                                                                             is_stacked=False
                                                                             )
                                               )
    
    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = self.instance.question_set.all()
    
    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        if commit:
            quiz.save()
        if quiz.pk:
            quiz.question_set = self.cleaned_data['questions']
            self.save_m2m()
        return quiz

class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    
    list_display = ('title', 'category', )
    list_filter = ('category',)
    search_fields = ('description', 'category', )
    

    
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category', )

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category', 'quiz', 'explanation' )
    
    search_fields = ('content', )
    filter_horizontal = ('quiz',)

    
    inlines = [AnswerInline]
    
    
class ProgressAdmin(admin.ModelAdmin):
    """
    to do:
            create a user section
    """
    search_fields = ('user', 'score', )

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Progress, ProgressAdmin)