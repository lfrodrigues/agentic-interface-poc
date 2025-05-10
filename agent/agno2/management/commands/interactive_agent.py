import atexit
import os
import readline
from django.core.management.base import BaseCommand
from agno2.agent_main import start_agent
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace  # Must precede other imports

load_dotenv()


class Command(BaseCommand):
    help = 'Starts an interactive session with the agent'

    def configure_console_tools(self):
        # Configure readline history
        histfile = os.path.join('/tmp', '.agno_history')
        try:
            readline.read_history_file(histfile)
            # Default history len is -1 (infinite), which may grow unruly
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass

        # Register the save history function to be called on exit
        atexit.register(readline.write_history_file, histfile)

        # Configure readline behavior
        readline.parse_and_bind('tab: complete')  # Enable tab completion
        readline.parse_and_bind('set editing-mode emacs')  # Use emacs-style editing
        readline.parse_and_bind('Control-a: beginning-of-line')  # Ctrl+a to beginning of line
        readline.parse_and_bind('Control-e: end-of-line')  # Ctrl+e to end of line
        readline.parse_and_bind('Control-l: clear-screen')  # Ctrl+l to clear screen
        readline.parse_and_bind('Control-k: kill-line')  # Ctrl+k to delete to end of line
        readline.parse_and_bind('Control-u: unix-line-discard')  # Ctrl+u to delete to beginning of line

    def handle(self, *args, **options):
        self.configure_console_tools()
        agent = start_agent()

        try:
            self.stdout.write(self.style.SUCCESS("Interactive Agent is ready! Type 'exit' to end the conversation."))
            self.stdout.write('You can copy-paste multi-line text directly into the prompt.')

            while True:
                user_input = input('You: ')
                if user_input.lower() == 'exit':
                    break
                response = agent.print_response(user_input)
                self.stdout.write(f'Agent: {response}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 