from django.urls import path
from .views import LoanCreateView, LoanListView, OfferAcceptView, RepaymentCreateView, PartnerMerchantStatusView

urlpatterns = [
    path('loans/', LoanCreateView.as_view(), name='loan-create'),
    path('loans/list/', LoanListView.as_view(), name='loan-list'),
    path('offers/<int:pk>/accept/', OfferAcceptView.as_view(), name='offer-accept'),
    path('repayments/', RepaymentCreateView.as_view(), name='repayment-create'),
    path('partner/merchant/<int:merchant_id>/status/', PartnerMerchantStatusView.as_view(), name='partner-merchant-status'),
]
