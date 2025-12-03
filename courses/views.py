from rest_framework import viewsets, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]
