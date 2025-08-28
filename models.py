from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey 
from sqlalchemy.orm import relationship, declarative_base #orm, treats db rows like python objects instead of raw sql

Base = declarative_base() #base case for all future models

class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer,primary_key = True,index = True)
    name = Column(String,nullable = False)
    genre = Column(String)
    instagram_name = Column(String)

    def __repr__(self):
        return f"Aritst(name = {self.name})" #helps debugging

class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key= True,index = True)
    name = Column(String,nullable = False)
    date = Column(Date)
    location = Column(String)
    organizer_id = Column(Integer,ForeignKey("organizer.id"))

class Lineup(Base):
    __tablename__ = "lineup"

    id = Column(Integer,primary_key= True,index = True)
    event_id = Column(Integer,ForeignKey("event.id"))
    artist_id = Column(Integer,ForeignKey("artist.id"))
    festival_id = Column(Integer,ForeignKey("festival.id"))

class Organizer(Base):
    __tablename__ = "organizer"

    id = Column(Integer,primary_key= True,index = True)
    name = Column(String,nullable= False)

class Festival(Base):
    __tablename__ = "festival"

    id = Column(Integer,primary_key= True,index = True)
    name = Column(String,nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String)
    organizer_id = Column(Integer,ForeignKey("organizer.id"))

class Source(Base):
    __tablename__ = "source"

    id = Column(Integer,primary_key=True,index = True)
    description = Column(String)
    