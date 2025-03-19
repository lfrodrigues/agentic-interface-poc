import json
import uuid


def get_information_from_billing_system(user_id: str) -> dict:
    """
    Use this function to get credit information from the telco billing system.

    Args:
        user_id (str): The phone number to retrieve billing information for.

    Returns:
        dict: JSON object containing credit information including:
            - Available credit
            - Voice, data, and SMS balances
            - Active subscriptions and bundles
    """
    return json.dumps(
        {
            "status": "success",
            "data": {
                "user_id": user_id,
                "available_credit": 100.00,
                "last_updated": "2024-03-20T10:30:00Z",
                "credit_status": "normal",
                "pending_transactions": 0,
                "currency": "USD",
                "voice_balance": 50.00,
                "data_balance": "2.5GB",
                "sms_balance": 100,
                "active_bundles": [
                    {
                        "name": "Premium Data",
                        "remaining": "1.5GB",
                        "expiry": "2024-03-25T23:59:59Z",
                    }
                ],
            },
        }
    )


global_outstanding_invoices = [
    {
        "invoice_id": "INV-2024-0342",
        "issue_date": "2024-03-01T00:00:00Z",
        "due_date": "2024-03-15T23:59:59Z",
        "amount": 89.99,
        "status": "overdue",
        "description": "Monthly service charge - March 2024",
    },
]


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
    return json.dumps(
        {
            "status": "success",
            "data": {"user_id": user_id, "invoices": global_outstanding_invoices},
        }
    )


def get_user_information(user_id: str) -> dict:
    """
    Use this function to retrieve user information from the telco customer database.

    This function queries the customer database to retrieve comprehensive user information
    including profile details, subscription information, service status, billing details,
    device information, and user preferences.

    Args:
        user_id (str): The phone number to retrieve user information for.

    Returns:
        dict: JSON object containing user information including:
            - User profile (customer ID, name, email, phone, status)
            - Subscription details (plan, dates, renewal status)
            - Services information (voice, data, SMS, roaming)
            - Billing details (address, payment method, cycle)
            - Device information (ID, model, IMEI, status)
            - User preferences (language, timezone, notifications)
    """
    return json.dumps(
        {
            "status": "success",
            "data": {
                "user_profile": {
                    "customer_id": "CUST123456",
                    "full_name": "John Doe",
                    "email": "john.doe@example.com",
                    "user_id": user_id,
                    "account_status": "active",
                    "registration_date": "2023-01-15T00:00:00Z",
                },
                "subscription": {
                    "plan_name": "Premium Plus",
                    "plan_type": "postpaid",
                    "start_date": "2023-01-15T00:00:00Z",
                    "renewal_date": "2024-01-15T00:00:00Z",
                    "auto_renewal": True,
                },
                "services": {"voice": True, "data": True, "sms": True, "roaming": True},
                "billing": {
                    "billing_address": {
                        "street": "123 Main St",
                        "city": "New York",
                        "state": "NY",
                        "zip": "10001",
                        "country": "USA",
                    },
                    "payment_method": "credit_card",
                    "billing_cycle": "monthly",
                },
            },
        }
    )


# global_payment_methods = []

