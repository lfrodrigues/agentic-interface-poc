import json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()


def generate_invoice_data(user, status='overdue'):
    """
    Generate random invoice data for a user.

    Args:
        user (User): The user to create the invoice for
        status (str): The status of the invoice (pending, paid, overdue, cancelled)

    Returns:
        dict: Randomly generated invoice data
    """
    # Generate random dates
    issue_date = fake.date_time_between(start_date='-30d', end_date='now')
    due_date = issue_date + timedelta(days=30)

    # Generate random amount between 50 and 500
    amount = fake.random_int(min=50, max=500)

    # Generate random description
    descriptions = [
        f'Monthly subscription for {user.plan_name} plan',
        f'Data usage charges for {fake.month()}',
        f'International calls and roaming charges',
        f'Additional services and features',
        f'Device installment payment',
        f'Premium content subscription',
        f'Service activation fee',
        f'Equipment upgrade fee',
    ]

    invoice_data = {
        'invoice_id': f'INV-{fake.uuid4()}',
        'issue_date': issue_date.isoformat() + 'Z',
        'due_date': due_date.isoformat() + 'Z',
        'amount': amount,
        'status': status,
        'description': fake.random_element(elements=descriptions),
    }

    return invoice_data


def create_user(phone_number: str):
    """
    Create or update a user in the database with randomly generated data.

    Args:
        phone_number (str): The phone number to use as the customer ID

    Returns:
        User: The created or updated User instance
    """
    from .models import User, Invoice  # Import here to avoid circular imports

    # Generate random dates
    registration_date = fake.date_time_between(start_date='-1y', end_date='now')
    renewal_date = registration_date + timedelta(days=365)

    # Generate user data
    user_data = {
        'user_profile': {
            'customer_id': phone_number,
            'full_name': fake.name(),
            'email': fake.email(),
            'account_status': fake.random_element(elements=('active', 'suspended', 'pending')),
            'registration_date': registration_date.isoformat() + 'Z',
        },
        'subscription': {
            'plan_name': fake.random_element(
                elements=('Basic', 'Premium', 'Premium Plus', 'Enterprise')
            ),
            'plan_type': fake.random_element(elements=('prepaid', 'postpaid')),
            'start_date': registration_date.isoformat() + 'Z',
            'renewal_date': renewal_date.isoformat() + 'Z',
            'auto_renewal': fake.boolean(chance_of_getting_true=80),
        },
        'services': {
            'voice': fake.boolean(chance_of_getting_true=90),
            'data': fake.boolean(chance_of_getting_true=95),
            'sms': fake.boolean(chance_of_getting_true=85),
            'roaming': fake.boolean(chance_of_getting_true=70),
        },
        'billing': {
            'billing_address': {
                'street': fake.street_address(),
                'city': fake.city(),
                'state': fake.state_abbr(),
                'zip': fake.zipcode(),
                'country': 'USA',
            },
            'payment_method': fake.random_element(elements=('credit_card')),
            'billing_cycle': fake.random_element(elements=('monthly', 'quarterly', 'annual')),
        },
    }

    # Create or update user in database
    user = User.from_user_information(user_data)

    # Create an invoice for the user
    invoice_data = generate_invoice_data(user, status='overdue')

    invoice = Invoice.from_invoice_data(user, invoice_data)

    return user
