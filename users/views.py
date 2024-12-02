from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token as AuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User, VerificationCode
from .serializers import (
    CodeSerializer,
    InviteCodeSerializer,
    PhoneNumberSerializer,
    UserProfileSerializer,
)
from .services import send_auth_code

auth_codes = {}


class SendCodeView(GenericAPIView):
    serializer_class = PhoneNumberSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            code = send_auth_code(phone_number)
            User.objects.get_or_create(phone_number=phone_number)

            # для тестирования отрпавляем код в ответе
            return Response(
                {"detail": "Код отправлен", "auth_code": code},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(GenericAPIView):
    serializer_class = CodeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            code = serializer.validated_data["code"]
            try:
                verification_code = VerificationCode.objects.get(
                    phone_number=phone_number, code=code, is_used=False
                )
            except VerificationCode.DoesNotExist:
                return Response(
                    {"detail": "Неверный код или номер телефона"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Проверяем, не истек ли код
            if verification_code.is_expired():
                return Response(
                    {"detail": "Код истек"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Помечаем код как использованный
            verification_code.is_used = True
            verification_code.save()

            # Аутентифицируем пользователя и выдаем токен
            user = User.objects.get(phone_number=phone_number)
            token, created = AuthToken.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "invite_code": user.invite_code},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivateInviteCodeView(GenericAPIView):
    serializer_class = InviteCodeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            invite_code = serializer.validated_data["invite_code"]
            user = request.user
            if user.activated_invite_code:
                return Response(
                    {"detail": "Инвайт-код уже активирован"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if invite_code == user.invite_code:
                return Response(
                    {"detail": "Нельзя активировать свой собственный инвайт-код"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                inviter = User.objects.get(invite_code=invite_code)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Инвайт-код не существует"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.activated_invite_code = invite_code
            user.invited_by = inviter
            user.save()
            return Response(
                {"detail": "Инвайт-код успешно активирован"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
