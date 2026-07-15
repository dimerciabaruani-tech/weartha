# clothing_engine.py
WARM = "#F2A65A"
COOL = "#4FD1C5"
STORM = "#6C8EBF"

def get_recommendation_from_prefs(temp_c, condition, wind_speed, humidity, uv_index, user_prefs):
    """
    Returns a list of clothing items tailored to specific conditions + user preference
    """
    # Adjust temperature based on user sensitivity with more human descriptions
    adjusted_temp = temp_c
    
    # More nuanced adjustments based on user preference
    if user_prefs == "I get cold easily":
        # If they feel cold easily, adjust more aggressively
        if temp_c < 15:
            adjusted_temp = temp_c - 5  # They feel much colder
        else:
            adjusted_temp = temp_c - 3
    elif user_prefs == "I get hot easily":
        if temp_c > 25:
            adjusted_temp = temp_c + 5  # They feel much hotter
        else:
            adjusted_temp = temp_c + 3

    items = []
    cond = condition.lower()
    
    # --- Top Layers (more comprehensive) ---
    if adjusted_temp < -5:
        items.append(("heavy_coat", "Heavy Coat", COOL, "Insulated winter coat for freezing temps."))
        items.append(("sweater", "Wool Sweater", WARM, "Thermal base layer."))
        items.append(("scarf", "Warm Scarf", COOL, "Protects neck from wind chill."))
        items.append(("gloves", "Insulated Gloves", COOL, "Keep hands warm in freezing conditions."))
    elif adjusted_temp < 0:
        items.append(("heavy_coat", "Winter Coat", COOL, "Insulated coat for cold weather."))
        items.append(("sweater", "Knit Sweater", WARM, "Warm layering piece."))
        items.append(("scarf", "Scarf", COOL, "Extra neck protection."))
    elif adjusted_temp < 10:
        items.append(("coat", "Parka/Trench", COOL, "Warm outer layer."))
        items.append(("sweater", "Knit Sweater", WARM, "Layering piece."))
        if wind_speed > 10:
            items.append(("scarf", "Scarf", COOL, "Wind protection for neck."))
    elif adjusted_temp < 16:
        items.append(("jacket", "Light Jacket", COOL, "Hoodie or bomber jacket."))
        items.append(("tshirt", "Long Sleeve", WARM, "Base layer for mild weather."))
    elif adjusted_temp < 22:
        items.append(("tshirt", "Cotton T-Shirt", WARM, "Comfortable everyday wear."))
        if wind_speed > 15:
            items.append(("windbreaker", "Windbreaker", STORM, "Protects from wind."))
    elif adjusted_temp < 28:
        items.append(("tshirt", "Bamboo/Linen Tee", WARM, "Lightweight and breathable."))
        items.append(("shorts", "Light Shorts", WARM, "Keep legs cool."))
        items.append(("sunglasses", "Sunglasses", WARM, "Sun protection."))
    else:
        items.append(("tshirt", "Bamboo/Linen Tee", WARM, "Ultra-light and breathable."))
        items.append(("shorts", "Light Shorts", WARM, "Maximum ventilation."))
        items.append(("hat", "Sun Hat", WARM, "Protection from intense sun."))
        items.append(("water", "Water Bottle", COOL, "Stay hydrated in heat."))
        if uv_index and uv_index > 5:
            items.append(("sunglasses", "UV Sunglasses", WARM, "Eye protection from UV rays."))

    # --- Bottoms ---
    if adjusted_temp < 0:
        items.append(("pants", "Thermal Pants", COOL, "Insulated trousers for cold."))
        items.append(("pants", "Waterproof Pants", STORM, "Protection from snow/rain."))
    elif adjusted_temp < 10:
        items.append(("pants", "Thermal Pants", COOL, "Insulated trousers/jeans."))
    elif adjusted_temp < 22:
        items.append(("pants", "Jeans/Chinos", WARM, "Classic everyday wear."))
    else:
        items.append(("shorts", "Shorts", WARM, "Comfortable loose-fit shorts."))

    # --- Shoes ---
    if "rain" in cond or "snow" in cond or "shower" in cond:
        items.append(("boots", "Waterproof Boots", STORM, "Keep feet completely dry."))
    elif adjusted_temp < 10:
        items.append(("boots", "Thermal Boots", COOL, "Insulated footwear."))
    else:
        items.append(("sneakers", "Sneakers", WARM, "Casual wear for mild conditions."))

    # --- Accessories (Based on specific weather) ---
    if "rain" in cond or "drizzle" in cond or "shower" in cond:
        items.append(("umbrella", "Umbrella", STORM, f"{humidity}% humidity, pack it just in case."))
        items.append(("jacket", "Rain Jacket", STORM, "Waterproof outer layer."))

    # UV and Sun protection
    needs_sunglasses = bool(uv_index and uv_index > 5) or adjusted_temp > 25
    if needs_sunglasses:
        reason = f"UV index {uv_index:.0f}, protect your eyes." if uv_index and uv_index > 5 else "Strong sun, protect your eyes."
        items.append(("sunglasses", "Sunglasses", WARM, reason))
    
    if uv_index and uv_index > 5:
        items.append(("hat", "Sun Hat", WARM, "Physical sun protection."))
        if adjusted_temp > 25:
            items.append(("water", "Water Bottle", COOL, "Stay hydrated in the sun."))

    # Wind protection
    if wind_speed > 15:
        items.append(("windbreaker", "Windbreaker", STORM, f"Wind speeds of {wind_speed:.0f} mph."))
        if adjusted_temp < 15:
            items.append(("scarf", "Scarf", COOL, "Prevents heat loss from wind chill."))
        if adjusted_temp < 5:
            items.append(("gloves", "Gloves", COOL, "Protect hands from cold wind."))

    # Special temperature warnings
    if adjusted_temp > 30:
        if not any(item[0] == "water" for item in items):
            items.append(("water", "Water Bottle", COOL, "Hydration is critical in this heat."))

    # Remove duplicates while preserving order
    seen = set()
    unique_items = []
    for item in items:
        if item[0] not in seen:
            seen.add(item[0])
            unique_items.append(item)
    
    return unique_items

def get_animation_backdrop(condition):
    cond = condition.lower()
    if "rain" in cond or "drizzle" in cond or "thunderstorm" in cond:
        return "rain"
    elif "snow" in cond:
        return "snow"
    elif "cloud" in cond or "overcast" in cond or "fog" in cond or "mist" in cond:
        return "cloud"
    elif "clear" in cond:
        return "sparkle"
    else:
        return "default"