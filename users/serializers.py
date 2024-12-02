from rest_framework import serializers
from rest_framework.authtoken.models import Token as AuthToken

from .models import User, VerificationCode
from .services import send_auth_code
from .validators import validate_phone_number


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[validate_phone_number])

    def create(self, validated_data):
        phone_number = validated_data["phone_number"]
        code = send_auth_code(phone_number)
        User.objects.get_or_create(phone_number=phone_number)
        validated_data["auth_code"] = code  # Для передачи в представление
        return validated_data


class CodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[validate_phone_number])
    code = serializers.CharField()
    token = serializers.CharField(read_only=True)
    invite_code = serializers.CharField(read_only=True)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        code = attrs.get("code")

        try:
            verification_code = VerificationCode.objects.get(
                phone_number=phone_number, code=code, is_used=False
            )
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Неверный код или номер телефона")

        if verification_code.is_expired():
            raise serializers.ValidationError("Код истек")

        attrs["verification_code"] = verification_code
        return attrs

    def create(self, validated_data):
        verification_code = validated_data.pop("verification_code")
        verification_code.is_used = True
        verification_code.save()

        phone_number = validated_data["phone_number"]
        user, _ = User.objects.get_or_create(phone_number=phone_number)
        token, _ = AuthToken.objects.get_or_create(user=user)

        return {
            "token": token.key,
            "invite_code": user.invite_code,
        }


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField()

    def validate_invite_code(self, value):
        user = self.context["request"].user

        if user.activated_invite_code:
            raise serializers.ValidationError("Инвайт-код уже активирован")

        if value == user.invite_code:
            raise serializers.ValidationError(
                "Нельзя активировать свой собственный инвайт-код"
            )

        if not User.objects.filter(invite_code=value).exists():
            raise serializers.ValidationError("Инвайт-код не существует")

        return value

    def create(self, validated_data):
        user = self.context["request"].user
        inviter = User.objects.get(invite_code=validated_data["invite_code"])
        user.activated_invite_code = validated_data["invite_code"]
        user.invited_by = inviter
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()
    inviter = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "phone_number",
            "invite_code",
            "activated_invite_code",
            "invited_users",
            "inviter",
        ]

    def get_invited_users(self, obj):
        return [user.phone_number for user in obj.invited_users.all()]

    def get_inviter(self, obj):
        inviter = obj.invited_by
        return inviter.phone_number if inviter else None
