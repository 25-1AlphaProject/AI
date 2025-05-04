# app/models/recipe.py
from sqlalchemy import Column, BigInteger, String, Float, Text
from app.db.base import Base

class Recipe(Base):
    __tablename__ = "recipe"

    id            = Column(BigInteger, primary_key=True, index=True)
    name          = Column(String(100))
    calories      = Column(Float)
    carbohydrates = Column(Float)
    protein       = Column(Float)
    fat           = Column(Float)
    sodium        = Column(Float)
    food_image    = Column(String(255))
    ingredient    = Column(Text)
    food_type     = Column(String(50))
    recipeText1   = Column(Text)
    recipeText2   = Column(Text)
    recipeText3   = Column(Text)
    recipeText4   = Column(Text)
    recipeText5   = Column(Text)
    recipeText6   = Column(Text)
    