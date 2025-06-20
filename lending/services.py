from .models import Offer

def create_dummy_offer(loan):
    return Offer.objects.create(
        loan=loan,
        amount=loan.principal_amount,
        interest_rate=5.0,
        duration_months=12,
    )
