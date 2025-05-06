# accounts/views.py
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser, EmailVerification
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password'])
            user.save()

            verification = EmailVerification.objects.create(user=user)
            verify_url = request.build_absolute_uri(
                reverse('accounts:verify_email', args=[verification.token])
            )
            send_mail(
                'メール認証を完了してください',
                f'以下のリンクをクリックして認証を完了してください:\n{verify_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )
            return render(request, 'accounts/email_sent.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
        user = verification.user
        user.is_active = True
        user.save()
        verification.delete()
        return render(request, 'accounts/verified.html')
    except EmailVerification.DoesNotExist:
        return render(request, 'accounts/invalid_token.html')
    
def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # 任意のリダイレクト先
            else:
                error_message = 'ユーザー名またはパスワードが間違っています。'
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')