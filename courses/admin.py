from django.contrib import admin
from django import forms
from django.forms import Textarea
from django.db import models as djmodels
from ckeditor.widgets import CKEditorWidget

from .models import Course, Lesson, Note, Enrollment


class LessonInlineForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),
        }


class LessonInline(admin.StackedInline):
    model = Lesson
    form = LessonInlineForm
    extra = 1
    classes = ('collapse',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published', 'created_at')
    list_editable = ('published',)
    list_filter = ('published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'excerpt')
    inlines = [LessonInline]
    formfield_overrides = {
        djmodels.TextField: {
            'widget': Textarea(attrs={'rows': 5, 'cols': 80}),
        },
    }

    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        updated = queryset.update(published=True)
        self.message_user(request, f"{updated} course(s) marked as published")
    make_published.short_description = 'Mark selected courses as published'

    def make_unpublished(self, request, queryset):
        updated = queryset.update(published=False)
        self.message_user(
            request, f"{updated} course(s) marked as unpublished"
        )
    make_unpublished.short_description = 'Mark selected courses as unpublished'


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),
        }


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ('id', 'title', 'course', 'order', 'duration_minutes')
    list_filter = ('course',)
    search_fields = ('title', 'content')
    ordering = ('course', 'order')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'lesson',
        'title',
        'author',
        'is_public',
        'created_at',
    )
    search_fields = ('title', 'content', 'author')
    list_filter = ('lesson', 'is_public')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'enrolled_at')
    search_fields = ('user__username', 'course__title')
    list_filter = ('course',)
