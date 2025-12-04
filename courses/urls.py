from rest_framework import routers
from .views import (
    CourseViewSet,
    LessonViewSet,
    NoteViewSet,
    EnrollmentViewSet,
)

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = router.urls
