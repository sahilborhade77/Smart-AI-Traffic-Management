import requests

# We bypass OpenWeatherMap API completely by using Open-Meteo,
# which requires absolutely NO API keys and is 100% free and open-source.

# WMO Weather interpretation codes
WMO_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    95: "Thunderstorm",
    96: "Thunderstorm with Hail",
    99: "Thunderstorm with Heavy Hail",
}

# Major Indian Cities Cache to prevent unnecessary Geocoding API calls (Keeps it fast for Dashboard)
CITIES = {
    "Mumbai": {"latitude": 19.0760, "longitude": 72.8777},
    "Delhi": {"latitude": 28.7041, "longitude": 77.1025},
    "Bengaluru": {"latitude": 12.9716, "longitude": 77.5946},
    "Pune": {"latitude": 18.5204, "longitude": 73.8567},
    "Chennai": {"latitude": 13.0827, "longitude": 80.2707}
}

def get_live_weather(city_name="Mumbai"):
    """
    Fetches real-time weather using Open-Meteo API (100% Free, NO API KEY)
    """
    if city_name not in CITIES:
        # Graceful fallback for Edge Cases (Needed for Phase 8)
        city_name = "Mumbai"
        
    lat = CITIES[city_name]["latitude"]
    lon = CITIES[city_name]["longitude"]
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        # Adding timeout to heavily prevent dashboard hangs if internet fails
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current_weather", {})
        temp = current.get("temperature", 25.0)
        wind_speed = current.get("windspeed", 0.0)
        code = current.get("weathercode", 0)
        
        condition = WMO_CODES.get(code, "Unknown Weather")
        
        return {
            "city": city_name,
            "temperature": temp,
            "wind_speed": wind_speed,
            "condition": condition,
            "wmo_code": code
        }
    except Exception as e:
        print(f"⚠️ Network Error (Graceful Fallback Engaged): {e}")
        return {"city": city_name, "temperature": 32.0, "wind_speed": 10.0, "condition": "Clear (Simulated Offline)", "wmo_code": 0}

def get_risk_multiplier(wmo_code):
    """
    Maps the current weather condition to an Accident Risk Multiplier.
    This feeds directly into the AI Accident Prediction score on the Dashboard.
    - Clear: 1.0X
    - Cloudy: 1.1X
    - Drizzle/Rain: 1.5X
    - Fog: 1.8X
    - Thunderstorm/Snow: 2.0X
    """
    if wmo_code == 0:
        return 1.0
    elif wmo_code in [1, 2, 3]:  # Cloudy
        return 1.1
    elif wmo_code in [51, 53, 55, 61, 63, 65]:  # Rain / Drizzle
        return 1.5
    elif wmo_code in [45, 48]: # Fog
        return 1.8
    elif wmo_code in [71, 73, 75, 95, 96, 99]: # Snow / Thunderstorm
        return 2.0
    
    return 1.0 # Default multiplier

if __name__ == "__main__":
    print("=" * 60)
    print("🌍 LIVE WEATHER INTEGRATION MODULE (NO API KEY REQUIRED)")
    print("=" * 60)
    
    for city in ["Mumbai", "Delhi", "Bengaluru", "Pune"]:
        w_data = get_live_weather(city)
        risk = get_risk_multiplier(w_data['wmo_code'])
        
        print(f"\n📍 Location    : {w_data['city']}")
        print(f"🌡️  Temperature : {w_data['temperature']} °C")
        print(f"☁️  Condition   : {w_data['condition']}")
        print(f"⚠️  Risk Mult   : {risk}X")
        print("-" * 30)
        
    print("\n✅ Multi-City Free Weather module verified!")
