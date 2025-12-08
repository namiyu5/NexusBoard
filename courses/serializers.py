from rest_framework import serializers
from .models import Course, Lesson
from .models import Note
from .models import Enrollment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'title', 'content',
            'order', 'video_url', 'duration_minutes'
        ]


class CourseSerializer(serializers.ModelSerializer):
    # only include lessons for authenticated requests
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'excerpt', 'published',
            'created_at', 'updated_at', 'lessons'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_lessons(self, obj):
        request = self.context.get('request')
        if not request:
            return []
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return []
        return LessonSerializer(obj.lessons.all(), many=True).data


class NoteSerializer(serializers.ModelSerializer):
    # author is a simple string on the Note model; expose it read-only
    author = serializers.ReadOnlyField()

    class Meta:
        model = Note
        fields = [
            'id',
            'lesson',
            'title',
            'content',
            'is_public',
            'author',
            'created_at',
        ]
        read_only_fields = ['created_at', 'author']


class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']
        read_only_fields = ['user', 'enrolled_at']
