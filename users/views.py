from django.contrib.auth import authenticate, login,logout
from .forms import Registration,ForgotPassword
from django.contrib.auth.decorators import login_required
from .models import User

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token,password_reset_token
from django.core.mail import EmailMessage

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SetPasswordForm
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('users/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'],
                                    )
            login(request, new_user)
            return redirect('profile')
    else:
        form=Registration()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    return render(request,'users/profile.html')


def customlogout(request):
    logout(request)
    return render(request,'user/logout.html')


def activate(request,uidb64, token):
    try:
        #import ipdb;ipdb.set_trace()
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):

        HttpResponse('what')
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        return HttpResponse('Thank you for your email confirmation.Email verified')
    else:
        return HttpResponse('Activation link is invalid! Email not verified')

@login_required
def change_password(request):
    #import ipdb;ipdb.set_trace()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })

def reset_password(request,uidb64,token):
    try:
        #import ipdb;ipdb.set_trace()
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):

        HttpResponse('what')
        user = None
    if user is not None and password_reset_token.check_token(user, token):
        login(request,user)
        return redirect('create_password')
    else:
        return HttpResponse('Activation link is invalid! Email not verified')

@login_required
def create_password(request):
    if request.method=='POST':
        # return HttpResponse("qwerty")
        form = SetPasswordForm(request.POST)

        if form.is_valid():

            # return HttpResponse("check")
            # form.save()
            # return HttpResponse(form.cleaned_data['new_password1'])
            request.user.set_password(form.cleaned_data['New_Password'])
            request.user.save()
            messages.success(request, 'Your password was successfully updated!')
            login(request,request.user)
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('create_password')
    else:
        form = SetPasswordForm()
    return render(request, 'users/create_password.html', {
        'form': form})





def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPassword(request.POST)

        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            current_site = get_current_site(request)
            mail_subject = 'Reset password'
            message = render_to_string('users/reset_password.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse("Check your registered mail to reset password")


        else:
            messages.error(request,'Email is not registered')
    else:
        form = ForgotPassword()
    return render(request,'users/email_reset_password.html',{'form':form})