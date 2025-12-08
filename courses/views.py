from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Course, Lesson, Note, Enrollment
from django.db import models as djmodels
from .serializers import CourseSerializer, LessonSerializer
from .serializers import NoteSerializer, EnrollmentSerializer


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
    # allow read to anyone but restrict create/update/delete to admins
    permission_classes = [IsAdminOrReadOnly]


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.select_related('lesson').all()
    serializer_class = NoteSerializer
    # Only authenticated users may list/create notes; object-level
    # edits/deletes are restricted to the note author or staff.
    
    class IsAuthorOrReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            # require authentication for listing and creating
            return request.user and request.user.is_authenticated

        def has_object_permission(self, request, view, obj):
            # allow safe methods for authenticated users
            if request.method in permissions.SAFE_METHODS:
                return True
            # staff can modify/delete any note
            if request.user and request.user.is_staff:
                return True
            # only the original author (stored as username string) may
            # modify/delete
                return (
                    getattr(obj, 'author', None)
                    == getattr(request.user, 'username', None)
                )

    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        qs = Note.objects.select_related('lesson').all()
        request = self.request
        # Filter by lesson if requested
        lesson_id = request.query_params.get('lesson')
        if lesson_id:
            qs = qs.filter(lesson_id=lesson_id)

        # If staff, return everything (admins manage notes)
        user = getattr(request, 'user', None)
        if user and user.is_staff:
            return qs

        # For authenticated non-staff users, show only public notes or
        # notes they authored
        username = getattr(user, 'username', None)
        qs = qs.filter(
            djmodels.Q(is_public=True) | djmodels.Q(author=username)
        )
        return qs

    def perform_create(self, serializer):
        # set the author automatically from the requesting user
        # Note.author is a CharField; save the username string
        username = getattr(self.request.user, 'username', None) or 'Anonymous'
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
        # Only return enrollments belonging to the requesting user
        user = self.request.user
        # staff users may view all enrollments; regular users only their own
        if user and user.is_staff:
            return Enrollment.objects.select_related('course', 'user').all()
        return Enrollment.objects.filter(user=user).select_related('course')

    def perform_create(self, serializer):
        # ensure the enrollment is linked to the current user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Prevent duplicate enrollments from creating duplicate rows
        course_id = request.data.get('course')
        if not course_id:
            return Response(
                {'detail': 'course field is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check whether an enrollment already exists
        exists = (
            Enrollment.objects
            .filter(user=request.user, course_id=course_id)
            .exists()
        )
        if exists:
            # Return the existing enrollment instead of creating a duplicate
            enrollment = Enrollment.objects.get(
                user=request.user, course_id=course_id
            )
            serializer = self.get_serializer(enrollment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)
