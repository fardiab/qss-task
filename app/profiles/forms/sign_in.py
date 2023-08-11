from django import forms
from django.contrib.auth import authenticate
from profiles.models.sign_in import SignInUser

class SignInForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput ,max_length=100, required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not SignInUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email does not exist.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
        return cleaned_data