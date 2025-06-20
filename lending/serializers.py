from rest_framework import serializers
from .models import Loan, Offer, Repayment
from users.models import Merchant

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['status', 'created_at', 'merchant']

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['created_at', 'is_accepted']

class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = '__all__'
        read_only_fields = ['paid_at']
class RepaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = ['id', 'amount_paid', 'paid_at']

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'amount', 'interest_rate', 'duration_months', 'is_accepted']

class LoanDetailSerializer(serializers.ModelSerializer):
    offers = OfferDetailSerializer(source='offer_set', many=True, read_only=True)
    repayments = RepaymentDetailSerializer(source='repayment_set', many=True, read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'principal_amount', 'status', 'created_at', 'offers', 'repayments']

class MerchantStatusSerializer(serializers.ModelSerializer):
    loans = LoanDetailSerializer(source='loan_set', many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Merchant
        fields = ['user', 'company_name', 'loans']
