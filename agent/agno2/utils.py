import json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()


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
    issue_date = fake.date_time_between(start_date='-30d', end_date='now')
    due_date = issue_date + timedelta(days=30)

    invoice_data = {
        'invoice_id': f'INV-{fake.uuid4()}',
        'issue_date': issue_date.isoformat() + 'Z',
        'due_date': due_date.isoformat() + 'Z',
        'amount': 89.99,
        'status': 'overdue',
        'description': f'Invoice for {user_data["subscription"]["plan_name"]} plan',
    }

    invoice = Invoice.from_invoice_data(user, invoice_data)

    return user
