from fastapi import FastAPI, HTTPException, status, Depends #injects dependencies like DB sessions, status - status codes
from . import models, database, crud, schemas
from sqlalchemy.orm import Session #each session is a task/query
from .database import SessionLocal, engine #factory that makes sessions ,powercabel connects to app from db
from typing import List
from .schemas import WeeklySchedule
from .models import Event


app = FastAPI() #makes the app object - attach functions to it

@app.get("/") 
def root():
    return {"message": "EDM Artist Tracker API"}


def get_db():
    db = SessionLocal() #creates a temp session for database
    try:
        yield db # hands off session to route function
    finally:
        db.close() #closes when finished


#get festival by name
@app.get("/festivals/{festival_name}")
def read_festival(festival_name: str, db: Session = Depends(get_db)): #depends runs function first before the outer function
    return crud.get_festival_by_name(db=db,festival_name=festival_name)


#get artists this week
@app.get("/artists/this-week",response_model= schemas.WeeklySchedule) #validates and formats response using your schemas
def get_artists_this_week(db: Session = Depends(get_db)):
    schedule_dict = crud.get_artists_this_week(db)
    return schemas.WeeklySchedule(schedule_dict) #wrapps schedule_dict(stores the crud function)


#get artist with events and/or festivals
@app.get("/artists/{artist_name}")
def read_artist(artist_name: str, db: Session = Depends(get_db)):
    return crud.get_artist_with_events_festivals(db=db,artist_name=artist_name)


@app.get("/debug/events")
def debug_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


@app.get("/enrich-artist/{artist_name}")
def enrich_artist(artist_name: str):
    metadata = crud.fetch_artist_metadata(artist_name)
    if metadata:
        return metadata
    return {"error": "Arist not found or metadata unavailable"}

