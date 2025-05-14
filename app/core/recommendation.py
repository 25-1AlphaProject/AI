import random

def calc_per_meal_cal(user):
    total = user.get("target_calories", 0)
    return total / 3 if total else 0


def recommend_one_day(user, recipes):
    """
    user: {
      "user_id": ...,
      "gender": ...,
      "age": ...,
      "weight": ...,
      "meal_count": ...,
      "target_calories": ...,
      "health_goal": ...,
      "user_diet_info": {
        "allergies": [...],
        "diseases": [...],
        "preferredMenus": [...],
        "avoidIngredients": [...],
      }
    }
    """
    def contains_any(text, keywords):
        return any(k in text for k in keywords)

    per_meal = calc_per_meal_cal(user)
    diet_info = user.get("user_diet_info", {})
    allergies = diet_info.get("allergy", [])
    preferredMenus     = diet_info.get("preferredMenus", [])
    avoidIngredients  = diet_info.get("avoidIngredients", [])
    diseases  = diet_info.get("diseases", [])

    data = []
    for r in recipes:
        data.append({
            "recipe_id": r.recipe_id,
            "name":      r.name,
            "calories":  r.calories or 0,
            "carbohydrates": r.carbohydrates or 0,
            "protein":       r.protein or 0,
            "fat":           r.fat or 0,
            "sodium":        r.sodium or 0,
            "food_type":     r.food_type or "",
            "ingredient":    r.ingredient or "",
            "score":         0
        })

    allergy_alts = {
        "해산물": ["닭고기","달걀","소고기"],
        "돼지고기": ["쇠고기","흰살생선"],
        "우유":     ["두유","멸치","해조류"],
        "계란":     ["생선","두부","콩나물"],
        "밀":       ["쌀","감자"],
        "땅콩":     ["들기름"],
        "콩":       ["김","미역","멸치"]
    }
    filtered = []
    for r in data:
        exclude = False
        for allergen in allergies:
            if allergen in r["ingredient"]:
                alts = allergy_alts.get(allergen)
                if not alts or not contains_any(r["ingredient"], alts):
                    exclude = True
        if not exclude:
            filtered.append(r)

    for r in filtered:
        for like in preferredMenus:
            if like in r["ingredient"]:
                r["score"] += 1
        for dislike in avoidIngredients:
            if dislike in r["ingredient"]:
                r["score"] -= 1

    for r in filtered:
        r["score"] -= abs(r["calories"] - per_meal) / 50

    ideal = {"carbs":0.55, "protein":0.2, "fat":0.25}
    for r in filtered:
        tot = (r["carbohydrates"]*4 + r["protein"]*4 + r["fat"]*9) or 1
        cr = (r["carbohydrates"]*4)/tot
        pr = (r["protein"]*4)/tot
        fr = (r["fat"]*9)/tot
        r["score"] += -(
            abs(cr-ideal["carbs"]) +
            abs(pr-ideal["protein"]) +
            abs(fr-ideal["fat"])
        ) * 3

    for r in filtered:
        ing = r["ingredient"]
        typ = r["food_type"]
        for d in diseases:
            if d == "hypertension" and contains_any(ing, ["간장","된장","고추장","젓갈","김치"]):
                r["score"] -= 2
            if d == "diabetes":
                if contains_any(ing, ["설탕","꿀","올리고당"]): r["score"] -= 2
                if contains_any(ing, ["잡곡","해조류","채소"]):    r["score"] += 2
            if d == "stroke":
                if contains_any(ing, ["삼겹살","갈비","유제품"]): r["score"] -= 2
                if contains_any(ing, ["참기름","들기름","올리브유","견과류","등푸른생선"]): r["score"] += 2
            if d == "reflux" and contains_any(ing, ["커피","콜라","차","우유","유제품","튀김"]):
                r["score"] -= 2
            if d == "osteoporosis" and contains_any(ing, ["우유","유제품","생선","미역","다시마","해조류"]):
                r["score"] += 2
            if d == "cancer":
                if "죽" in typ: r["score"] += 2
                if contains_any(ing, ["채소","과일","육류","생선","계란","두부","콩","우유"]):
                    r["score"] += 1
            if d == "hyperlipidemia":
                if contains_any(typ, ["튀김","전"]): r["score"] -= 2
                if contains_any(typ, ["조림","구이","찜"]): r["score"] += 2
            if d == "respiratory" and contains_any(ing, ["도라지","미역"]):
                r["score"] += 2
            if d == "liver" and contains_any(ing, ["조개","콩나물"]):
                r["score"] += 2
            if d == "stomach" and contains_any(ing, ["양배추","무"]):
                r["score"] += 2
            if d == "dementia" and contains_any(ing, ["견과류","올리브오일"]):
                r["score"] += 2

    sorted_data = sorted(filtered, key=lambda x: x["score"], reverse=True)
    top10 = sorted_data[:10] if len(sorted_data)>=10 else sorted_data

    breakfast = random.choice(top10)
    lunch     = random.choice(top10)
    dinner    = random.choice(top10)

    return {
        "breakfast": {
            "recipe_id": breakfast["recipe_id"],
            "name":       breakfast["name"],
            "calories":   breakfast["calories"],
            "ingredients": breakfast["ingredient"],
            "score":      breakfast["score"]
        },
        "lunch": {
            "recipe_id": lunch["recipe_id"],
            "name":       lunch["name"],
            "calories":   lunch["calories"],
            "ingredients": lunch["ingredient"],
            "score":      lunch["score"]
        },
        "dinner": {
            "recipe_id": dinner["recipe_id"],
            "name":       dinner["name"],
            "calories":   dinner["calories"],
            "ingredients": dinner["ingredient"],
            "score":      dinner["score"]
        }
    }
