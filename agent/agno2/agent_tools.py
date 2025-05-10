import json
import uuid
from datetime import datetime

from agno2.models import Invoice, User, PaymentCard  # Import PaymentCard model


def get_outstanding_invoices(user_id: str) -> dict:
    """
    Use this function to get information about outstanding invoices from the telco billing system.

    Args:
        user_id (str): The phone number to retrieve outstanding invoice information for.

    Returns:
        dict: JSON object containing outstanding invoice information including:
            - Total amount due
            - Number of outstanding invoices
            - List of invoices with details (invoice ID, date, amount, due date, status)
            - Payment history
    """
    try:
        # Get the user
        user = User.objects.get(customer_id=user_id)

        # Get all outstanding invoices for the user
        outstanding_invoices = Invoice.objects.filter(
            user=user, status__in=['pending', 'overdue']
        ).order_by('due_date')

        # Convert to list of dictionaries
        invoices_list = [
            {
                'invoice_id': invoice.invoice_id,
                'issue_date': invoice.issue_date.isoformat() + 'Z',
                'due_date': invoice.due_date.isoformat() + 'Z',
                'amount': float(invoice.amount),
                'status': invoice.status,
                'description': invoice.description,
            }
            for invoice in outstanding_invoices
        ]

        return json.dumps(
            {
                'status': 'success',
                'data': {
                    'user_id': user_id,
                    'invoices': invoices_list,
                },
            }
        )
    except User.DoesNotExist:
        return json.dumps(
            {
                'status': 'error',
                'data': {'message': f'User with ID {user_id} not found.'},
            }
        )


def get_available_cards(user_id: str) -> dict:
    """
    Use this function retrieve the available card that can be used to pay the invoice

    Args:
        user_id (str): The phone number to retrieve billing information for.

    Returns:
        List of dicts: JSON object containing payment methods including:
            - card_number
            - expiration_date
            - payment_method_id
    """
    try:
        # Get the user
        user = User.objects.get(customer_id=user_id)

        # Get all payment cards for the user
        payment_cards = PaymentCard.objects.filter(user=user)

        payment_methods = [
            {
                'card_number': card.card_number,
                'expiration_date': card.expiration_date.strftime('%m/%Y'),
                'payment_method_id': card.payment_method_id,
            }
            for card in payment_cards
        ]

        return json.dumps({'status': 'success', 'data': {'payment_methods': payment_methods}})
    except User.DoesNotExist:
        return json.dumps(
            {
                'status': 'error',
                'data': {'message': f'User with ID {user_id} not found.'},
            }
        )


def add_card(user_id: str, card_number: str, expiration_date: str) -> dict:
    """
    Use this function to add a card to the payment system.

    Args:
        user_id (str): The phone number to add the payment method for.
        card_number (str): The full card number.
        expiration_date (str): The expiration date of the payment method (format: "MM/YYYY").

    Returns:
        dict: JSON object containing the result of the operation and the added payment method.
    """
    try:
        # Get the user
        user = User.objects.get(customer_id=user_id)

        # Parse expiration date
        exp_date = datetime.strptime(expiration_date, '%m/%Y').date()

        # Create new payment card
        payment_card = PaymentCard.objects.create(
            user=user,
            card_number=card_number,
            expiration_date=exp_date,
            payment_method_id=f'card_{uuid.uuid4().hex[:8]}',
        )

        return json.dumps(
            {
                'status': 'success',
                'data': {
                    'message': 'Card added successfully',
                    'added_card': {
                        'card_number': card_number,
                        'expiration_date': expiration_date,
                        'payment_method_id': payment_card.payment_method_id,
                    },
                },
            }
        )
    except User.DoesNotExist:
        return json.dumps(
            {
                'status': 'error',
                'data': {'message': f'User with ID {user_id} not found.'},
            }
        )
    except ValueError:
        return json.dumps(
            {
                'status': 'error',
                'data': {'message': 'Invalid expiration date format. Please use MM/YYYY format.'},
            }
        )


def make_payment(user_id: str, invoice_id: str, payment_method_id: str = None) -> dict:
    """
    Use this function to pay an outstanding invoice in the telco billing system.

    Args:
        user_id (str): The phone number of the user making the payment.
        invoice_id (str): The ID of the invoice to be paid.
        payment_method_id (str, optional): The ID of the payment method to use.
                                          If not provided, the default payment method will be used.

    Returns:
        dict: JSON object containing the result of the payment operation including:
            - Transaction ID
            - Payment status
            - Payment date
            - Amount paid
            - Updated invoice status
    """
    try:
        # Get the user
        user = User.objects.get(customer_id=user_id)

        # Find the invoice for the user
        invoice = Invoice.objects.get(invoice_id=invoice_id, user=user)

        # Update the invoice status
        invoice.status = 'paid'
        invoice.save()

        return json.dumps(
            {
                'status': 'success',
                'data': {
                    'message': 'Payment processed successfully',
                    'transaction_id': f'TXN-{uuid.uuid4().hex[:8].upper()}',
                    'invoice_status': invoice.status,
                },
            }
        )
    except Invoice.DoesNotExist:
        return json.dumps(
            {
                'status': 'error',
                'data': {'message': f'Invoice with ID {invoice_id} not found for user {user_id}.'},
            }
        )
    except User.DoesNotExist:
        return json.dumps(
            {
                'status': 'error',
                'data': {'message': f'User with ID {user_id} not found.'},
            }
        )


def validate_phone_number(phone_number: str) -> dict:
    """
    Use this function to validate if a phone number is valid in the system.

    Args:
        phone_number (str): The phone number to validate.

    Returns:
        dict: JSON object containing validation result:
            - is_valid: Boolean indicating if the phone number is valid
            - message: Description of the validation result
    """
    try:
        # Check if the phone number starts with +1
        if not phone_number.startswith('+1'):
            return json.dumps(
                {
                    'status': 'error',
                    'data': {'is_valid': False, 'message': 'Invalid phone number format'},
                }
            )

        # Check if user exists in database
        User.objects.get(customer_id=phone_number)

        return json.dumps(
            {
                'status': 'success',
                'data': {'is_valid': True, 'message': 'Valid phone number'},
            }
        )
    except User.DoesNotExist:
        return json.dumps(
            {
                'status': 'error',
                'data': {'is_valid': False, 'message': 'Client not found'},
            }
        )
