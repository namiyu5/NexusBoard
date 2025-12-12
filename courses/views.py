from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Course, Lesson, Note, Enrollment
from django.db import models as djmodels
from .serializers import CourseSerializer, LessonSerializer
from .serializers import NoteSerializer, EnrollmentSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read access to everyone, write access to admin only."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CourseViewSet(viewsets.ModelViewSet):
    """Courses are read-only for regular users, editable by admin."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    """Lessons are read-only for regular users, editable by admin."""
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]


class NoteViewSet(viewsets.ModelViewSet):
    """Notes: editable by author or admin. Public notes visible to all."""
    queryset = Note.objects.select_related('lesson').all()
    serializer_class = NoteSerializer

    class IsAuthorOrReadOnly(permissions.BasePermission):
        """Author or admin can edit. Authenticated users can read."""
        def has_permission(self, request, view):
            return request.user and request.user.is_authenticated

        def has_object_permission(self, request, view, obj):
            # Safe methods allowed for authenticated users
            if request.method in permissions.SAFE_METHODS:
                return True
            # Admin can always edit/delete
            if request.user and request.user.is_staff:
                return True
            # Only the note author can edit/delete their own notes
            return (
                getattr(obj, 'author', None)
                == getattr(request.user, 'username', None)
            )

    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        """Filter notes based on user permissions.

        Admin sees all notes.
        Regular users see: public notes + their own notes.
        """
        qs = Note.objects.select_related('lesson').all()
        request = self.request
        lesson_id = request.query_params.get('lesson')
        if lesson_id:
            qs = qs.filter(lesson_id=lesson_id)

        user = getattr(request, 'user', None)
        if user and user.is_staff:
            return qs

        # Show only public notes or notes authored by current user
        username = getattr(user, 'username', None)
        qs = qs.filter(
            djmodels.Q(is_public=True) | djmodels.Q(author=username)
        )
        return qs

    def perform_create(self, serializer):
        """Auto-assign note author from current user when creating."""
        username = getattr(self.request.user, 'username', None) or (
            'Anonymous'
        )
        serializer.save(author=username)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """Allow users to list and create their enrollments.

    `list` returns only enrollments for the requesting user.
    `create` attaches `request.user` as the `user` on the Enrollment.
    """
    queryset = Enrollment.objects.select_related('course', 'user').all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Staff sees all enrollments; regular users see only their own
        if user and user.is_staff:
            return Enrollment.objects.select_related('course', 'user').all()
        return Enrollment.objects.filter(user=user).select_related('course')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Prevent duplicate enrollments
        course_id = request.data.get('course')
        if not course_id:
            return Response(
                {'detail': 'course field is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        exists = (
            Enrollment.objects
            .filter(user=request.user, course_id=course_id)
            .exists()
        )
        if exists:
            # User already enrolled, return existing enrollment
            enrollment = Enrollment.objects.get(
                user=request.user, course_id=course_id
            )
            serializer = self.get_serializer(enrollment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)
