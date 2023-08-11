from django.urls import path, include

from .views import *

urlpatterns = [
    path('sign-up/', sign_up_view, name='sign-up'),
    path('sign-in/', sign_in_view, name='sign-in'),
    path('success/', success_page, name='success'),
]
