import requests
import json
from faker import Faker

fake = Faker()

def test_create_user():
    # API endpoint
    url = "http://localhost:8000/api/users/create/"
    
    # Generate a random phone number
    phone_number = fake.numerify("+1##########")  # US format: +1XXXXXXXXXX
    
    # Request payload
    payload = {
        "phone_number": phone_number
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Print the response
        print(f"\nPhone Number: {phone_number}")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        
        return response.status_code == 201  # Check if user was created successfully
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return False

if __name__ == "__main__":
    print("Testing Create User API...")
    success = test_create_user()
    print(f"\nTest {'passed' if success else 'failed'}") 