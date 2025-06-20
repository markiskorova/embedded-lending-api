from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Merchant

class RegisterSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'company_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        company_name = validated_data.pop('company_name')
        user = User.objects.create_user(**validated_data)
        Merchant.objects.create(user=user, company_name=company_name)
        return user

class MerchantSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Merchant
        fields = ['user', 'company_name', 'created_at']
