from dataclasses import dataclass


@dataclass
class CLIArgs:
    """
    Dataclass to store CLI arguments
    """

    url: str
    output_dir: str
    selector: str

    concurrency: int = 1
    count: int | None = None
    verbose: bool = False
    ai_naming: bool = True


args: CLIArgs = CLIArgs("", "", "")


def set_args(cli_args: CLIArgs) -> CLIArgs:
    """
    Function to set CLI arguments
    """

    global args
    args = cli_args

    # print("CLI arguments set", args)

    return args


def get_args() -> CLIArgs:
    """
    Function to get CLI arguments
    """

    # print("CLI arguments get", args)

    return args
