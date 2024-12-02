from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    CodeSerializer,
    InviteCodeSerializer,
    PhoneNumberSerializer,
    UserProfileSerializer,
)


class SendCodeView(CreateAPIView):
    serializer_class = PhoneNumberSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(
            {"detail": "Код отправлен", "auth_code": data["auth_code"]},
            status=status.HTTP_200_OK,
        )


class VerifyCodeView(CreateAPIView):
    serializer_class = CodeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(
            {"token": data["token"], "invite_code": data["invite_code"]},
            status=status.HTTP_200_OK,
        )


class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user


class ActivateInviteCodeView(CreateAPIView):
    serializer_class = InviteCodeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Инвайт-код успешно активирован"},
            status=status.HTTP_200_OK,
        )
