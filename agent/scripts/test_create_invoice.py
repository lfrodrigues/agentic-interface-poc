import argparse
import json

import requests


def test_create_invoice(customer_id):
    # API endpoint
    url = 'http://localhost:8000/api/invoices/create/'

    # Request payload
    payload = {'customer_id': customer_id}

    try:
        # Make the POST request
        response = requests.post(url, json=payload)

        # Print the response
        print(f'\nCustomer ID: {customer_id}')
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(json.dumps(response.json(), indent=2))

        return response.status_code == 201  # Check if invoice was created successfully

    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the Create Invoice API')
    parser.add_argument('customer_id', help='Customer ID of the user to create invoice for')

    args = parser.parse_args()

    print('Testing Create Invoice API...')
    success = test_create_invoice(args.customer_id)
    print(f"\nTest {'passed' if success else 'failed'}")
