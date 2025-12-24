from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:pgadmin@localhost:5432/greencycles"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)