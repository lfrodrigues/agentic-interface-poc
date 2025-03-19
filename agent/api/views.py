from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from agno2.agent import start_agent
from agno2.interface import start_agent_jsx, start_agent_json
from .serializers import MessageInputSerializer
import uuid
from textwrap import dedent
import json

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
                print("*******  JSON")
                print(response_json.get_content_as_string())

                return Response({'message': json.loads(response_json.content), 'session_id': session_id}, status=status.HTTP_200_OK)

            agent = start_agent(session_id)

            # response = agent.print_response(message_text)
            response = agent.run(message_text)
            print("*******  AGENT")
            print(response.get_content_as_string())

            agent_jsx = start_agent_jsx()
            response_jsx = agent_jsx.run(response.content)
            print("*******  JSX")
            print(response_jsx.get_content_as_string())

            agent_json = start_agent_json()
            response_json = agent_json.run(response_jsx.content)
            print("*******  JSON")
            print(response_json.get_content_as_string())
            
            
            return Response({'message': json.loads(response_json.content), 'session_id': session_id}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# {
#     "message": " I want to pay my invoices",
#     "session_id": "NEW"
# }


# {
#     "message": " I want to pay my invoices",
#     "session_id": "session_2"
# }


# {
#     "message": " +123456543",
#     "session_id": "session_2"
# }