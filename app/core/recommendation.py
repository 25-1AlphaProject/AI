import pandas as pd
import random
from datetime import datetime

df = pd.read_excel(
    "recipe_data (1).xls",
    engine="xlrd"
)

df = df.rename(columns={
    "메뉴명": "name",
    "요리종류": "food_type",
    "열량(kcal)": "calories",
    "탄수화물(g)": "carbohydrates",
    "단백질(g)": "protein",
    "지방(g)": "fat",
    "나트륨": "sodium",
    "이미지경로": "food_image",
    "재료정보": "ingredient"
})

def calc_per_meal_cal(user):
    if user["desired_per_meal_cal"] is not None:
        return user["desired_per_meal_cal"]
    
    w = user["weight"]
    factor = {
        "none": (25 + 30) / 2,     
        "moderate": (30 + 35) / 2, 
        "high": (35 + 40) / 2      
    }[user["activity_level"]]
    
    daily = w * factor
    if user["pregnant"]:
        daily += 400
    return daily / 3

def recommend_one_day(user):
    """사용자 정보를 받아서 하루 식단 추천"""
    per_meal = calc_per_meal_cal(user)
    d = df.copy()
    d["ingredient"] = d["ingredient"].fillna("").astype(str)
    
    for allergen in user["allergy"]:
        d = d[~d["ingredient"].str.contains(allergen)]
    
    if "hypertension" in user["diseases"]:
        d = d[d["sodium"] <= 500]
    
    d["score"] = 0
    for like in user["likes"]:
        d.loc[d["ingredient"].str.contains(like), "score"] += 1
    for dislike in user["dislikes"]:
        d.loc[d["ingredient"].str.contains(dislike), "score"] -= 1
    
    d["calorie_diff"] = (d["calories"] - per_meal).abs()
    d = d.sort_values(by=["score", "calorie_diff"], ascending=[False, True])

    breakfast = d.sample(n=1)
    lunch = d.sample(n=1)
    dinner = d.sample(n=1)

    return {
        "breakfast": {
            "name": breakfast.iloc[0]["name"],
            "calories": breakfast.iloc[0]["calories"],
            "ingredients": breakfast.iloc[0]["ingredient"]
        },
        "lunch": {
            "name": lunch.iloc[0]["name"],
            "calories": lunch.iloc[0]["calories"],
            "ingredients": lunch.iloc[0]["ingredient"]
        },
        "dinner": {
            "name": dinner.iloc[0]["name"],
            "calories": dinner.iloc[0]["calories"],
            "ingredients": dinner.iloc[0]["ingredient"]
        }
    }
