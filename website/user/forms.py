from django import forms

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from user.models import User


class CreateUserForm(forms.ModelForm):
    # TODO: Добавить валидацию полей
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'avatar')
        widgets = {"password": forms.PasswordInput}

    def clean_password(self):
        return PasswordHasher().hash(self.cleaned_data.get("password"))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        try:
            PasswordHasher().verify(password1, password2)
        except VerificationError:
            raise forms.ValidationError("Passwords don't match")
        return password2


class AuthUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
