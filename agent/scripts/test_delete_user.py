import argparse
import json

import requests


def test_delete_user(customer_id):
    # API endpoint
    url = f'http://localhost:8000/api/users/delete/{customer_id}/'

    try:
        # Make the POST request
        response = requests.post(url)

        # Print the response
        print(f'\nCustomer ID: {customer_id}')
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(json.dumps(response.json(), indent=2))

        return response.status_code == 200  # Check if user was deleted successfully

    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the Delete User API')
    parser.add_argument('customer_id', help='Customer ID of the user to delete')

    args = parser.parse_args()

    print('Testing Delete User API...')
    success = test_delete_user(args.customer_id)
    print(f"\nTest {'passed' if success else 'failed'}")
