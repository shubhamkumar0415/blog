from django import forms
from django.contrib.auth import password_validation
from django.http import HttpResponse

from users.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError



class Registration(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput,required=False)

    class Meta:
        model = User
        fields = ['email','password','password2']

    def clean(self):
        #import ipdb;ipdb.set_trace()
        email=self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError('password mismatch')


        if len(password) < 8 or len(password2)< 8:
            raise forms.ValidationError('password must have atleast 8 letter')


        if len(email)<3:
            raise forms.ValidationError('email not be empty')


        try:
            password_validation.validate_password(password2)
        except:
            raise ValidationError('password too common')

        if User.objects.filter(email=email):
            raise ValidationError("email already exist")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ForgotPassword(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def clean(self):

        email = self.cleaned_data['email']
        if not User.objects.filter(email = email):
            raise ValidationError("Email not registered")




class SetPasswordForm(forms.Form):

    New_Password = forms.CharField(
        # label= ("New password"),
        widget=forms.PasswordInput,
        strip=False,


    )
    Confirm_New_Password = forms.CharField(
        # label= ("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )
    # return HttpResponse(New_Password)
    def clean_New_Password(self, data):
        pass

    def clean_New_Password(self, data):
        pass

    def clean(self):
        # return HttpResponse(self.cleaned_data['New_Password'])
        password1 = self.cleaned_data['New_Password']
        password2 = self.cleaned_data['Confirm_New_Password']
        # return HttpResponse(password1)
        # return HttpResponse(password2)
        if password1 and password2 and password1!=password2:
            # return HttpResponse("hii")
            raise ValidationError("password mismatch")
        return self.cleaned_data

    # def save(self, commit=True):
    #     password = self.cleaned_data["new_password1"]
    #     self.user.set_password(password)
    #     if commit:
    #         self.user.save()
    #     return self.user




