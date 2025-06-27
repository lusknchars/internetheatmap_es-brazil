import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Configuração de página
st.set_page_config(
    page_title="Heatmap de Estações de Banda Larga do Espírito Santo",
    page_icon="📡",
    layout="wide"
)

# Título 
st.title("Mapa de Densidade de Estações de Banda Larga - Espírito Santo")

# Sidebar 
st.sidebar.header("Informações")
st.sidebar.write("Este mapa representa a densidade das estações de banda larga (3G,4G,5G) no estado do Espírito Santo.")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("Estacoes_SMP_ES_processado.csv", sep=";", encoding="utf-8-sig")
    
    # Filtrar apenas linhas com coordenadas válidas
    df_clean = df[["Latitude_Decimal_Final", "Longitude_Decimal_Final", "Empresa Estação", "Tecnologia", "Município-UF"]].dropna()
    return df_clean

# Carregar os dados
try:
    df = load_data()
    
    # Mostrar estatísticas básicas
    st.sidebar.metric("Total de Estações", len(df))
    st.sidebar.metric("Empresas Únicas", df["Empresa Estação"].nunique())
    
    # Filtros
    st.sidebar.subheader("Filtros")
    
    # Filtro por empresa
    empresas = st.sidebar.multiselect(
        "Selecione as Empresas:",
        options=df["Empresa Estação"].unique(),
        default=df["Empresa Estação"].unique()
    )
    
    # Filtro por tecnologia
    tecnologias = st.sidebar.multiselect(
        "Selecione as Tecnologias:",
        options=df["Tecnologia"].unique(),
        default=df["Tecnologia"].unique()
    )
    
    # Aplicar filtros
    df_filtered = df[
        (df["Empresa Estação"].isin(empresas)) & 
        (df["Tecnologia"].isin(tecnologias))
    ]
    
    # Criar o mapa
    if not df_filtered.empty:
        # Converter coordenadas para lista
        heat_data = df_filtered[["Latitude_Decimal_Final", "Longitude_Decimal_Final"]].values.tolist()
        
        # Criar mapa centrado no ES
        m = folium.Map(
            location=[-20.29, -40.31],
            zoom_start=8,
            tiles="OpenStreetMap"
        )
        
        # Adicionar heatmap
        HeatMap(
            heat_data,
            min_opacity=0.2,
            radius=15,
            blur=10,
            max_zoom=18,
        ).add_to(m)
        
        # Exibir o mapa
        st.subheader("Mapa de Densidade")
        st_folium(m, width=700, height=500)
        
        # Mostrar dados filtrados
        st.subheader("Dados Filtrados")
        st.dataframe(df_filtered)
        
    else:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
        
except FileNotFoundError:
    st.error("Arquivo 'Estacoes_SMP_ES_processado.csv' não encontrado. Certifique-se de que o arquivo está no diretório correto.")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {str(e)}")

