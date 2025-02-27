from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    VerifyTOTPSerializer,
    ChangePasswordSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"user": UserSerializer(user).data, "message": "User created successfully"},
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class Enable2FAView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        # Delete existing devices
        TOTPDevice.objects.filter(user=user).delete()
        # Create new device
        device = TOTPDevice.objects.create(user=user, name="Default")
        user.is_2fa_enabled = True
        user.save()

        return Response(
            {
                "otpauth_url": device.config_url,
                "secret_key": device.config_url.split("secret=")[1].split("&")[0],
            }
        )


class Verify2FAView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = VerifyTOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        device = TOTPDevice.objects.get(user=user)

        if device.verify_token(serializer.validated_data["token"]):
            return Response({"message": "2FA verification successful"})
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.data.get("old_password")):
            return Response(
                {"error": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(
            {"message": "Password updated successfully"}, status=status.HTTP_200_OK
        )
