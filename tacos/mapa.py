import pandas as pd
import folium

# Leer los datos
df = pd.read_csv("tacos_CDMX.csv")

# Crear mapa centrado en el promedio de lat/lng
center_lat = df["lat"].mean()
center_lng = df["lng"].mean()
mapa = folium.Map(location=[center_lat, center_lng], zoom_start=12)

# Añadir cada taco como marcador
for _, row in df.iterrows():
    popup_text = f"""
    <b>{row['name']}</b><br>
    {row['address']}<br>
    Rating: {row.get('rating', 'N/A')}<br>
    Price Level: {row.get('priceLevel', 'N/A')}<br>
    """
    folium.Marker(
        location=[row["lat"], row["lng"]],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color="red", icon="cutlery", prefix="fa")
    ).add_to(mapa)

# Guardar el mapa
mapa.save("tacos_CDMX_map.html")
print("✅ Mapa guardado como tacos_CDMX_map.html")
