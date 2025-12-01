from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import re
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'category']
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        
        
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 10:
            raise forms.ValidationError("Password must be at least 10 characters long.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*]", password):
            raise forms.ValidationError("Password must contain at least one special character (!@#$%^&*).")
        return password
