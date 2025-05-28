from core.api import create_shell_engine, eval_command
from user.prompt import create_prompt


class Shell:
    """
    Shell class to handle command line interface.
    """
    def __init__(self, **kwargs):
        self.engine = create_shell_engine(**kwargs)

    def run(self):
        """
        Run the shell command line interface.
        """
        try:
            while True:
                cmdline = create_prompt(self.engine)
                if cmdline.strip():
                    eval_command(self.engine, cmdline)

        except EOFError:
            print("\nExiting shell...")
        except KeyboardInterrupt:
            print("\nExiting shell...")
