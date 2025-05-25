from sqlalchemy import Column, BigInteger, DateTime, Enum as SQLEnum, Date, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
from enum import Enum as PyEnum

class MealType(PyEnum):
    BREAKFAST = "BREAKFAST"
    LUNCH     = "LUNCH"
    DINNER    = "DINNER"
    SNACK     = "SNACK"

class WeeklyMeal(Base):
    __tablename__ = "weekly_meal"

    meal_id    = Column(BigInteger, primary_key=True, index=True)
    recipe_id  = Column(BigInteger, ForeignKey("recipe.recipe_id", ondelete="CASCADE"))
    user_id    = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    meal_type  = Column(
        SQLEnum(MealType, name="meal_type_enum"),  # native_enum=True 가 기본
        nullable=False
    )
    meal_date  = Column(Date, nullable=False)
