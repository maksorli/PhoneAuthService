from rest_framework import serializers

from .models import User


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Номер телефона должен содержать только цифры."
            )
        if len(value) < 10:
            raise serializers.ValidationError(
                "Номер телефона должен содержать минимум 10 цифр."
            )
        return value


class CodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError("Код должен состоять из 4 цифр.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()
    activated_invite_code = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "phone_number",
            "invite_code",
            "activated_invite_code",
            "invited_users",
            "invited_by_id",
        ]

    def get_invited_users(self, obj) -> list:
        users = obj.invited_users.all()
        return [user.phone_number for user in users]

    def get_inviter(self, obj):
        inviter = obj.invited_by
        return inviter.phone_number if inviter else None


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

    def validate_invite_code(self, value):
        if not User.objects.filter(invite_code=value).exists():
            raise serializers.ValidationError("Инвайт-код не существует.")
        return value
