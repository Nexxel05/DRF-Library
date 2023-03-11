from django.contrib.auth import get_user_model
from rest_framework import serializers

from users_service.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_staff"
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data: dict) -> callable:
        return get_user_model().objects.create_user(**validated_data)

    def update(
            self,
            instance: Customer,
            validated_data: dict
    ) -> Customer:
        password = validated_data.pop("password", None)
        customer = super().update(instance, validated_data)
        if password:
            customer.set_password(password)
            customer.save()

        return customer
