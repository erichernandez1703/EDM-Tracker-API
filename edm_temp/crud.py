#queries the database/ retrieves data from pgadmin the way you want
from sqlalchemy.orm import Session, joinedload #eager loading relationships - 
from fastapi import HTTPException #raises status codes incase of error
from .models import Artist, Event, Festival, Source, Lineup
from datetime import date, timedelta #date is timestamp, timedelta is distance between timestamps
from sqlalchemy import or_, and_
from collections import defaultdict
import requests

def get_festival_by_name(db: Session, festival_name: str):
    festival = db.query(Festival).options(joinedload(Festival.lineups).joinedload(Lineup.artist)).filter(Festival.name == festival_name).first()

    if not festival:
        raise HTTPException(status_code = 404, detail ="Festival not found")
    
    return {
        "name": festival.name,
        "location":festival.location,
        "start_date": festival.start_date,
        "end_date": festival.end_date,
        "organizer_id": festival.organizer_id,
        "artists": [
            {
                "name": lineup.artist.name,
                "genre": lineup.artist.genre
            }
            for lineup in festival.lineups if lineup.artist
        ]
    }



def get_artist_with_events_festivals(db: Session, artist_name: str):
    artist = db.query(Artist).options(joinedload(Artist.lineups).joinedload(Lineup.event),
        joinedload(Artist.lineups).joinedload(Lineup.festival)).filter(Artist.name == artist_name).first()

    if not artist:
        raise HTTPException(status_code=404, detail = "Artist Not Found")
    
    return {
        "artist":{
        "name": artist.name,
        "genre": artist.genre,
        "instagram_name": artist.instagram_name,
        },
        "festivals": [
            {
                "name":lu.festival.name,
                "location": lu.festival.location,
                "dates": f"{lu.festival.start_date} to {lu.festival.end_date}"
            }
            for lu in artist.lineups if lu.festival
        ],
        "events":[
            {
                "name": lu.event.name,
                "location": lu.event.location,
                "date": str(lu.event.date)
            }
            for lu in artist.lineups if lu.event
        ]
    }


def get_artists_this_week(db: Session):
    today = date.today()
    end_of_week = today + timedelta(days=6)

    print("today:", today)
    print("end of week:", end_of_week)

    lineups = db.query(Lineup).options(joinedload(Lineup.artist),joinedload(Lineup.festival),joinedload(Lineup.event)
    ).filter(
        or_( #or event or festival
            and_( #and if event exists and it has is this week
                Lineup.event != None,
                Lineup.event.has(
                    and_(
                        Event.date >= today - timedelta(days=30),
                        Event.date <= today + timedelta(days=30),
                    )
                )
            ),
            and_(
                Lineup.festival != None,
                Lineup.festival.has(
                    and_(
                        Festival.start_date >= today - timedelta(days=30),
                        Festival.end_date <= today + timedelta(days=30),
                    )
                )
            )
        )
    ).all()

    if not lineups:
        raise HTTPException(status_code = 404, detail = "No artists scheduled this week")

    schedule = defaultdict(list)
#for each lineup
    for lineup in lineups:
        artist = lineup.artist
        if artist is None:
            continue
            #extract artist
        if lineup.event:
            performance_date = lineup.event.date
        elif lineup.festival:
            performance_date = lineup.festival.start_date
        else:
            continue
            #convert date to weekday
        weekday = performance_date.strftime('%A')
        #add artist to weekday group
        schedule[weekday].append({
            "name":artist.name,
            "date": performance_date.isoformat()
        })
    return dict(schedule)




def fetch_artist_metadata(artist_name: str) -> dict:
    url = "https://www.theaudiodb.com/api/v1/json/123/search.php"
    response = requests.get(url, params = {"s": artist_name})
    if response.status_code == 200:
        data = response.json()
        artist = data.get("artists")
        if artist:
            raw = artist[0]
            return {
                "name": raw.get("strArtist"),
                "genre": raw.get("strGenre"),
                "bio": raw.get("strBiographyEN"),
                "image_url": raw.get("strArtistThumb"),
            }
        return None
