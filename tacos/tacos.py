# Full Python script that queries Google Places API for "Tacos" in 225 grid squares (15x15)
# and saves the results into tacos_CDMX.csv with rate limiting

import json
import requests
import csv
import time
from llave import GOOGLE_MAPS_API_KEY

apiKey = GOOGLE_MAPS_API_KEY
print(f"Using API key: {apiKey[:4]}***")

# Step 1: Definimos el area de la Ciudad de México
lat_min, lng_min = 19.29099, -99.224607  # Southwest corner
lat_max, lng_max = 19.521517, -99.036189  # Northeast corner

# Step 2: Dividimos el area en una cuadrícula de 15x15
grid_size = 15
lat_step = (lat_max - lat_min) / grid_size
lng_step = (lng_max - lng_min) / grid_size

# Step 3:  Pereparamos los headers para la solicitud de la API
headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": apiKey,
    "X-Goog-FieldMask": "places.displayName,places.generativeSummary,places.formattedAddress,places.priceLevel,places.priceRange,places.rating,places.userRatingCount,places.location,places.websiteUri"
}

tacos_CDMX = []

# Step 4: for para cada celda de la cuadrícula, hacemos una solicitud a la API
for i in range(grid_size):
    for j in range(grid_size):
        sw_lat = lat_min + i * lat_step
        sw_lng = lng_min + j * lng_step
        ne_lat = sw_lat + lat_step
        ne_lng = sw_lng + lng_step

        payload = {
            "textQuery": "Tacos",
            "locationRestriction": {
                "rectangle": {
                    "low": {
                        "latitude": round(sw_lat, 6),
                        "longitude": round(sw_lng, 6)
                    },
                    "high": {
                        "latitude": round(ne_lat, 6),
                        "longitude": round(ne_lng, 6)
                    }
                }
            }
        }

        response = requests.post(
            "https://places.googleapis.com/v1/places:searchText",
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200: 
            # Parse the JSON response
            data = response.json()
            for place in data.get("places", []):
                # Con un for creamos una lista con los datos que queremos
                tacos_CDMX.append({
                    "name": place.get("displayName", {}).get("text"),
                    "address": place.get("formattedAddress"),
                    "lat": place.get("location", {}).get("latitude"),
                    "lng": place.get("location", {}).get("longitude"),
                    "rating": place.get("rating"),
                    "userRatingCount": place.get("userRatingCount"),
                    "priceLevel": place.get("priceLevel"),
                    "website": place.get("generativeSummary"),
                    "genAI": place.get("websiteUri")
                })
        else:
            print(f"❌ Error in cell ({i}, {j}): {response.status_code} - {response.text}")

        # ⏱️ Add delay to respect 10 requests per second limit
        time.sleep(0.4)
        print(f"✅ Processed cell ({i}, {j}) - {len(tacos_CDMX)} places found so far.")

# Step 5: Export results to CSV
if tacos_CDMX:
    with open("tacos_CDMX.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tacos_CDMX[0].keys())
        writer.writeheader()
        writer.writerows(tacos_CDMX)
    print(f"✅ CSV saved as tacos_CDMX.csv with {len(tacos_CDMX)} places.")
else:
    print("⚠️ No results to save.")
