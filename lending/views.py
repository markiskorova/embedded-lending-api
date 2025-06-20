from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Loan, Offer, Repayment
from .serializers import LoanSerializer, OfferSerializer, RepaymentSerializer
from users.models import Merchant
from django.shortcuts import get_object_or_404

class LoanCreateView(generics.CreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        merchant = get_object_or_404(Merchant, user=self.request.user)
        serializer.save(merchant=merchant, status='pending')

class LoanListView(generics.ListAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        merchant = get_object_or_404(Merchant, user=self.request.user)
        return Loan.objects.filter(merchant=merchant)

class OfferAcceptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        offer = get_object_or_404(Offer, id=pk)
        offer.is_accepted = True
        offer.save()
        loan = offer.loan
        loan.status = 'funded'
        loan.save()
        return Response({"detail": "Offer accepted and loan funded."}, status=status.HTTP_200_OK)

class RepaymentCreateView(generics.CreateAPIView):
    serializer_class = RepaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class PartnerMerchantStatusView(APIView):
    permission_classes = [permissions.AllowAny]  # Replace with API key/JWT check for production

    def get(self, request, merchant_id):
        merchant = get_object_or_404(Merchant, id=merchant_id)
        serializer = MerchantStatusSerializer(merchant)
        return Response(serializer.data)