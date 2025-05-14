from sqlalchemy import Column, Integer, Enum, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class UserDetails(Base):
    __tablename__ = "user_details"

    id                = Column(Integer, primary_key=True, index=True)
    user_id           = Column(Integer, unique=True, nullable=False)  # 외부 서비스 유저 ID
    gender            = Column(Enum("M","F", name="gender"), nullable=False)
    age               = Column(Integer, nullable=False)
    height            = Column(Float, nullable=True)
    weight            = Column(Float, nullable=False)
    meal_count        = Column(Enum("BREAKFAST","LUNCH","DINNER", name="meal_count"), nullable=False)
    target_calories   = Column(Integer, nullable=False)
    user_diet_info    = Column(JSON, nullable=True)  
    created_at        = Column(DateTime(timezone=True), server_default=func.now())
    health_goal       = Column(Enum("DIET","DISEASE_MANAGEMENT","HABIT_IMPROVEMENT","NOT_SURE", name="health_goal"), nullable=False)  # 건강 목표