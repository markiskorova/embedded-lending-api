from django.contrib.auth.models import User
from .models import Merchant

def create_user_and_merchant(username, password, company_name):
    user = User.objects.create_user(username=username, password=password)
    merchant = Merchant.objects.create(user=user, company_name=company_name)
    return user, merchant
