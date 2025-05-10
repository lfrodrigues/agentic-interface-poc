import json
import uuid
from textwrap import dedent

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from agno2.agent_interface import start_agent_json, start_agent_jsx
from agno2.agent_main import start_agent
from agno2.models import User
from agno2.utils import create_user
from api.serializers import MessageInputSerializer, UserCreateSerializer, UserListSerializer


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

        # Create or update user in database
        user = create_user(serializer.validated_data['phone_number'])

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

            # Delete all associated invoices first
            user.invoices.all().delete()

            # Delete the user
            user.delete()

            # Delete the billing address since it's not needed
            billing_address = user.billing_address
            billing_address.delete()

            return Response(
                {
                    'message': 'User and associated data deleted successfully',
                    'customer_id': customer_id,
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {'message': f'User with customer_id {customer_id} not found'},
                status=status.HTTP_404_NOT_FOUND,
            )


class ListUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
