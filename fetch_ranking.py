import requests

TEAM_ID = "307387"
COUNTRY = "Cuba"
API_URL = f"https://ctftime.org/api/v1/teams/{TEAM_ID}/"

try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        rank = data['rating']['2025']  # Datos del año 2025
        # Leer y actualizar
        readme_file = open("README.md","r+",encoding = "utf-8")
        readme_lines = readme_file.readlines()
        print(readme_lines)
        line = readme_lines.index("### WriteUps de competiciones de ciberseguridad / CTF writeups\n")
        readme_lines[line+2] = f"🇨🇺 **CTFtime {COUNTRY} Rank:** #{rank['country_place']}\n"
        readme_lines[line+4] = f"👑 **Global Rank:** #{rank['rating_place']}\n"
        readme_lines[line+6] = f"⭐ **Rating Points:** {rank['rating_points']:.2f}\n"
        readme_file.close()
        readme_file = open("README.md","w+",encoding = "utf-8")
        readme_file.writelines(readme_lines)
        readme_file.close()
    else:
        print("⚠️ Error fetching rank: API unavailable")
except Exception as e:
    print(f"⚠️ Error: {str(e)}")
