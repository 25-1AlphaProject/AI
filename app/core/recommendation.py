import pandas as pd
import random
from datetime import datetime

df = pd.read_excel(
    "data.xls",   
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
    per_meal = calc_per_meal_cal(user)
    d = df.copy()
    d["ingredient"] = d["ingredient"].fillna("").astype(str)
    
    allergy_alternatives = {
        "해산물": ["닭고기", "달걀", "소고기"],
        "돼지고기": ["쇠고기", "흰살생선"],
        "우유": ["두유", "멸치", "해조류"],
        "계란": ["생선", "두부", "콩나물"],
        "밀": ["쌀", "감자"],
        "땅콩": ["들기름"],
        "콩": ["김", "미역", "멸치"]
    }

    for allergen in user["allergy"]:
        allergen_mask = d["ingredient"].str.contains(allergen)
        
        if allergen in allergy_alternatives:
            alt_masks = [d["ingredient"].str.contains(alt) for alt in allergy_alternatives[allergen]]
            alternative_mask = alt_masks[0]
            for m in alt_masks[1:]:
                alternative_mask |= m
            
            d.loc[allergen_mask & alternative_mask, "score"] = d.get("score", 0) + 2
            d = d[~(allergen_mask & ~alternative_mask)]
        
        else:
            d = d[~allergen_mask]
    
    d["score"] = d.get("score", 0)  
    
    for like in user["likes"]:
        d.loc[d["ingredient"].str.contains(like), "score"] += 1
    for dislike in user["dislikes"]:
        d.loc[d["ingredient"].str.contains(dislike), "score"] -= 1

    d["calorie_diff"] = (d["calories"] - per_meal).abs()
    d["score"] -= d["calorie_diff"] / 50  

    ideal_ratio = {"carbs": 0.55, "protein": 0.2, "fat": 0.25}

    d["carbs_ratio"] = (d["carbohydrates"] * 4) / (d["calories"] + 1e-6)
    d["protein_ratio"] = (d["protein"] * 4) / (d["calories"] + 1e-6)
    d["fat_ratio"] = (d["fat"] * 9) / (d["calories"] + 1e-6)

    d["nutrition_score"] = -(
        abs(d["carbs_ratio"] - ideal_ratio["carbs"]) +
        abs(d["protein_ratio"] - ideal_ratio["protein"]) +
        abs(d["fat_ratio"] - ideal_ratio["fat"])
    )
    d["score"] += d["nutrition_score"] * 3

    for disease in user["diseases"]:
        if disease == "hypertension":
            d.loc[d["ingredient"].str.contains("간장|된장|고추장|젓갈|김치"), "score"] -= 2

        if disease == "diabetes":
            d.loc[d["ingredient"].str.contains("설탕|꿀|올리고당"), "score"] -= 2
            d.loc[d["ingredient"].str.contains("잡곡|해조류|채소"), "score"] += 2

        if disease == "stroke":
            d.loc[d["ingredient"].str.contains("삼겹살|갈비|유제품"), "score"] -= 2
            d.loc[d["ingredient"].str.contains("참기름|들기름|올리브유|견과류|등푸른생선"), "score"] += 2

        if disease == "reflux":
            d.loc[d["ingredient"].str.contains("커피|콜라|차|우유|유제품|튀김"), "score"] -= 2

        if disease == "osteoporosis":
            d.loc[d["ingredient"].str.contains("우유|유제품|생선|미역|다시마|해조류"), "score"] += 2

        if disease == "cancer":
            d.loc[d["food_type"].str.contains("죽"), "score"] += 2
            d.loc[d["ingredient"].str.contains("채소|과일|육류|생선|계란|두부|콩|우유"), "score"] += 1

        if disease == "hyperlipidemia":
            d.loc[d["food_type"].str.contains("튀김|전"), "score"] -= 2
            d.loc[d["food_type"].str.contains("조림|구이|찜"), "score"] += 2

        if disease == "respiratory":
            d.loc[d["ingredient"].str.contains("도라지|미역"), "score"] += 2

        if disease == "liver":
            d.loc[d["ingredient"].str.contains("조개|콩나물"), "score"] += 2

        if disease == "stomach":
            d.loc[d["ingredient"].str.contains("양배추|무"), "score"] += 2

        if disease == "dementia":
            d.loc[d["ingredient"].str.contains("견과류|올리브오일"), "score"] += 2

    d = d.sort_values(by=["score"], ascending=False)

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
