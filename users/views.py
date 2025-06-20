from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, MerchantSerializer
from .models import Merchant

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MerchantProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        merchant = Merchant.objects.get(user=request.user)
        serializer = MerchantSerializer(merchant)
        return Response(serializer.data)
