from sqlalchemy import create_engine#connects to database
from sqlalchemy.orm import sessionmaker #produces database sessions
from sqlalchemy.ext.declarative import declarative_base #defines models
from dotenv import load_dotenv #loads environment variables
import os
from models import Base

# Load environment variables from .env
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()


