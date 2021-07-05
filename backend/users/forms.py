from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# getting user model
User = get_user_model()

class UserCreateFormAdmin(forms.ModelForm):
    """
    The form we can create user in admin panel
    """
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    repeated_password = forms.CharField(widget=forms.PasswordInput, label="تایید رمز عبور")
    
    class Meta:
        model = User
        fields = ["email", "username", "password", "phone_number", "repeated_password"]

    def clean_repeated_password(self):
        data = self.cleaned_data
        if data["password"] and data["repeated_password"] and data["password"] != data["repeated_password"]:
            raise forms.ValidationError("رمز و تایید آن باید یکی باشد")
        return data["repeated_password"] 

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeFormAdmin(forms.ModelForm):
    """
    The form we can change user's information and update it
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "username", "phone_number", "password"]

    def clean_password(self):
        return self.initial["password"]    