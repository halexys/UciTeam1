import requests

TEAM_ID = "307387"  # CTFtime Team ID
API_URL = f"https://ctftime.org/api/v1/teams/{TEAM_ID}/"

try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        rank = data['rating']['2025']  # Datos del año 2025
        
        print(f"🇨🇺 **CTFtime Cuba Rank:** #{rank['country_place']}")
        print(f"👑 **Global Rank:** #{rank['rating_place']}")
        print(f"⭐ **Rating Points:** {rank['rating_points']:.2f}")
    else:
        print("⚠️ Error fetching rank: API unavailable")
except Exception as e:
    print(f"⚠️ Error: {str(e)}")
