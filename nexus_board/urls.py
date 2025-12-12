"""
URL configuration for nexus_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import signup, current_user, admin_stats, admin_users
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/auth/login/', TokenObtainPairView.as_view(),
         name='api_login'),
    path('api/auth/signup/', signup, name='api_signup'),
    path('', TemplateView.as_view(template_name='nexus_board/index.html')),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/', include('courses.urls')),
    path('api/me/', current_user, name='api_me'),
    path('api/admin/stats/', admin_stats, name='api_admin_stats'),
    path('api/admin/users/', admin_users, name='api_admin_users'),
    path('api/admin/users/<int:pk>/', admin_users,
         name='api_admin_user_detail'),
]
