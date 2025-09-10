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
from django.utils import timezone
from .models import PasswordResetOTP
from .forms import OTPRequestForm, OTPVerifyForm
from django.db import transaction
import random
from django.core.mail import EmailMultiAlternatives

@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(username=email)
        except User.DoesNotExist:
            user_obj = None
        if user_obj and not user_obj.is_active:
            resend_url = reverse('resend_verification') + f'?email={email}'
            login_error = f'Your account is not active. Please <a href="{resend_url}" class="resend-link">Click here</a> to resend verification link.'
            return render(request, 'accounts/login.html', {
                'login_error': login_error
            })
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            if hasattr(user, 'userrole') and user.userrole.is_organiser:
                return redirect('staff_dashboard')
            else:
                return redirect('home')
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
            return render(request, 'accounts/signup.html', {'signup_error': 'Passwords do not match'})

        try:
            validate_password(password1)
        except ValidationError as e:
            return render(request, 'accounts/signup.html', {'signup_error': e.messages})

        # Delete any previous inactive users with this email
        existing_user = User.objects.filter(username=email).first()
        if existing_user:
            if existing_user.is_active:
                return render(request, 'accounts/signup.html', {
            'signup_error': 'Email already registered and verified'
        })
            else:
                # Remove stale inactive user
                existing_user.delete()

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=email, email=email, password=password1)
                user.is_active = False
                user.save()

        # Prepare email
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                verification_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )

                subject = 'Verify your SIM2REAL account'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [email]


                # Send email
                

# ... after generating `verification_link`

                html_content = f"""
<html>
<head>
<style>
.btn {{
    display: inline-block;
    padding: 12px 24px;
    font-size: 16px;
    color: white;
    background-color: #007BFF;
    text-decoration: none;
    border-radius: 5px;
}}
.container {{
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}}
</style>
</head>
<body>
<div class="container">
<h2>Welcome to SIM2REAL!</h2>
<p>Thank you for signing up. Please verify your email to activate your account.</p>
<p><a href="{verification_link}" class="btn">Verify Email</a></p>
<p>If the button doesn’t work, copy and paste this link into your browser:</p>
<p>{verification_link}</p>
<p>Regards,<br>SIM2REAL Team</p>
</div>
</body>
</html>
"""

                email_message = EmailMultiAlternatives(subject, "Please view this email in HTML", from_email, recipient_list)
                email_message.attach_alternative(html_content, "text/html")
                email_message.send(fail_silently=False)

        except Exception as e:
            # If email fails, rollback user creation automatically
            return render(request, 'accounts/signup.html', {'signup_error': f"Error sending email: Plese check your email or contact organisers"})

        messages.success(request, "Signup successful! Check your email to activate your account. If mail not found in Inbox please check Spam")
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
            return redirect('login')
        except user_model.DoesNotExist:
            messages.error(request, 'No account found with that email.')
            return render(request, 'accounts/signup.html')
    return render(request, 'accounts/login.html')

def request_otp_view(request):
    if request.method == "POST":
        form = OTPRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "No user with this email exists.")
                return render(request, 'accounts/request_otp.html', {'form': form})

            # Generate OTP
            otp = f"{random.randint(100000, 999999)}"
            PasswordResetOTP.objects.create(user=user, otp=otp)

            # Send Email
            subject = "Your SIM2REAL Password Reset OTP"
            message = f"Use this OTP to reset your password. It expires in 10 minutes.\n\nOTP: {otp}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "OTP sent to your email.")
            from django.urls import reverse
            return redirect(f"{reverse('verify_otp')}?email={email}")

    else:
        form = OTPRequestForm()
    return render(request, 'accounts/request_otp.html', {'form': form})


def verify_otp_view(request):
    initial_email = request.GET.get('email', '')
    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        initial_email = request.GET.get('email', '')
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password1']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email.")
                return render(request, 'accounts/verify_otp.html', {'form': form})

            # Get latest OTP for user
            otp_records = PasswordResetOTP.objects.filter(user=user, otp=otp).order_by('-created_at')
            if not otp_records.exists():
                messages.error(request, "Invalid OTP.")
                return render(request, 'accounts/verify_otp.html', {'form': form})

            otp_record = otp_records.first()
            if otp_record.is_expired():
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect('request_otp')

            # Reset password
            user.set_password(new_password)
            user.save()

            # Delete all OTPs for this user to invalidate old ones
            PasswordResetOTP.objects.filter(user=user).delete()

            messages.success(request, "Password reset successful. You can now log in.")
            return redirect('login')

    else:
        
        form = OTPVerifyForm(initial={'email': initial_email})

    return render(request, 'accounts/verify_otp.html', {'form': form})