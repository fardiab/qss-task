from django.urls import path, include

from .apis.user import * 

urlpatterns = [
    path('user/', UserApiView.as_view(), name='user'),
]