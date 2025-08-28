from fastapi import FastAPI
from. import models, database

app = FastAPI() #makes the app object - attach functions to it

@app.get("/") 
def root():
    return {"message": "EDM Artist Tracker API"}