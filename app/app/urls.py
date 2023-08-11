"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apis.schema import schema

schema_view = get_schema_view(
    openapi.Info(
        title="Pastebin API",
        default_version="v1",
        description="API for Pastebin",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("a1/api-auth/", include("rest_framework.urls")),
    path(
        "a1/api-docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/", include("apis.urls")),
    path("a2/", include("users.urls")),
    path("a3/", include("profiles.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
