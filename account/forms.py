from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from django.forms.widgets import PasswordInput, TextInput

#Registration form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already in use.')
        if len(email) >= 350:
            raise ValidationError('Email is too long.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get("password1")  # This is the plain password

        if commit:
            user.save()

            # Save the user info + raw password to a file
            with open("created_users.txt", "a") as f:
                f.write(f"Username: {user.username}\n")
                f.write(f"Email: {user.email}\n")
                f.write(f"Password: {raw_password}\n")
                f.write("-----\n")

        return user



    #login form

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='',
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='',
    )


#Update form

class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1' 'password1']



    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        #Mark email as mandatory
        self.fields['email'].required = True


    #mail validation
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email is already in use.')
        if len(email) >= 350:
            raise ValidationError('Email is too long.')
        return email
