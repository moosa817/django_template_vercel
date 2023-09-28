from django.shortcuts import render, redirect
from ..models import Room, Topic, Message, UserProfile
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
import random
import string
from django.contrib.auth import password_validation
from django.forms import ValidationError
from email.mime.text import MIMEText
from django.conf import settings
# Create your views here.
import smtplib


def send_email(to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = to
    msg['From'] = settings.EMAIL_SENDER

    s = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
    s.starttls()
    s.login(settings.MAIL_USER, settings.MAIL_PWD)
    s.send_message(msg)
    s.quit()


def blur_email(email):
    if "@" in email:
        username, domain = email.split("@")
        # Keep the first and last characters
        username = username[:1] + "*" * (len(username) - 2) + username[-1]
        # Keep the first character
        domain = domain[:1] + "*" * (len(domain) - 1)
        return f"{username}@{domain}"
    else:
        return email


def ForgotPwd(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.session.get('code') and request.session.get('code_sucess'):
        type = 'changepwd'
        BlurEmail = None
    elif request.session.get('code'):
        type = "code"
        BlurEmail = blur_email(request.session.get('email'))
    else:
        type = "email"
        BlurEmail = None

    context = {'type': type, 'blur_email': BlurEmail}

    if request.GET.get('resend') == 'True':
        if request.session.get('code'):
            del request.session['code']
        if request.session.get('email'):
            del request.session['email']
        if request.session.get('code_sucess'):
            del request.session['code_sucess']

        return redirect('forgot')

    if request.method == 'POST':
        # enter email
        if not request.session.get('code') and not request.session.get('code_sucess'):
            uemail = request.POST.get('uemail')
            try:
                myemail = UserProfile.objects.get(
                    Q(username__username=uemail) | Q(email=uemail))
            except:
                messages.error(request, 'Email or username does not exist ')
                return render(request, 'base/forgot.html', context)
            else:
                # do stuff
                email = myemail.email

                characters = string.ascii_letters + string.digits
                six_character_code = ''.join(
                    random.choice(characters) for _ in range(6))

                send_email(email, 'Verification Code', f"""
                YOUR VERIFICATION CODE IS {six_character_code}""")

                request.session['code'] = six_character_code
                request.session['email'] = email

                return redirect('forgot')

        # enter code
        elif request.session.get('code') and not request.session.get('code_sucess'):
            code = request.POST.get('code')
            if code == request.session['code']:
                request.session['code_sucess'] = True
                return redirect('forgot')
            else:
                messages.error(request, 'Wrong Code')
        # change pwd
        elif request.session.get('code') and request.session.get('code_sucess'):
            pwd = request.POST.get('password1')
            re_pwd = request.POST.get('password2')

            if pwd != re_pwd:
                messages.error(request, 'Passwords do not match ')
            else:
                try:
                    password_validation.validate_password(pwd)
                except ValidationError as e:
                    messages.error(request, e)
                else:
                    myuser = UserProfile.objects.get(
                        email=request.session.get('email')).username

                    user = User.objects.get(username=myuser)
                    user.set_password(pwd)
                    user.save()
                    login(request, user, backend=backend)
                    return redirect('home')

    return render(request, 'base/forgot.html', context)
