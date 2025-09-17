from pydantic import BaseModel, RootModel  #pydantic valdates data in the correct format you wish
from datetime import date
from typing import List, Dict


class ArtistSchema(BaseModel):
    name: str
    genre: str | None = None #can be a string or None, if not provided default is None
    instagram_name: str | None = None

class Artist(ArtistSchema): #get class for user retrieving data and int comes to the user
    id: int

    class Config: #specific config for special scenarios
        orm_mode = True #reads data directly from sqlalchemy objects
        extra = "forbid"




class OrganizerSchema(BaseModel):
    name: str

class Organizer(OrganizerSchema):
    id: int

    class Config:
        orm_mode = True
        extra = "forbid"




class EventSchema(BaseModel):
    name: str
    date: date
    location: str | None = None
    organizer: OrganizerSchema

class Event(EventSchema):
    id: int

    class Config:
        orm_mode = True
        extra = "forbid"





class FestivalSchema(BaseModel):
    name: str
    start_date: date
    end_date: date
    location: str
    organizer: OrganizerSchema

class Festival(FestivalSchema):
    id: int

    class Config:
        orm_mode = True
        extra = "forbid"




class LineupSchema(BaseModel):
    event: EventSchema | None = None
    artist: ArtistSchema
    festival: FestivalSchema | None = None

class Lineup(LineupSchema):
    id: int

    class Config:
        orm_mode = True
        extra = "forbid"




class SourceSchema(BaseModel):
    description: str
    event: EventSchema | None = None
    festival: FestivalSchema | None = None

class Source(SourceSchema):
    id: int

    class Config:
        orm_mode = True
        extra = "forbid"

#this is used inside a list
class ArtistSchedule(BaseModel): #defines shape of a single artist's appearance
    name: str
    date: str
#wrapper schemas for week's schedule
class WeeklySchedule(RootModel[Dict[str,List[ArtistSchedule]]]): #rootmodel, defines a schemas for a non-object root, like dict or list
    pass