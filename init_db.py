from app.memory.database import engine, Base
from app.memory import db_models


Base.metadata.create_all(bind=engine)

print("Database tables created")