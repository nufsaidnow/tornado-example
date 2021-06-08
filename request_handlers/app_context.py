from enum import Enum
from fabric import Connection


class Target:
    def __init__(self, host, user, port):
        self.host = host
        self.user = user
        self.port = port

    def get_connection(self):
        return Connection(
            host=self.host,
            user=self.user,
            port=self.port,
        )


class ApplicationState(str, Enum):
    WAITING_FOR_COMMAND = "WAITING_FOR_COMMAND",
    EXECUTING = "EXECUTING"


class AppContext:
    def __init__(self):
        self.current_command = None
        self.state = ApplicationState.WAITING_FOR_COMMAND
        self.error = None

    def to_json(self):
        current_command = None
        if self.current_command:
            current_command = {
                "name": self.current_command.name,
                "output": self.current_command.output,
                "target": self.current_command.target.host,
            }
        return {
            "state": self.state,
            # "error": self.error,
            "current_command": current_command,
        }


class Command:
    def __init__(self, name, script, target):
        self.name = name
        self.script = script
        self.output = ""
        self.target = target
