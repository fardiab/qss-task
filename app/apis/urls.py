from django.urls import path, include

from . import views

urlpatterns = [
    path('sectors/', views.SectViewSet.as_view({'get': 'list'}), name='sectors'),
    path('subsectors/', views.SubSectApiView.as_view(), name='subsectors'),
    path('indicators/', views.IndicaApiView.as_view(), name='indicators'),
    path('indicators/<int:pk>/', views.IndicaApiView.as_view(), name='indicators-detail'),
]