from django.urls import path

from .views import SecretCreate, SecretUpdate

urlpatterns = [
    path("generate/", SecretCreate.as_view(), name="generate"),
    path("secrets/<slug:slug>/", SecretUpdate.as_view(), name="get_secret"),
]
