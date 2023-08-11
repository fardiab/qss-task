from django import forms

from profiles.models.sign_up import SignUpUser


class SignUpForm(forms.Form):
    GENDER = (
        ("male", "male"),
        ("female", "female"),
        ("other", "other")
    )
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    gender = forms.ChoiceField(choices=GENDER, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    company = forms.CharField(max_length=100, required=True)
    industry = forms.CharField(max_length=100, required=True)
    job_title = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput ,max_length=100, required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and SignUpUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email
    
    def cleaned_field(self):
        data = self.cleaned_data['password']
        return data
    