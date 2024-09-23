"""
URL configuration for notbug project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from blog_app.views import IndexView, LoginView, LogoutView, RegisterView, AddPostView, DashboardView, UpdatePostView, \
    DeletePostView, DeleteAccountView, UpdatePasswordView, UpdateProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('update-post/<int:id>/', UpdatePostView.as_view(), name='post'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('delete-post/<int:id>/', DeletePostView.as_view(), name='delete_post'),
    path('update-password/', UpdatePasswordView.as_view(), name='update_password'),
    path('profile/', UpdateProfileView.as_view(), name='profile'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]
