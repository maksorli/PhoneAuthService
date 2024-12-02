from rest_framework import serializers


def validate_phone_number(value):
    if not value.isdigit():
        raise serializers.ValidationError(
            "Номер телефона должен содержать только цифры."
        )
    if len(value) < 10:
        raise serializers.ValidationError(
            "Номер телефона должен содержать минимум 10 цифр."
        )
    return value
