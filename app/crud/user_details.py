from sqlalchemy.orm import Session
from app.models.user_details import UserDetails

def get_user_details(db: Session, user_id: int) -> UserDetails | None:
    return db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
