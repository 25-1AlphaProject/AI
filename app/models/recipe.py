from sqlalchemy import Column, BigInteger, String, Float, Text
from app.db.base import Base

class Recipe(Base):
    __tablename__ = "recipe"

    recipe_id     = Column(BigInteger, primary_key=True, index=True)
    name          = Column(String(100))
    calories      = Column(Float)
    carbohydrates = Column(Float)
    protein       = Column(Float)
    fat           = Column(Float)
    sodium        = Column(Float)
    food_image    = Column(String(255))
    ingredient    = Column(Text)
    food_type     = Column(String(50))
    recipe_text1   = Column(Text)
    recipe_text2   = Column(Text)
    recipe_text3   = Column(Text)
    recipe_text4   = Column(Text)
    recipe_text5   = Column(Text)
    recipe_text6   = Column(Text)
    