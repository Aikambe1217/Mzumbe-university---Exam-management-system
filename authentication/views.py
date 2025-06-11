from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import re


def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        return False, "Password must contain at least one special character."
    return True, ""

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        is_valid, error_message = is_strong_password(password)
        if not is_valid:
            messages.error(request, f"Password Error: {error_message}")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Sorry! Username is already taken. Try another one.')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Sorry! Email is already taken. Try another one.')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('login')
    else:
        return render(request, 'authentication.html')



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                request.session['show_preloader'] = True
                request.session['preloader_username'] = user.username
                return redirect('/main/index')
            else:
                messages.error(request, 'Admin confirmation pending! contact your admin to have you granted permission to access the system.')
                return redirect('/')
        else:
            messages.error(request, 'Incorrect credentials or you are not authorized.')
            return redirect('/')
    else:
        
        return render(request,'authentication.html')



def admin_auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                return redirect('/examAdmin/dashboard')
            else:
                messages.error(request, 'user is not an Admin')
                return redirect('admin_auth')
        else:
            messages.error(request, 'user is not found')
            return redirect('admin_auth')
    else:
        
        return render(request, 'admin-auth.html')
    
    
# Add this to your views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def clear_preloader_session(request):
    if 'show_preloader' in request.session:
        del request.session['show_preloader']
    return JsonResponse({'status': 'success'})


def logout(request):
    auth.logout(request)
    return redirect('login')



User = get_user_model()

def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        
        # Check if a user with this email exists
        try:
            user = User.objects.get(email=email)
            
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build the reset URL
            domain = request.get_host()
            protocol = 'https' if request.is_secure() else 'http'
            reset_url = f"{protocol}://{domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
            
            # Render the email template
            email_context = {
                'user': user,
                'reset_url': reset_url,
                'domain': domain,
                'site_name': 'Your Site Name',
                'protocol': protocol,
                'uid': uid,
                'token': token,
            }
            email_subject = "Password Reset on Your Site"
            email_body = render_to_string('password_reset/password_reset_email.html', email_context)
            
            # Send the email
            send_mail(
                email_subject,
                email_body,
                'noreply@yoursite.com',
                [user.email],
                fail_silently=False,
                html_message=email_body
            )
            
            messages.success(request, "Password reset email has been sent. Please check your inbox.")
            return redirect('password_reset_done')
            
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist
            messages.success(request, "Password reset email has been sent. Please check your inbox.")
            return redirect('password_reset_done')
    
    return render(request, 'password_reset/password_reset_form.html')