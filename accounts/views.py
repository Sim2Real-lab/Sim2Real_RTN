from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache

@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if hasattr(user, 'userrole') and user.userrole.is_organiser:
                    return redirect('staff_dashboard')
                else:
                    return redirect('home')  # or redirect to dashboard
            else:
                return render(request, 'accounts/login.html', {
                    'login_error': 'Please verify your email before logging in.'
                })
        else:
            return render(request, 'accounts/login.html', {
                'login_error': 'Invalid email or password'
            })

    return render(request, 'accounts/login.html')
@never_cache
def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'accounts/signup.html', {
                'signup_error': 'Passwords do not match'
            })

        if User.objects.filter(username=email).exists():
            return render(request, 'accounts/signup.html', {
                'signup_error': 'Email already registered'
            })
        try:
            validate_password(password1)
        except ValidationError as e:
            return render(request, 'accounts/signup.html', {
                'signup_error': e.messages  # this is a list of errors
            })
        
        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password1)
        user.is_active = False
        user.save()
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        verification_link = request.build_absolute_uri(
            reverse('activate', kwargs={'uidb64': uid, 'token': token})
        )

        subject = 'Verify your SIM2REAL account'
        message = f'Hi! Please click the link below to verify your email and activate your account:\n\n{verification_link}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, 'Please check your email to verify your account.')
        return redirect('login')
    return render(request, 'accounts/signup.html')

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str  # for Django 3.1+, use force_text for older versions
from django.http import HttpResponse

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully! You can now login.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid or has expired.')

def resend_verification_view(request):
    if request.method=="POST":
        email=request.POST.get('email')
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=email)
            if user.is_active:
                messages.info(request, 'Your account is already active. You can log in.')
                return redirect('login')
            # Resend verification email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            verification_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )

            subject = 'Resend - Verify your SIM2REAL account'
            message = f'Hi again! Click below to verify your account:\n\n{verification_link}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

            messages.success(request, 'Verification email resent. Please check your inbox.')
        except user_model.DoesNotExist:
            messages.error(request, 'No account found with that email.')
            return render(request, 'accounts/signup.html')
    return render(request, 'accounts/signup.html')