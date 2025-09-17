from datetime import date
from database import SessionLocal
import models

def seed():
    db = SessionLocal()

    try:
        festival = models.Festival(
            name="Coachella",
            location = "California",
            start_date = date(2025, 9, 10),
            end_date = date (2025, 9, 12),
        ) 
        db.add(festival)
        db.commit()
        db.refresh(festival)

        artist = models.Artist(
            name="Beltran",
            performance_date = date(2025,9,11),
        )
        db.add(artist)
        db.commit()
        db.refresh(artist)

        event = models.Event(
            name="Sunset Jam",
            date = date(2025,9,11),
        )

        db.add(event)
        db.commit()

    except Exception as e:
        db.rollback() #reverts changes if error occurs
        print(f"error: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    seed()