from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from users.models import Merchant
from .models import Loan

class LoanTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='merchant', password='testpass')
        self.merchant = Merchant.objects.create(user=self.user, company_name='TestCo')
        self.client.force_authenticate(user=self.user)

    def test_create_loan(self):
        data = {'principal_amount': '5000.00'}
        response = self.client.post('/api/loans/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Loan.objects.count(), 1)
