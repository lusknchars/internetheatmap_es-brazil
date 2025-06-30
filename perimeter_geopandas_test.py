import pandas as pd
import folium
import geopandas as gpd
from shapely.geometry import MultiPoint

# Carregar as coordenadas do arquivo CSV
df_coordinates = pd.read_csv("coordinates.csv")

# Criar pontos a partir das coordenadas
points = [(row["Longitude_Decimal_Final"], row["Latitude_Decimal_Final"]) 
          for index, row in df_coordinates.iterrows() if pd.notna(row["Longitude_Decimal_Final"]) and pd.notna(row["Latitude_Decimal_Final"])]

# Criar um mapa Folium centrado no Espírito Santo
map_es = folium.Map(location=[-20.29, -40.31], zoom_start=8)

# Opção 1: Usar GeoJSON do Espírito Santo
# Baixar o arquivo GeoJSON do Espírito Santo (você precisará fazer isso previamente)
# Você pode encontrar dados do IBGE ou outras fontes oficiais
try:
    # Carregar o GeoJSON do Espírito Santo
    es_geo = gpd.read_file("br_es.json")
    
    # Adicionar o polígono do ES ao mapa
    folium.GeoJson(
        es_geo,
        name='Espírito Santo',
        style_function=lambda x: {
            'fillColor': 'blue',
            'color': 'blue',
            'weight': 2,
            'fillOpacity': 0.2
        },
        tooltip='Estado do Espírito Santo'
    ).add_to(map_es)
    
except Exception as e:
    print(f"Erro ao carregar GeoJSON: {e}")
    
    # Opção 2: Definir manualmente os limites aproximados do ES
    # Coordenadas aproximadas dos limites do ES (sentido horário)
    es_boundaries = [
        [-21.30, -41.88],  # Sudoeste
        [-21.30, -39.70],  # Sudeste
        [-17.89, -39.70],  # Nordeste
        [-17.89, -41.88],  # Noroeste
        [-21.30, -41.88],  # Fechar o polígono
    ]
    
    # Adicionar o polígono do ES ao mapa
    folium.Polygon(
        locations=es_boundaries,
        color='blue',
        weight=2,
        fill_color='blue',
        fill_opacity=0.2,
        tooltip='Limites aproximados do Espírito Santo'
    ).add_to(map_es)

# Adicionar os pontos originais ao mapa para referência
for point in points:
    folium.CircleMarker(
        location=[point[1], point[0]],  # [lat, lon]
        radius=3,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
        tooltip='Ponto de Coordenada'
    ).add_to(map_es)

# Criar a envoltória convexa dos pontos (opcional, para comparação)
if points:
    multipoint = MultiPoint(points)
    convex_hull = multipoint.convex_hull
    
    # Adicionar a envoltória convexa ao mapa
    if convex_hull.geom_type == 'Polygon':
        folium.Polygon(
            locations=[[lat, lon] for lon, lat in convex_hull.exterior.coords],
            color='green',
            weight=2,
            fill_color='green',
            fill_opacity=0.1,
            tooltip='Envoltória Convexa dos Pontos'
        ).add_to(map_es)

# Adicionar controle de camadas
folium.LayerControl().add_to(map_es)

# Salvando o mapa
map_es.save("es_coverage_map.html")

print("Mapa de cobertura do Espírito Santo gerado e salvo como es_coverage_map.html")