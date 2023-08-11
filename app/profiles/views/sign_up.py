from django.shortcuts import render
from django.contrib.auth import get_user_model
from profiles.forms import *
from profiles.models import *


User = get_user_model()

def sign_up_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create a User instance
            user = User.objects.create_user(email=email, password=password)

            # Create a SignUpUser instance and associate it with the User
            sign_up_user = SignUpUser(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                gender=form.cleaned_data['gender'],
                phone_number=form.cleaned_data['phone_number'],
                company=form.cleaned_data['company'],
                industry=form.cleaned_data['industry'],
                job_title=form.cleaned_data['job_title'],
                email=email,
                password=password
            )
            sign_up_user.set_password(password)
            sign_up_user.save()
            return render(request, "profiles/sign_up.html", {"form": form})
    else:
        form = SignUpForm()
    return render(request, "profiles/sign_up.html", {"form": form})