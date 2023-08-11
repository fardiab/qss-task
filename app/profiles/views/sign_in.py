from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

from profiles.forms import *
from profiles.models import *



def sign_in_view(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("success")  # Redirect to a success page or desired URL
            else:
                print("Form has errors:", form.errors)
                # Authentication failed
                form.add_error(None, "Invalid email or password")
    else:
        print("nothing")
        form = SignInForm()
    return render(request, "profiles/sign_in.html", {"form": form})

def success_page(request):
    return render(request, "profiles/success.html")