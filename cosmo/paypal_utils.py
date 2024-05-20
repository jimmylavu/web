import paypalrestsdk
from django.conf import settings

# Configure PayPal SDK with your client credentials
paypalrestsdk.configure({
    "mode": settings.PAYPAL_TEST,  # Use PAYPAL_TEST setting
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET_KEY
})

def get_transaction_details(payment_id):
    try:
        # Retrieve payment details from PayPal using the transaction ID (payment_id)
        transaction = paypalrestsdk.Payment.find(payment_id)
        
        # Check if transaction is found and return details
        if transaction:
            return transaction.to_dict()
        else:
            return None

    except paypalrestsdk.exceptions.ResourceNotFound as error:
        # Handle resource not found error (e.g., invalid payment ID)
        print(f"Error retrieving transaction details: {error}")
        return None

    except Exception as error:
        # Handle other exceptions
        print(f"Error retrieving transaction details: {error}")
        return None
