import sys
from user.shell import Shell
from core.api import create_shell_engine, eval_command

if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    if args_num > 2:
        raise ValueError("wrong number of command line arguments")
    elif args_num == 2:
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        engine = create_shell_engine()
        eval_command(engine, sys.argv[2])
    elif args_num == 1:
        if sys.argv[1] != "-e":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        shell = Shell(exit_flag=False)
        shell.run()
    else:
        shell = Shell()
        shell.run()
