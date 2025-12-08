from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


User = get_user_model()


def vue_app(request):
    return render(request, "nexus_board/index.html")


@api_view(['POST'])
def signup(request):
    """Create a new user. Expects JSON with username, email, password."""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    if not username or not password:
        return Response(
            {'detail': 'username and password required'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if User.objects.filter(username=username).exists():
        return Response(
            {'detail': 'username already exists'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return Response(
            {'id': user.id, 'username': user.username},
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response(
            {'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_stats(request):
    """Return admin dashboard stats: totals and recent items."""
    if not request.user.is_staff:
        return Response({'detail': 'admin only'}, status=status.HTTP_403_FORBIDDEN)

    from django.db.models import Count
    from courses.models import Course, Lesson, Enrollment, Note

    total_users = request.user.__class__.objects.count()
    total_courses = Course.objects.count()
    total_lessons = Lesson.objects.count()
    total_enrollments = Enrollment.objects.count()

    recent_enrolls_qs = (
        Enrollment.objects.select_related('user', 'course')
        .order_by('-enrolled_at')[:10]
    )
    recent_enrolls = [
        {
            'id': e.id,
            'user': getattr(e.user, 'username', str(e.user)),
            'course': e.course.title if e.course else None,
            'enrolled_at': e.enrolled_at.isoformat(),
        }
        for e in recent_enrolls_qs
    ]

    recent_notes_qs = Note.objects.select_related('lesson').order_by('-created_at')[:10]
    recent_notes = [
        {
            'id': n.id,
            'title': n.title,
            'author': n.author,
            'lesson': n.lesson.title if n.lesson else None,
            'created_at': n.created_at.isoformat(),
        }
        for n in recent_notes_qs
    ]

    recent_users_qs = request.user.__class__.objects.order_by('-id')[:10]
    recent_users = [
        {
            'id': u.id,
            'username': u.username,
            'is_staff': u.is_staff,
            'is_active': u.is_active,
        }
        for u in recent_users_qs
    ]

    return Response(
        {
            'totals': {
                'users': total_users,
                'courses': total_courses,
                'lessons': total_lessons,
                'enrollments': total_enrollments,
            },
            'recent_enrollments': recent_enrolls,
            'recent_notes': recent_notes,
            'recent_users': recent_users,
        }
    )


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def admin_users(request, pk=None):
    """List users (GET) or update a single user (PATCH via pk)."""
    if not request.user.is_staff:
        return Response({'detail': 'admin only'}, status=status.HTTP_403_FORBIDDEN)

    User = request.user.__class__

    if request.method == 'GET':
        users = User.objects.order_by('-id')[:200]
        data = [
            {'id': u.id, 'username': u.username, 'is_staff': u.is_staff, 'is_active': u.is_active}
            for u in users
        ]
        return Response(data)

    if request.method == 'PATCH' and pk:
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        # Only admins can toggle staff and active status
        is_staff = request.data.get('is_staff')
        is_active = request.data.get('is_active')
        changed = False
        if is_staff is not None:
            u.is_staff = bool(is_staff)
            changed = True
        if is_active is not None:
            u.is_active = bool(is_active)
            changed = True
        if changed:
            u.save()
        return Response({'id': u.id, 'username': u.username, 'is_staff': u.is_staff, 'is_active': u.is_active})

    return Response({'detail': 'method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
