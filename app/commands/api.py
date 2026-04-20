from app.session import Session
from app.commands.core import get_command_data


def execute_command(command: str, session: Session) -> dict:
    result = get_command_data(command, session)

    if result is None:
        return {
            "command": command,
            "error": "Unknown command",
        }

    return result