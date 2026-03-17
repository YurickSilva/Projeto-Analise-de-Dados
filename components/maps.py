import folium
from streamlit_folium import st_folium
import pandas as pd
import streamlit as st
from metrics.interatividade import set_selecao

def render_mapa_atendimentos(df, id_pagina, response_atendimentos=None, lat_col='Latitude', lon_col='Longitude', permite_clique=True):
    df_mapa = df.dropna(subset=[lat_col, lon_col]).copy()
    df_mapa[lat_col] = pd.to_numeric(df_mapa[lat_col], errors='coerce')
    df_mapa[lon_col] = pd.to_numeric(df_mapa[lon_col], errors='coerce')
    df_mapa = df_mapa.dropna(subset=[lat_col, lon_col])

    selecionados = response_atendimentos.get('selected_rows') if response_atendimentos else None    
    if selecionados is not None and len(selecionados) > 0:
        df_foco = pd.DataFrame(selecionados)
        map_center = [df_foco[lat_col].mean(), df_foco[lon_col].mean()]
        map_zoom = 15 if len(selecionados) == 1 else 13
    elif not df_mapa.empty:
        map_center = [df_mapa[lat_col].mean(), df_mapa[lon_col].mean()]
        map_zoom = 12
    else:
        map_center, map_zoom = [-15.78, -47.93], 4

    m = folium.Map(location=map_center, zoom_start=map_zoom, tiles="cartodbpositron")

    for _, row in df_mapa.iterrows():
        status = str(row.get('Contrato', '')).strip().upper()
        cor_pin = "orange" if status == "SIM" else "red" if status == "RESCINDIDO" else "gray"
        
        folium.Marker(
            location=[row[lat_col], row[lon_col]],
            popup=f"Ticket: {row.get('Id_ticket')}",
            icon=folium.Icon(color=cor_pin, icon="info-sign")
        ).add_to(m)

    objetos_retorno = ["last_object_clicked"] if permite_clique else []

    map_output = st_folium(
        m, 
        key=f"map_{id_pagina}", 
        use_container_width=True, 
        height=500, 
        returned_objects=objetos_retorno
    )

    if permite_clique and map_output and map_output.get("last_object_clicked"):
        coords = map_output["last_object_clicked"]
        match = df_mapa[
            (df_mapa[lat_col].round(5) == round(coords['lat'], 5)) & 
            (df_mapa[lon_col].round(5) == round(coords['lng'], 5))
        ]
        if not match.empty:
            set_selecao(id_pagina, match.iloc[0]['Id_ticket'])
    
    return map_output