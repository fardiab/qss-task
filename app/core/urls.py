from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.all, name='all'),
    # path('agriculture/', views.agriculture, name='agriculture'),
    # path('army/', views.army, name='army'),
    # path('economy/', views.economy, name='economy'),
    # path('government/', views.government, name='government'),
    # path('health/', views.health, name='health'),
    # path('social/', views.social, name='social'),
    # path('techology/', views.technology, name='technology'),
    # path('transportation/', views.transportation, name='transportation'),
    # path('other/', views.other, name='other'),
    # path('<int:pk>/', views.details, name='details'),
]