# app/models/weekly_meal.py
from sqlalchemy import Column, BigInteger, DateTime, Enum, Date, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class WeeklyMeal(Base):
    __tablename__ = "weekly_meal"

    id         = Column(BigInteger, primary_key=True, index=True)
    recipe_id  = Column(BigInteger, ForeignKey("recipe.id", ondelete="CASCADE"))
    id2        = Column(BigInteger)  # 나중에 users.id FK 로 걸어도 됨
    created_at = Column(DateTime, server_default=func.now())
    meal_type  = Column(Enum("breakfast","lunch","dinner","snack"), nullable=False)
    meal_date  = Column(Date, nullable=False)
