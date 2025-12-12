from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'title', 'content',
            'order', 'video_url', 'duration_minutes',
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'excerpt', 'published',
            'created_at', 'updated_at', 'lessons',
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
