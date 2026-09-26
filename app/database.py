from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
