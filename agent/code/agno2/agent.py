from langtrace_python_sdk import langtrace  # Must precede other imports

from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.aws import AwsBedrock
from .tools import (
    get_outstanding_invoices,
    get_user_information,
    add_card,
    get_available_cards,
    make_payment,
    validate_phone_number,
    get_available_packages,
    activate_package,
)
from agno.storage.agent.sqlite import SqliteAgentStorage
from textwrap import dedent
from agno.models.openai import OpenAIChat
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.pgvector import PgVector
import readline
import os
import atexit

load_dotenv()

def start_console_tools():
    # Configure readline history
    histfile = os.path.join("tmp", ".agno_history")
    try:
        readline.read_history_file(histfile)
        # Default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    # Register the save history function to be called on exit
    atexit.register(readline.write_history_file, histfile)

    # Configure readline behavior
    readline.parse_and_bind("tab: complete")  # Enable tab completion
    readline.parse_and_bind("set editing-mode emacs")  # Use emacs-style editing
    readline.parse_and_bind("Control-a: beginning-of-line")  # Ctrl+a to beginning of line
    readline.parse_and_bind("Control-e: end-of-line")  # Ctrl+e to end of line
    readline.parse_and_bind("Control-l: clear-screen")  # Ctrl+l to clear screen
    readline.parse_and_bind("Control-k: kill-line")  # Ctrl+k to delete to end of line
    readline.parse_and_bind(
        "Control-u: unix-line-discard"
    )  # Ctrl+u to delete to beginning of line


# langtrace.init()

knowledge_base = TextKnowledgeBase(
    path="data/txt_files",
    # Table name: ai.text_documents
    vector_db=PgVector(
        table_name="text_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
)

# Create a storage backend using the Sqlite database
storage = SqliteAgentStorage(table_name="agent_sessions", db_file="tmp/data.db")


def start_agent(session_id=None):

    agent = Agent(
        # model=AwsBedrock(id="us.anthropic.claude-3-7-sonnet-20250219-v1:0", temperature=0), 
        session_id=session_id,
        model=OpenAIChat(id="gpt-4o-mini", temperature=0),
        description=dedent("""
            You are a helpful assistant.
            The first tool you need to call is search_knowledge_base.
            You can only help with questions related to the knowledge base and you can only use the tools provided to you.
            DO NOT reply to anything that is not related to the knowledge base.
            Never explain the process you need to follow to execute the user's request.
            When you conclude a process print the message: FINISHED_PROCESS
        """),
        instructions=dedent("""
            Execution:
            1. Search for the process to answer the user\'s question in the knowledge base.
            2. If the process is not found, ask the user to provide more information.
            3. If the process is found, use the tools to answer the user\'s question.
            4. If there's a default action that is needed from the user add it inside <default_action> tags.
            5. if there are necessary fields that are needed from the user add them inside <necessary_fields> tags.
        """),
        add_history_to_messages=True,
        num_history_responses=15,
        tools=[
            get_outstanding_invoices,
            get_user_information,
            add_card,
            get_available_cards,
            make_payment,
            validate_phone_number,
            get_available_packages,
            activate_package,
        ],
        show_tool_calls=True,
        markdown=True,
        storage=storage,
        knowledge=knowledge_base,
        search_knowledge=True,
        # debug_mode=True
    )

    return agent

# agent.knowledge.load(recreate=True)

if __name__ == "__main__":
    start_console_tools()
    agent = start_agent()
    try:
        # agent.print_response("What is my credit?", stream=True)
        # agent.print_response("what is my credit?", stream=True)

        print("Interactive Agent is ready! Type 'exit' to end the conversation.")
        print("You can copy-paste multi-line text directly into the prompt.")

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            # response = agent.print_response(user_input, stream=True)
            response = agent.print_response(user_input)
            print(f"Agent: {response}")

    except Exception as e:
        print(f"Error: {str(e)}")
