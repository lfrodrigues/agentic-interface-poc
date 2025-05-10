from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from agno2.agent import start_agent
from agno2.interface import start_agent_jsx, start_agent_json
from api.serializers import MessageInputSerializer, UserCreateSerializer
import uuid
from textwrap import dedent
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import User
from agno2.tools import get_user_information, validate_phone_number
import random
import string
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()


def generate_random_user_data(phone_number):
    """Generate random user data using Faker."""
    registration_date = fake.date_time_between(start_date='-1y', end_date='now')
    renewal_date = registration_date + timedelta(days=365)

    return json.dumps(
        {
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
    )


class TalkAgentView(APIView):
    """
    API endpoint for talking to an agent
    """

    def post(self, request, format=None):
        serializer = MessageInputSerializer(data=request.data)

        if serializer.is_valid():
            message_text = serializer.validated_data['message']
            session_id = serializer.validated_data['session_id']

            if session_id == 'NEW':
                session_id = str(uuid.uuid4())
                jsx_text = dedent("""
                   <View>
                        <Text>What do you want do to today?</Text>
                        <TextInput 
                            name="message"
                            placeholder="Write here what you want" 
                            onChangeText={storeData}
                        />
                        <Button title="Let's go!" onPress={handleSubmit} />
                    </View>
                """)
                agent_json = start_agent_json()
                response_json = agent_json.run(jsx_text)
                print('*******  JSON')
                print(response_json.get_content_as_string())

                return Response(
                    {
                        'message': json.loads(response_json.content),
                        'session_id': session_id,
                    },
                    status=status.HTTP_200_OK,
                )

            agent = start_agent(session_id)

            # response = agent.print_response(message_text)
            response = agent.run(message_text)
            print('*******  AGENT')
            print(response.get_content_as_string())

            agent_jsx = start_agent_jsx()
            response_jsx = agent_jsx.run(response.content)
            print('*******  JSX')
            print(response_jsx.get_content_as_string())

            agent_json = start_agent_json()
            response_json = agent_json.run(response_jsx.content)
            print('*******  JSON')
            print(response_json.get_content_as_string())

            return Response(
                {
                    'message': json.loads(response_json.content),
                    'session_id': session_id,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Generate random user data instead of calling external service
        user_data = generate_random_user_data(serializer.validated_data['phone_number'])

        # Create or update user in database
        user = User.from_user_information(json.loads(user_data))

        return Response(
            {
                'message': 'User created successfully',
                'customer_id': user.customer_id,
                'full_name': user.full_name,
                'email': user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class DeleteUserView(APIView):
    def delete(self, request, customer_id):
        try:
            user = User.objects.get(customer_id=customer_id)
            user.delete()
            return Response(
                {'message': 'User deleted successfully', 'customer_id': customer_id},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {'message': f'User with customer_id {customer_id} not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {'message': f'Error deleting user: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