global_payment_methods = [
    # {
    #     "user_id": "asasd",
    #     "card_number": "1111 1111 1111 1111",
    #     "expiration_date": "12/2025",
    #     "payment_method_id": "card_1111",
    # }
]


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

    payment_methods = [
        {
            "card_number": x.get("card_number"),
            "expiration_date": x.get("expiration_date"),
            "payment_method_id": x.get("payment_method_id"),
        }
        for x in global_payment_methods
    ]

    return json.dumps(
        {"status": "success", "data": {"payment_methods": payment_methods}}
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
    new_payment_method = {
        "user_id": user_id,
        "card_number": card_number,
        "expiration_date": expiration_date,
        "payment_method_id": "card_1111",
    }

    global_payment_methods.append(new_payment_method)

    return json.dumps(
        {
            "status": "success",
            "data": {
                "message": "Card added successfully",
                "added_card": {
                    "card_number": card_number,
                    "expiration_date": expiration_date,
                    "payment_method_id": "card_1111",
                },
            },
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
    # Find the invoice in the global outstanding invoices
    invoice_to_pay = None
    for invoice in global_outstanding_invoices:
        if invoice["invoice_id"] == invoice_id:
            invoice_to_pay = invoice
            break

    if not invoice_to_pay:
        return json.dumps(
            {
                "status": "error",
                "data": {
                    "message": f"Invoice with ID {invoice_id} not found for user {user_id}."
                },
            }
        )

    # Update the invoice status
    invoice_to_pay["status"] = "paid"

    # Remove the invoice from outstanding invoices
    global_outstanding_invoices.remove(invoice_to_pay)

    return json.dumps(
        {
            "status": "success",
            "data": {
                "message": "Payment processed successfully",
                "transaction_id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
                "invoice_status": invoice_to_pay["status"],
            },
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
    # Check if the phone number starts with +1
    is_valid = phone_number.startswith("+1")

    if is_valid:
        return json.dumps(
            {
                "status": "success",
                "data": {"is_valid": True, "message": "Valid phone number"},
            }
        )
    else:
        return json.dumps(
            {
                "status": "error",
                "data": {"is_valid": False, "message": "Client not found"},
            }
        )


def get_available_packages(user_id: str) -> dict:
    """
    Use this function to retrieve available telco packages for a user.
    The first package in the list is the user's current active package.

    Args:
        user_id (str): The phone number to retrieve available packages for.

    Returns:
        dict: JSON object containing available package information including:
            - List of packages with details (name, price, data, voice, SMS, features)
            - Current active package is listed first
    """
    # Get user information to determine current package
    user_info = json.loads(get_user_information(user_id))
    current_plan_name = user_info["data"]["subscription"]["plan_name"]
    
    # Define available packages
    packages = [
        {
            "package_id": "PKG-001",
            "name": "Premium Plus",
            "price": 89.99,
            "currency": "USD",
            "billing_cycle": "monthly",
            "data": {
                "amount": "Unlimited",
                "high_speed_cap": "50GB",
                "throttle_speed": "3Mbps"
            },
            "voice": {
                "minutes": "Unlimited",
                "international": True
            },
            "sms": {
                "messages": "Unlimited",
                "international": True
            },
            "features": [
                "5G Access",
                "Mobile Hotspot (30GB)",
                "HD Streaming",
                "International Roaming"
            ],
            "is_current": True
        },
        {
            "package_id": "PKG-002",
            "name": "Standard",
            "price": 59.99,
            "currency": "USD",
            "billing_cycle": "monthly",
            "data": {
                "amount": "25GB",
                "high_speed_cap": "25GB",
                "throttle_speed": "2Mbps"
            },
            "voice": {
                "minutes": "Unlimited",
                "international": False
            },
            "sms": {
                "messages": "Unlimited",
                "international": False
            },
            "features": [
                "5G Access",
                "Mobile Hotspot (10GB)",
                "SD Streaming"
            ],
            "is_current": False
        },
        {
            "package_id": "PKG-003",
            "name": "Basic",
            "price": 39.99,
            "currency": "USD",
            "billing_cycle": "monthly",
            "data": {
                "amount": "10GB",
                "high_speed_cap": "10GB",
                "throttle_speed": "1Mbps"
            },
            "voice": {
                "minutes": 1000,
                "international": False
            },
            "sms": {
                "messages": 1000,
                "international": False
            },
            "features": [
                "4G Access",
                "Mobile Hotspot (5GB)"
            ],
            "is_current": False
        }
    ]
    
    return json.dumps(
        {
            "status": "success",
            "data": {
                "user_id": user_id,
                "current_package": current_plan_name,
                "available_packages": packages
            }
        }
    )


def activate_package(user_id: str, package_name: str) -> dict:
    """
    Use this function to activate a new telco package for a user.

    Args:
        user_id (str): The phone number of the user activating the package.
        package_name (str): The name of the package to activate (e.g., "Premium Plus", "Standard", "Basic").

    Returns:
        dict: JSON object containing the result of the activation including:
            - Activation status
            - Transaction ID
            - New package details
            - Effective date
            - Prorated billing information
    """
    # Get available packages to validate the requested package
    available_packages_response = json.loads(get_available_packages(user_id))
    available_packages = available_packages_response["data"]["available_packages"]
    current_package = available_packages_response["data"]["current_package"]
    
    # Find the requested package
    package_to_activate = None
    for package in available_packages:
        if package["name"].lower() == package_name.lower():
            package_to_activate = package
            break
    
    # If package not found
    if not package_to_activate:
        return json.dumps(
            {
                "status": "error",
                "data": {
                    "message": f"Package '{package_name}' not found. Please choose from available packages."
                },
            }
        )
    
    # If package is already active
    if package_to_activate["name"] == current_package:
        return json.dumps(
            {
                "status": "error",
                "data": {
                    "message": f"Package '{package_name}' is already active for user {user_id}."
                },
            }
        )
        
    return json.dumps(
        {
            "status": "success",
            "data": {
                "message": f"Package '{package_name}' activated successfully",
            },
        }
    )
