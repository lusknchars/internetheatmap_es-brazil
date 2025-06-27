import pandas as pd
import folium
from shapely.geometry import MultiPoint

# Carregar as coordenadas do arquivo CSV
df_coordinates = pd.read_csv("coordinates.csv")


points = [ (row["Longitude_Decimal_Final"], row["Latitude_Decimal_Final"]) for index, row in df_coordinates.iterrows()]

# Criando obejto MultiPoint
multipoint = MultiPoint(points)

# Calcular a envoltória convexa (Convex Hull)
convex_hull = multipoint.convex_hull

# Criar um mapa Folium centrado no Espírito Santo
map_es = folium.Map(location=[-20.29, -40.31], zoom_start=8)

# Adicionar o polígono da envoltória convexa ao mapa
# Verifica se o convex_hull é um polígono (pode ser um ponto ou linha se houver poucos pontos)
if convex_hull.geom_type == 'Polygon':
    # Folium : [latitude, longitude] para polígonos
    folium.Polygon(
        locations=[[lat, lon] for lon, lat in convex_hull.exterior.coords],
        color='blue',
        weight=2,
        fill_color='blue',
        fill_opacity=0.2,
        tooltip='Perímetro de Cobertura'
    ).add_to(map_es)
elif convex_hull.geom_type == 'Point':
    folium.Marker(
        location=[convex_hull.y, convex_hull.x],
        tooltip='Ponto de Cobertura'
    ).add_to(map_es)
elif convex_hull.geom_type == 'LineString':
    folium.PolyLine(
        locations=[[lat, lon] for lon, lat in convex_hull.coords],
        color='blue',
        weight=2,
        tooltip='Linha de Cobertura'
    ).add_to(map_es)

# Salvando o mapa
map_es.save("coverage_perimeter.html")

print("Perímetro de cobertura gerado e salvo como coverage_perimeter.html")


