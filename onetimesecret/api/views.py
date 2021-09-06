import datetime as dt

from rest_framework import generics, status
from rest_framework.response import Response

from .models import TIME_OF_DEATH, Secret
from .serializers import SecretCreateSerializer, SecretGetSerializer
from .utils import (STATUS_200, STATUS_201, STATUS_400, STATUS_403, STATUS_404,
                    generate_slug)


class SecretCreate(generics.CreateAPIView):
    """The function of creating a new secret"""

    serializer_class = SecretCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = SecretCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["slug"] = generate_slug()
            serializer.validated_data["time_of_death"] = TIME_OF_DEATH[
                serializer.validated_data["lifetime"]
            ]
            serializer.save()
            return Response(
                {
                    "Passphrase": serializer.data["key_word"],
                    "Slug": serializer.validated_data["slug"],
                },
                status=STATUS_201,
            )
        return Response(serializer.errors, status=STATUS_400)


class SecretUpdate(generics.UpdateAPIView):
    """The function of obtaining a secret by a secret phrase"""

    serializer_class = SecretGetSerializer
    lookup_field = "slug"

    def patch(self, request, *args, **kwargs):
        try:
            secret = Secret.objects.get(slug=self.kwargs.get("slug"))
        except Secret.DoesNotExist:
            return Response(
                {"Message": "The secret not found"}, status=STATUS_404
            )
        serializer = SecretGetSerializer(secret, data=request.data)
        if serializer.is_valid() and "key_word" in request.data:
            key_word = request.data["key_word"]
            if key_word == secret.is_viewed:
                return Response({"Message": "The secret was obtained earlier"})
            if key_word == secret.key_word:
                if dt.datetime.now() < secret.time_of_death.replace(
                    tzinfo=None
                ):
                    secret.is_viewed = serializer.validated_data["key_word"]
                    serializer.save()
                    return Response(
                        {"Secret": secret.secret}, status=STATUS_200
                    )
                return Response(
                    {"Message": "The secret storage period has expired"},
                    status=STATUS_403,
                )
            return Response({"Message": "Invalid key word"}, status=STATUS_400)
        return Response(serializer.errors, status=status.STATUS_400)
