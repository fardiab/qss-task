from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.all, name='all'),
    # path('country-rank/', views.country_rank_data, name='country-rank'),
    # path('import-csv/', views.import_csv, name='import-csv'),
]