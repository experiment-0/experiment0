from django.contrib import admin
from .models import School, Course, Lesson, LessonCompletion

admin.site.register(School)
admin.site.register(Course)
admin.site.register(Lesson)


class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson', 'student']
    list_filter = ['lesson', 'student']


admin.site.register(LessonCompletion, LessonCompletionAdmin)
