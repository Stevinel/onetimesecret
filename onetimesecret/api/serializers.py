from rest_framework import serializers

from api.models import LIFE_TIME, Secret


class SecretCreateSerializer(serializers.ModelSerializer):
    lifetime = serializers.ChoiceField(choices=LIFE_TIME, default="1")

    class Meta:
        model = Secret
        fields = ["secret", "key_word", "lifetime"]


class SecretGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ["key_word"]
