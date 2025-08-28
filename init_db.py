from database import engine  # adjust if your path is different
from models import Base

Base.metadata.create_all(bind=engine)
