import pandas as pd
import folium

# Leer los datos
df = pd.read_csv("tacos_CDMX.csv")

# Crear mapa centrado en el promedio
center_lat = df["lat"].mean()
center_lng = df["lng"].mean()
mapa = folium.Map(location=[center_lat, center_lng], zoom_start=12)

# Función para asignar color según priceLevel
def get_color(price_level):
    if pd.isna(price_level):
        return "gray"
    elif price_level == "PRICE_LEVEL_INEXPENSIVE":
        return "green"
    elif price_level == "PRICE_LEVEL_MODERATE":
        return "blue"
    elif price_level == "PRICE_LEVEL_EXPENSIVE":
        return "orange"
    else:
        return "red"

# Añadir marcadores de lugares
for _, row in df.iterrows():
    color = get_color(row.get("priceLevel"))
    popup_text = f"""
    <b>{row['name']}</b><br>
    {row['address']}<br>
    Rating: {row.get('rating', 'N/A')}<br>
    Price Level: {row.get('priceLevel', 'N/A')}<br>
    """
    folium.Marker(
        location=[row["lat"], row["lng"]],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color=color, icon="cutlery", prefix="fa")
    ).add_to(mapa)

# Crear la cuadrícula 10x10 con etiquetas de coordenadas
lat_min, lng_min = 19.29099, -99.224607  # SW
lat_max, lng_max = 19.521517, -99.036189  # NE
grid_size = 10
lat_step = (lat_max - lat_min) / grid_size
lng_step = (lng_max - lng_min) / grid_size

for i in range(grid_size):
    for j in range(grid_size):
        sw_lat = lat_min + i * lat_step
        sw_lng = lng_min + j * lng_step
        ne_lat = sw_lat + lat_step
        ne_lng = sw_lng + lng_step

        bounds = [[sw_lat, sw_lng], [ne_lat, ne_lng]]
        folium.Rectangle(
            bounds=bounds,
            color="black",
            fill=False,
            weight=1
        ).add_to(mapa)

        label = f"{round(sw_lat, 5)}, {round(sw_lng, 5)}\n{round(ne_lat, 5)}, {round(ne_lng, 5)}"
        folium.Marker(
            location=[(sw_lat + ne_lat) / 2, (sw_lng + ne_lng) / 2],
            icon=folium.DivIcon(html=f"""<div style="font-size:8pt">{label}</div>""")
        ).add_to(mapa)

# Guardar mapa
map_file_path = "tacos_CDMX_grid_map.html"
mapa.save(map_file_path)
map_file_path
