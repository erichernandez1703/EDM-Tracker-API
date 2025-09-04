from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey 
from sqlalchemy.orm import relationship, declarative_base #orm, treats db rows like python objects instead of raw sql

Base = declarative_base() #base case for all future models

class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer,primary_key = True,index = True)
    name = Column(String,nullable = False)
    genre = Column(String)
    instagram_name = Column(String)
    lineups = relationship("Lineup", back_populates="artist")
    #                      modelname           modelname                 variable attribute

    def __repr__(self):
        return f"Artist(name={self.name})" #helps debugging

class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key= True,index = True)
    name = Column(String,nullable = False)
    date = Column(Date)
    location = Column(String)
    organizer_id = Column(Integer,ForeignKey("organizer.id"))
    lineups = relationship("Lineup", back_populates="event")

class Lineup(Base):
    __tablename__ = "lineup"

    id = Column(Integer,primary_key= True,index = True)
    event_id = Column(Integer,ForeignKey("event.id"))
    artist_id = Column(Integer,ForeignKey("artist.id"))
    festival_id = Column(Integer,ForeignKey("festival.id"))
    festival = relationship("Festival", back_populates="lineups")
    artist = relationship("Artist", back_populates="lineups")
    event = relationship("Event", back_populates="lineups")

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
    lineups = relationship("Lineup", back_populates="festival") #i have many lineups
    

class Source(Base):
    __tablename__ = "source"

    id = Column(Integer,primary_key=True,index = True)
    description = Column(String)
    