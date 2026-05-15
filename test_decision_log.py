from app.memory.database import initialize_database
from app.memory.decision_log_repository import DecisionLogRepository


initialize_database()

repository = DecisionLogRepository()

for decision in repository.get_all_decisions()[:5]:
    print(decision.symbol, decision.final_action, decision.timestamp)
