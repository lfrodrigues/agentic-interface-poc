from dotenv import load_dotenv
from agno.agent import Agent
from textwrap import dedent
from agno.models.openai import OpenAIChat

load_dotenv()

def start_agent_jsx(session_id=None):

    agent = Agent(
        # model=AwsBedrock(id="anthropic.claude-3-haiku-20240307-v1:0", temperature=0),
        model=OpenAIChat(id="gpt-4o-mini", temperature=0),
        description=dedent("""
            You are a helpful assistant that converts text to a nice looking React Native JSX interface.
        """),
        instructions=dedent("""
            1. Never include any explanation
            2. Never include any javascript code, only JSX
            3. Dont include ```jsx``` tags
            4. Always include the context text that is provided to you
            5. Use only react native components
            6. Fields inside necessary_fields are TextInput
            7. If you need to add a submit button, use the handleSubmit function
            8. Always include a prop called name when the widget is a TextInput
            9. Always include onChangeText in TextInput, use the function "storeData"
        """),
        # debug_mode=True
    )
    return agent 

def start_agent_json(session_id=None):

    agent = Agent(
        # model=AwsBedrock(id="anthropic.claude-3-haiku-20240307-v1:0", temperature=0),
        model=OpenAIChat(id="gpt-4o-mini", temperature=0),
        description=dedent("""
            You are a helpful assistant that converts JSX to a JSON object.
        """),
        instructions=dedent("""
            JSX Example 1:
            <View style={{ padding: 10, backgroundColor: "#f0f0f0", borderRadius: 8 }}>
                <Text type="subtitle" style={{ marginBottom: 10 }}>
                    Dynamic UI from JKAJHJAHSHJSH
                </Text>
                <Button title="Refresh Data" onPress={handleSubmit} />
                <View style={{ marginTop: 15 }}>
                    <Text>This entire UI was rendered from a JSON response!</Text>
                </View>
            </View>

            JSON Example 1:
            {
                "type": "View",
                "props": {
                "style": { "padding": 10, "backgroundColor": "#f0f0f0", "borderRadius": 8 }
                },
                "children": [
                {
                    "type": "Text",
                    "props": {
                    "type": "subtitle",
                    "style": { "marginBottom": 10 }
                    },
                    "children": "Dynamic UI from JKAJHJAHSHJSH"
                },
                {
                    "type": "Button",
                    "props": {
                    "title": "Refresh Data",
                    "onPress": "handleSubmit"
                    }
                },
                {
                    "type": "View",
                    "props": {
                    "style": { "marginTop": 15 }
                    },
                    "children": [
                    {
                        "type": "Text",
                        "children": "This entire UI was rendered from a JSON response!"
                    }
                    ]
                }
                ]
            }
                            
            JSX Example 2:
            <View
                style={{
                padding: 16,
                backgroundColor: "#fff",
                borderRadius: 8,
                shadowColor: "#000",
                shadowOffset: { width: 0, height: 2 },
                shadowOpacity: 0.2,
                shadowRadius: 4,
                elevation: 5
                }}
            >
                <Text
                style={{
                    fontSize: 16,
                    marginBottom: 8
                }}
                >
                Email Address
                </Text>
                <TextInput
                name="email"
                style={{
                    height: 40,
                    borderColor: "#ccc",
                    borderWidth: 1,
                    borderRadius: 4,
                    paddingHorizontal: 10,
                    marginBottom: 12
                }}
                onChangeText={storeData}
                keyboardType="email-address"
                autoCapitalize="none"
                />
                <Text
                style={{
                    fontSize: 16,
                    marginBottom: 8
                }}
                >
                Password
                </Text>
                <TextInput
                name="password"
                style={{
                    height: 40,
                    borderColor: "#ccc",
                    borderWidth: 1,
                    borderRadius: 4,
                    paddingHorizontal: 10,
                    marginBottom: 12
                }}
                onChangeText={storeData}
                secureTextEntry={true}
                />
                <Button title="Submit" onPress={handleSubmit} />
            </View>



            JSON Example 2:
            {
                "type": "View",
                "props": {
                "style": {
                    "padding": 16,
                    "backgroundColor": "#fff",
                    "borderRadius": 8,
                    "shadowColor": "#000",
                    "shadowOffset": { "width": 0, "height": 2 },
                    "shadowOpacity": 0.2,
                    "shadowRadius": 4,
                    "elevation": 5
                }
                },
                "children": [
                {
                    "type": "Text",
                    "props": {
                    "style": {
                        "fontSize": 16,
                        "marginBottom": 8
                    }
                    },
                    "children": "Email Address"
                },
                {
                    "type": "TextInput",
                    "props": {
                    "name": "email",
                    "style": {
                        "height": 40,
                        "borderColor": "#ccc",
                        "borderWidth": 1,
                        "borderRadius": 4,
                        "paddingHorizontal": 10,
                        "marginBottom": 12
                    },
                    "onChangeText": "storeData",
                    "keyboardType": "email-address",
                    "autoCapitalize": "none"
                    }
                },
                {
                    "type": "Text",
                    "props": {
                    "style": {
                        "fontSize": 16,
                        "marginBottom": 8
                    }
                    },
                    "children": "Password"
                },
                {
                    "type": "TextInput",
                    "props": {
                    "name": "password",
                    "style": {
                        "height": 40,
                        "borderColor": "#ccc",
                        "borderWidth": 1,
                        "borderRadius": 4,
                        "paddingHorizontal": 10,
                        "marginBottom": 12
                    },
                    "onChangeText": "storeData",
                    "secureTextEntry": true
                    }
                },
                {
                    "type": "Button",
                    "props": {
                    "title": "Submit",
                    "onPress": "handleSubmit"
                    }
                }
                ]
            }
        """),
        # debug_mode=True
    )
    return agent 

if __name__ == "__main__":
    try:
        agent_jsx = start_agent_jsx()
        input = dedent("""
┃ Your payment has been successfully processed! Here are the details:                                                                                                                  ┃
┃                                                                                                                                                                                      ┃
┃  • Transaction ID: TXN-894D0BB6                                                                                                                                                      ┃
┃  • Invoice Status: Paid                                                                                                                                                              ┃
┃                                                                                                                                                                                      ┃
┃ Additionally, your card has been added successfully:                                                                                                                                 ┃
┃                                                                                                                                                                                      ┃
┃  • Card Number: 1234565432345                                                                                                                                                        ┃
┃  • Expiration Date: 12/2028                                                                                                                                                          ┃
┃                                                                                                                                                                                      ┃
┃ If you need any further assistance, feel free to ask!                                                                                                                                ┃
┃                                                            
        """)
        agent_jsx.print_response(input, stream=True)

    except Exception as e:
        print(f"Error: {str(e)}")
