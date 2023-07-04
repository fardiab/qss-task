from django.urls import path, include

from . import views

urlpatterns = [
    path('sectors/', views.SectViewSet.as_view({'get': 'list'}), name='sectors'),
    path('subsectors/', views.SubSectApiView.as_view(), name='subsectors'),
    path('indicators/',  views.IndicaApiView.as_view(), name='indicators'),
    path('indicators/<int:pk>/', views.IndicaApiView.as_view(), name='indicators-detail'),
    path('country/', views.CountryApiView.as_view(), name='country'),
    path('rank-difference/', views.RankDifferenceApiView.as_view(), name='rank_difference'),
    path('country-info/', views.CountryInfoApiView.as_view(), name='country_info'),
    path('country-diagram/', views.CountryIndicaDiagramApiView.as_view(), name='country_diagram'),
    path('country-rank-difference/', views.CountryIndicaRankDifferenceApiView.as_view(), name='country_rank_difference'),
    # path('country-ranks/<int:pk>/', views.CountryRankApiView.as_view(), name='country-ranks-detail'),
]