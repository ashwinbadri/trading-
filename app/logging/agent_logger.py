from datetime import datetime

from app.memory.agent_log_repository import AgentLogRepository


class AgentLogger:

    def __init__(self):
        self.repository = AgentLogRepository()

    def log(self, message: str):
        timestamp = datetime.now().isoformat()
        formatted_message = f"[{timestamp}] {message}"

        print(formatted_message)

        self.repository.save_log(message)