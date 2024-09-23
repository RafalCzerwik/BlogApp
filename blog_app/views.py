from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.shortcuts import render, redirect
from django.views import View

from blog_app.models import Post

User = get_user_model() # bardzo ważne


class IndexView(View):
    def get(self, request):
        all_user_posts = Post.objects.all().order_by('-created_at')

        return render(request, 'blog_app/index.html', {'all_user_posts': all_user_posts})


class DashboardView(View):
    def get(self, request):

        user = request.user
        all_user_posts = Post.objects.filter(author=user).order_by('-created_at')

        return render(request, 'blog_app/dashboard.html', {'all_user_posts': all_user_posts})


class LoginView(View):
    def get(self, request):
        return render(request, 'blog_app/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            expiration_time = datetime.now() + timedelta(hours=1)
            response = redirect('dashboard')
            response.set_cookie('user_authenticated', 'true', expires=expiration_time)

            return response
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'blog_app/login.html', {'error_message': error_message})


class UpdatePasswordView(View):
    def get(self, request):
        return render(request, 'blog_app/update_password.html')

    def post(self, request):
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('new_password_confirm')

        user = request.user

        if len(new_password) < 8:
            error_message = 'Password must be at least 8 characters.'
            return render(request, 'blog_app/update_password.html', {'error_message': error_message})

        elif new_password != confirm_new_password:
            error_message = 'Passwords do not match!'
            return render(request, 'blog_app/update_password.html', {'error_message': error_message})
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            success_message = 'Password updated successfully.'
            return render(request, 'blog_app/update_password.html', {'success_message': success_message})


class UpdateProfileView(View):
    def get(self, request):
        return render(request, 'blog_app/profile.html')

    def post(self, request):
        update_first_name = request.POST.get('first_name')
        update_surname = request.POST.get('last_name')
        update_email = request.POST.get('email')

        user = request.user

        user.first_name = update_first_name
        user.last_name = update_surname
        user.email = update_email

        try:
            user.save()
            success_message = 'Your account has been updated.'
            return render(request, 'blog_app/profile.html', {'success_message': success_message})

        except Exception as e:
            error_message = 'An error occurred while updating the profile.'
            return render(request, 'blog_app/profile.html', {
                'error_message': error_message,
                'first_name': update_first_name,
                'last_name': update_surname,
                'email': update_email,
            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class DeleteAccountView(View):
    def post(self, request):
        user = request.user
        user.delete()
        return redirect('index')


class RegisterView(View):
    def get(self, request):
        return render(request, 'blog_app/register.html')

    def post(self, request):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirm')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists!'
            return render(request, 'blog_app/register.html', {'error_message': error_message})

        if User.objects.filter(email=email).exists():
            error_message = 'Email already exists!'
            return render(request, 'blog_app/register.html', {'error_message': error_message})

        if len(password) < 8:
            error_message = 'Password must be at least 8 characters.'
            return render(request, 'blog_app/register.html', {'error_message': error_message})
        elif password != confirm_password:
            error_message = 'Passwords do not match!'
            return render(request, 'blog_app/register.html', {'error_message': error_message})
        else:
            new_user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=surname,
                email=email,
                password=password,
            )
            success_message = 'You have successfully registered.'
        new_user.save()

        # funkcja do wysylania wiadomosci email po rejestracji.
        # subject = f'Welcome {username} on !!!'
        # email_message = (
        #     f'Dear {username},\n\n'
        #     f'Thank you for registering on my demo portal!\n'
        #     f'We are excited to have you on board.\n\n'
        #     f'If you have any questions or need assistance, feel free to reach out.\n\n'
        #     f'Best regards,\n'
        #     f'Rafal Czerwik\n'
        # )
        #
        # send_mail(
        #     subject,
        #     email_message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [email],
        #     fail_silently=False,
        # )

        return render(request, 'blog_app/login.html', {'success_message': success_message})


class AddPostView(View):
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('content')

        user = request.user
        all_user_posts = Post.objects.filter(author=user).order_by('-created_at')

        if not title or not description:
            error_message = 'Title or description cannot be empty.'
            return render(request, 'blog_app/dashboard.html', {'error_message': error_message})
        else:
            new_post = Post.objects.create(
                title=title,
                content=description,
                author=user,
            )
            success_message = 'Your post has been added.'

        return render(request, 'blog_app/dashboard.html', {
            'success_message': success_message,
            'all_user_posts': all_user_posts
        })


class UpdatePostView(View):
    def get(self, request, id):

        user = request.user
        post = Post.objects.get(id=id, author=user)

        return render(request, 'blog_app/post.html', {'post': post})

    def post(self, request, id):

        user = request.user
        all_user_posts = Post.objects.filter(author=user).order_by('-created_at')

        updated_title = request.POST.get('title')
        updated_content = request.POST.get('content')

        updated_post = Post.objects.get(id=id, author=user)

        if updated_title:
            updated_post.title=updated_title

        if updated_content:
            updated_post.content=updated_content

        updated_post.save()

        success_message = 'Your post has been updated.'

        # inna wersja:

        # all_user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
        # updated_post = Post.objects.get(id=id, author=request.user)
        #
        # if updated_title:
        #     updated_post.title = request.POST.get('title')
        #
        # if updated_content:
        #     updated_post.content = request.POST.get('content')
        #
        # updated_post.save()
        #
        # success_message = 'Your post has been updated.'

        return render(request, 'blog_app/dashboard.html', {
            'success_message': success_message,
            'all_user_posts': all_user_posts,
        })


class DeletePostView(View):
    def get(self, request, id):

        all_user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
        delete_post = Post.objects.get(id=id, author=request.user)
        delete_post.delete()

        success_message = 'Your post has been deleted.'
        return render(request, 'blog_app/dashboard.html', {
            'success_message': success_message,
            'all_user_posts': all_user_posts,
        })
