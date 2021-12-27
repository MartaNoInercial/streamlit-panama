##########################################################################################
#                                  LIBRERIAS
##########################################################################################
import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import pydeck as pdk
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px
import os
import datetime
import geopandas as gpd
import folium
import streamlit as st
import geemap.foliumap as geemap
from datetime import date, timedelta, datetime
import plotly.graph_objects as go
import leafmap.foliumap as leafmap
from rois import *
##########################################################################################
#                                  app.py
##########################################################################################
import streamlit as st

st.set_page_config(layout="wide")

#today = str(date.today())
#tomorrow = str(date.today()+timedelta(days=1))
#hour_48 = str(date.today()+timedelta(days=2))

today = str(datetime(2021,10,3))
tomorrow = str(datetime(2021,10,3)+timedelta(days=1))
hour_48 = str(datetime(2021,10,3)+timedelta(days=2))
##########################################################################################
#                                  FUNCIONES
##########################################################################################

##########################################################################################
#                                  SCREENS
##########################################################################################
def general():

    st.image('logo-stiky-twp-nw-withe-600x252.png')
    st.title('Coleccion de dashboards')


def meteo_01():
    components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_01/index.html", height=1100)

def meteo_02():
    st.title('Información de la precipitación')

    col1, col2, col3 = st.columns((2,1,1))

    with col1:
        st.write('Efecto de la precipitación sobre el caudal de los rios:')
        components.iframe("https://theweatherpartner.xyz/martav/DC102/caudal+precip.html", height=800)

    with col2:
        path = "/Users/34691/Desktop/TWP/AppTimeLapse/meteo_precip_v2.csv"
        df = pd.read_csv(path)
        lat = st.slider("Selecciona la latitud:", min_value=round(min(df.Latitude),2), max_value=round(max(df.Latitude),2))
    with col3:
        lon = st.slider("Selecciona la longitud:", min_value=round(min(df.Longitude),2), max_value=round(max(df.Longitude),2))

    precip_today=((df[(round(df['Latitude'],1)==round(lat,1))&
                 (round(df['Longitude'],1)==round(lon,1))
                         &((df['Time'])==today)
                        ].PrecipitacionAcumulada))
    precip_24=((df[(round(df['Latitude'],1)==round(lat,1))&
                 (round(df['Longitude'],1)==round(lon,1))
                      &((df['Time'])==tomorrow)
                     ].PrecipitacionAcumulada))
    precip_48=((df[(round(df['Latitude'],1)==round(lat,1))&
                 (round(df['Longitude'],1)==round(lon,1))
                      &((df['Time'])==hour_48)
                     ].PrecipitacionAcumulada))

    col2.metric("Precipitacion acumulada de mañana en el punto seleccionado:",
                str(round(max(precip_24),2))+' mm',
                round(max(precip_24)-max(precip_today),2))

    col3.metric("Precipitacion acumulada de 24 a 48 horas en el punto seleccionado:",
                str(round(max(precip_48),2))+' mm',
                round(max(precip_48)-max(precip_24),2))

    with col2:
        fig = go.Figure(data=go.Scatter(x=df.Time, y=df.PrecipitacionAcumulada))
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.info("""
        Información del modelo:
        - ...
        - ...
        - ...
        """)

def meteo_03():
    st.title('Pronóstico de mañana')
    path = "/Users/34691/Desktop/TWP/AppTimeLapse/meteo_03.csv"
    df = pd.read_csv(path)
    when = st.select_slider('Selecciona el momento del dia:',options=['mañana','mediodia','tarde','noche'])
    col1, col2, col3 = st.columns((2,1,1))
    with col1:
        with st.expander("Mapa de avisos"):
            components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/alertas.html", height=400)
        with st.expander("Mapa de temperaturas"):
            if when == 'mañana':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/mapa_temperatura_06.html", height=400)
            if when == 'mediodia':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/mapa_temperatura_12.html", height=400)
            if when == 'tarde':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/mapa_temperatura_18.html", height=400)
            if when == 'noche':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/mapa_temperatura_00.html", height=400)
        with st.expander("Mapa de precipitación"):
            if when == 'mañana':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/mapa_precipitacion_06.html", height=400)
            if when == 'mediodia':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/mapa_precipitacion_12.html", height=400)
            if when == 'tarde':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/mapa_precipitacion_18.html", height=400)
            if when == 'noche':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/mapa_precipitacion_00.html", height=400)
        with st.expander("Mapa de vientos"):
            if when == 'mañana':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/vent_06/demo.html", height=400)
            if when == 'mediodia':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/vent_12/demo.html", height=400)
            if when == 'tarde':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/vent_18/demo.html", height=400)
            if when == 'noche':
                components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/vent_00/demo.html", height=400)
    if when == 'mañana':
        df = df[df['Time']=='2021-10-02 06:00:00']
        col2.metric("Avisos por precipitación:",
                    len(df[df['PrecipitacionAcumulada']>=92.0]))
        col3.metric("Avisos por viento:",
                    len(df[df['WindSpeed']>=10.0]))
        col2.metric("Temperatura máxima:",
                    round(max([x for x in df.Temperatura if str(x) != 'nan']),1))
        col3.metric("Temperatura mínima:",
                    round(min([x for x in df.Temperatura if str(x) != 'nan']),1))
    if when == 'mediodia':
        df = df[df['Time']=='2021-10-02 12:00:00']
        col2.metric("Avisos por precipitación:",
                    len(df[df['PrecipitacionAcumulada']>=92.0]))
        col3.metric("Avisos por viento:",
                    len(df[df['WindSpeed']>=10.0]))
        col2.metric("Temperatura máxima:",
                    round(max([x for x in df.Temperatura if str(x) != 'nan']),1))
        col3.metric("Temperatura mínima:",
                    round(min([x for x in df.Temperatura if str(x) != 'nan']),1))
    if when == 'tarde':
        df = df[df['Time']=='2021-10-02 18:00:00']
        col2.metric("Avisos por precipitación:",
                    len(df[df['PrecipitacionAcumulada']>=92.0]))
        col3.metric("Avisos por viento:",
                    len(df[df['WindSpeed']>=10.0]))
        col2.metric("Temperatura máxima:",
                    round(max([x for x in df.Temperatura if str(x) != 'nan']),1))
        col3.metric("Temperatura mínima:",
                    round(min([x for x in df.Temperatura if str(x) != 'nan']),1))
    if when == 'noche':
        df = df[df['Time']=='2021-10-02 00:00:00']
        col2.metric("Avisos por precipitación:",
                    len(df[df['PrecipitacionAcumulada']>=92.0]))
        col3.metric("Avisos por viento:",
                    len(df[df['WindSpeed']>=10.0]))
        col2.metric("Temperatura máxima:",
                    round(max([x for x in df.Temperatura if str(x) != 'nan']),1))
        col3.metric("Temperatura mínima:",
                    round(min([x for x in df.Temperatura if str(x) != 'nan']),1))
    with col2:
        lat = st.slider("Selecciona la latitud:", min_value=round(min(df.Latitude),2), max_value=round(max(df.Latitude),2))
    with col3:
        lon = st.slider("Selecciona la longitud:", min_value=round(min(df.Longitude),2), max_value=round(max(df.Longitude),2))
    if when == 'mañana':
        df = df[df['Time']=='2021-10-02 06:00:00']
        df = df[(round(df['Latitude'],1)==round(lat,1))&(round(df['Longitude'],1)==round(lon,1))]
        col2.metric("Temperatura:",
                    round(max([x for x in df.Temperatura if str(x) != 'nan']),1))
        col3.metric("Precipitaciones:",
                    round(max([x for x in df.PrecipitacionAcumulada if str(x) != 'nan']),1))
        col2.metric("Dirección del viento:",
                    round(max([x for x in df.WindDirection if str(x) != 'nan']),1))
        col3.metric("Velocidad del viento:",
                    round(max([x for x in df.WindSpeed if str(x) != 'nan']),1))
    if when == 'mediodia':
        df = df[df['Time']=='2021-10-02 12:00:00']
        df = df[(round(df['Latitude'],1)==round(lat,1))&(round(df['Longitude'],1)==round(lon,1))]
        col2.metric("Temperatura:",
                    round(max([x for x in df.Temperatura if str(x) != 'nan']),1))
        col3.metric("Precipitaciones:",
                    round(max([x for x in df.PrecipitacionAcumulada if str(x) != 'nan']),1))
        col2.metric("Dirección del viento:",
                    round(max([x for x in df.WindDirection if str(x) != 'nan']),1))
        col3.metric("Velocidad del viento:",
                    round(max([x for x in df.WindSpeed if str(x) != 'nan']),1))
    if when == 'tarde':
        df = df[df['Time']=='2021-10-02 18:00:00']
        df = df[(round(df['Latitude'],1)==round(lat,1))&(round(df['Longitude'],1)==round(lon,1))]
        col2.metric("Temperatura:",
                    round(max([x for x in df.Temperatura if str(x) != 'nan']),1))
        col3.metric("Precipitaciones:",
                    round(max([x for x in df.PrecipitacionAcumulada if str(x) != 'nan']),1))
        col2.metric("Dirección del viento:",
                    round(max([x for x in df.WindDirection if str(x) != 'nan']),1))
        col3.metric("Velocidad del viento:",
                    round(max([x for x in df.WindSpeed if str(x) != 'nan']),1))
    if when == 'noche':
        df = df[df['Time']=='2021-10-02 00:00:00']
        df = df[(round(df['Latitude'],1)==round(lat,1))&(round(df['Longitude'],1)==round(lon,1))]
        col2.metric("Temperatura:",
                    round(max([x for x in df.Temperatura if str(x) != 'nan']),1))
        col3.metric("Precipitaciones:",
                    round(max([x for x in df.PrecipitacionAcumulada if str(x) != 'nan']),1))
        col2.metric("Dirección del viento:",
                    round(max([x for x in df.WindDirection if str(x) != 'nan']),1))
        col3.metric("Velocidad del viento:",
                    round(max([x for x in df.WindSpeed if str(x) != 'nan']),1))

def meteo_04():
    st.title('Comparación con datos satélite')
    st.write('En construcción')

    col1, col2 = st.columns(2)

    with col1:
        st.header('Precipitación segun la predicción:')
        st.write('Aquí va un mapa')
        st.info('Info del modelo')
    with col2:
        st.header('Precipitación segun el satélite:')
        st.write('Aquí va un mapa')
        st.info('Info del satélite')


def hidro_01():
    st.title('Comparación de los distintos modelos')
    st.write('En construcción')
    path = '/Users/34691/Desktop/TWP/AppTimeLapse/sitios_toma_02.csv'
    df = pd.read_csv(path)
    st_list=list(dict.fromkeys(list(df.Nombre)))
    pois = st.multiselect('Selecciona los sitios toma', st_list)
    filtered = df[df['Nombre'].isin(pois)]
    if filtered.empty==True:
        filtered = df
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('WRF-Hydro')
        components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/pois.html",height=500)
        fig = go.Figure()
        for i in range(len(pois)):
            fig.add_trace(go.Scatter(x=df[df['Nombre']==(pois[i])].verification_time,
                                     y=df[df['Nombre']==(pois[i])].Flow_hydro,name=pois[i]))
        st.plotly_chart(fig, use_container_width=True)
        st.info('Información del modelo')
    with col2:
        st.header('HMS')
        components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/pois.html",height=500)
        fig = go.Figure()
        for i in range(len(pois)):
            fig.add_trace(go.Scatter(x=df[df['Nombre']==(pois[i])].verification_time,
                                     y=df[df['Nombre']==(pois[i])].Flow_hydro,name=pois[i]))
        st.plotly_chart(fig, use_container_width=True)
        st.info('Información del modelo')
    with col3:
        st.header('Tetis')
        components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/pois.html",height=500)
        fig = go.Figure()
        for i in range(len(pois)):
            fig.add_trace(go.Scatter(x=df[df['Nombre']==(pois[i])].verification_time,
                                     y=df[df['Nombre']==(pois[i])].Flow_hydro,name=pois[i]))
        st.plotly_chart(fig, use_container_width=True)
        st.info('Información del modelo')

def hidro_02():
    st.title('Caudal con WRF-Hydro')

    path = '/Users/34691/Desktop/TWP/AppTimeLapse/sitios_toma_02.csv'
    df = pd.read_csv(path)
    st_list=list(dict.fromkeys(list(df.Nombre)))
    pois = st.multiselect('Selecciona los sitios toma', st_list)
    filtered = df[df['Nombre'].isin(pois)]
    if filtered.empty==True:
        filtered = df

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Caudal máximo hoy:",
                round(max(list(filtered[filtered['verification_time']=='2021-10-28 18:00:00'].Flow_hydro)),2))
    col2.metric("Caudal máximo mañana:",
                round(max(list(filtered[filtered['verification_time']=='2021-10-28 20:00:00'].Flow_hydro)),2))
    col2.metric("Caudal máximo los próximos 7 dias:",
                round(max(list(filtered[filtered['verification_time']=='2021-10-28 23:00:00'].Flow_hydro)),2))
    col3.metric("Alertas:",
                len(list(filtered[filtered['Flow_hydro']>=400.0])))

    col1, col2 = st.columns(2)

    with col1:
        components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/pois.html",height=500)
    with col2:
        fig = go.Figure()
        for i in range(len(pois)):
            fig.add_trace(go.Scatter(x=df[df['Nombre']==(pois[i])].verification_time,
                                     y=df[df['Nombre']==(pois[i])].Flow_hydro,name=pois[i]))
        st.plotly_chart(fig, use_container_width=True)

    st.info('Información del modelo')

def hidro_03():
    st.title('Caudal con HMS')

    path = '/Users/34691/Desktop/TWP/AppTimeLapse/sitios_toma_02.csv'
    df = pd.read_csv(path)
    st_list=list(dict.fromkeys(list(df.Nombre)))
    pois = st.multiselect('Selecciona los sitios toma', st_list)
    filtered = df[df['Nombre'].isin(pois)]
    if filtered.empty==True:
        filtered = df

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Caudal máximo hoy:",
                round(max(list(filtered[filtered['verification_time']=='2021-10-28 18:00:00'].Flow_hms)),2))
    col2.metric("Caudal máximo mañana:",
                round(max(list(filtered[filtered['verification_time']=='2021-10-28 20:00:00'].Flow_hms)),2))
    col2.metric("Caudal máximo los próximos 7 dias:",
                round(max(list(filtered[filtered['verification_time']=='2021-10-28 23:00:00'].Flow_hms)),2))
    col3.metric("Alertas:",
                len(list(filtered[filtered['Flow_hydro']>=400.0])))

    col1, col2 = st.columns(2)

    with col1:
        components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/pois.html",height=500)
    with col2:
        fig = go.Figure()
        for i in range(len(pois)):
            fig.add_trace(go.Scatter(x=df[df['Nombre']==(pois[i])].verification_time,
                                     y=df[df['Nombre']==(pois[i])].Flow_hms,name=pois[i]))
        st.plotly_chart(fig, use_container_width=True)

    st.info('Información del modelo')

def hidro_04():
    st.title('Caudal con Tetis')

    path = '/Users/34691/Desktop/TWP/AppTimeLapse/sitios_toma_02.csv'
    df = pd.read_csv(path)
    st_list=list(dict.fromkeys(list(df.Nombre)))
    pois = st.multiselect('Selecciona los sitios toma', st_list)
    filtered = df[df['Nombre'].isin(pois)]
    if filtered.empty==True:
        filtered = df

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Caudal máximo hoy:",
                round(max(list(filtered[filtered['verification_time']=='2021-10-28 18:00:00'].Flow_hydro)),2))
    col2.metric("Caudal máximo mañana:",
                round(max(list(filtered[filtered['verification_time']=='2021-10-28 20:00:00'].Flow_hydro)),2))
    col2.metric("Caudal máximo los próximos 7 dias:",
                round(max(list(filtered[filtered['verification_time']=='2021-10-28 23:00:00'].Flow_hydro)),2))
    col3.metric("Alertas:",
                len(list(filtered[filtered['Flow_hydro']>=400.0])))

    col1, col2 = st.columns(2)

    with col1:
        components.iframe("https://theweatherpartner.xyz/martav/DC102/meteo_03/pois.html",height=500)
    with col2:
        fig = go.Figure()
        for i in range(len(pois)):
            fig.add_trace(go.Scatter(x=df[df['Nombre']==(pois[i])].verification_time,
                                     y=df[df['Nombre']==(pois[i])].Flow_hydro,name=pois[i]))
        st.plotly_chart(fig, use_container_width=True)

    st.info('Información del modelo')

def uploaded_file_to_gdf(data):
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.getbuffer())

    if file_path.lower().endswith(".kml"):
        gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"
        gdf = gpd.read_file(file_path, driver="KML")
    else:
        gdf = gpd.read_file(file_path)

    return gdf

def timelapse():
#    uploaded_file_to_gdf()
    app()


@st.cache
def uploaded_file_to_gdf(data):
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.getbuffer())

    if file_path.lower().endswith(".kml"):
        gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"
        gdf = gpd.read_file(file_path, driver="KML")
    else:
        gdf = gpd.read_file(file_path)

    return gdf


def app():

    today = date.today()

    st.title("Crear una Timelapse")

    row1_col1, row1_col2 = st.columns([2, 1])

    if st.session_state.get("zoom_level") is None:
        st.session_state["zoom_level"] = 4

    st.session_state["ee_asset_id"] = None
    st.session_state["bands"] = None
    st.session_state["palette"] = None
    st.session_state["vis_params"] = None

    with row1_col1:
        m = geemap.Map(
            basemap="HYBRID", plugin_Draw=True, draw_export=True, locate_control=True
        )
        m.add_basemap("ROADMAP")

    with row1_col2:

        keyword = st.text_input("Search for a location:", "")
        if keyword:
            locations = geemap.geocode(keyword)
            if locations is not None and len(locations) > 0:
                str_locations = [str(g)[1:-1] for g in locations]
                location = st.selectbox("Select a location:", str_locations)
                loc_index = str_locations.index(location)
                selected_loc = locations[loc_index]
                lat, lng = selected_loc.lat, selected_loc.lng
                folium.Marker(location=[lat, lng], popup=location).add_to(m)
                m.set_center(lng, lat, 12)
                st.session_state["zoom_level"] = 12

        collection = st.selectbox(
            "Select a satellite image collection: ",
            [
                "Any Earth Engine ImageCollection",
                "Landsat TM-ETM-OLI Surface Reflectance",
                "Sentinel-2 MSI Surface Reflectance",
                "Geostationary Operational Environmental Satellites (GOES)",
                "MODIS Vegetation Indices (NDVI/EVI) 16-Day Global 1km",
                "MODIS Gap filled Land Surface Temperature Daily",
                "USDA National Agriculture Imagery Program (NAIP)",
            ],
            index=1,
        )

        if collection in [
            "Landsat TM-ETM-OLI Surface Reflectance",
            "Sentinel-2 MSI Surface Reflectance",
        ]:
            roi_options = ["Uploaded GeoJSON"] + list(landsat_rois.keys())

        elif collection == "Geostationary Operational Environmental Satellites (GOES)":
            roi_options = ["Uploaded GeoJSON"] + list(goes_rois.keys())

        elif collection in [
            "MODIS Vegetation Indices (NDVI/EVI) 16-Day Global 1km",
            "MODIS Gap filled Land Surface Temperature Daily",
        ]:
            roi_options = ["Uploaded GeoJSON"] + list(modis_rois.keys())
        else:
            roi_options = ["Uploaded GeoJSON"]

        if collection == "Any Earth Engine ImageCollection":
            keyword = st.text_input("Enter a keyword to search (e.g., MODIS):", "")
            if keyword:

                assets = geemap.search_ee_data(keyword)
                ee_assets = []
                for asset in assets:
                    if asset["ee_id_snippet"].startswith("ee.ImageCollection"):
                        ee_assets.append(asset)

                asset_titles = [x["title"] for x in ee_assets]
                dataset = st.selectbox("Select a dataset:", asset_titles)
                if len(ee_assets) > 0:
                    st.session_state["ee_assets"] = ee_assets
                    st.session_state["asset_titles"] = asset_titles
                    index = asset_titles.index(dataset)
                    ee_id = ee_assets[index]["id"]
                else:
                    ee_id = ""

                if dataset is not None:
                    with st.expander("Show dataset details", False):
                        index = asset_titles.index(dataset)
                        html = geemap.ee_data_html(st.session_state["ee_assets"][index])
                        st.markdown(html, True)
            # elif collection == "MODIS Gap filled Land Surface Temperature Daily":
            #     ee_id = ""
            else:
                ee_id = ""

            asset_id = st.text_input("Enter an ee.ImageCollection asset ID:", ee_id)

            if asset_id:
                with st.expander("Customize band combination and color palette", True):
                    try:
                        col = ee.ImageCollection.load(asset_id)
                        size = col.size().getInfo()
                        st.session_state["ee_asset_id"] = asset_id
                    except:
                        st.error("Invalid Earth Engine asset ID.")
                        st.session_state["ee_asset_id"] = None
                        return

                    img_bands = col.first().bandNames().getInfo()
                    if len(img_bands) >= 3:
                        default_bands = img_bands[:3][::-1]
                    else:
                        default_bands = img_bands[:]
                    bands = st.multiselect(
                        "Select one or three bands (RGB):", img_bands, default_bands
                    )
                    st.session_state["bands"] = bands

                    if len(bands) == 1:
                        palette_options = st.selectbox(
                            "Color palette",
                            cm.list_colormaps(),
                            index=2,
                        )
                        palette_values = cm.get_palette(palette_options, 15)
                        palette = st.text_area(
                            "Enter a custom palette:",
                            palette_values,
                        )
                        st.write(
                            cm.plot_colormap(cmap=palette_options, return_fig=True)
                        )
                        st.session_state["palette"] = eval(palette)

                    if bands:
                        vis_params = st.text_area(
                            "Enter visualization parameters",
                            "{'bands': ["
                            + ", ".join([f"'{band}'" for band in bands])
                            + "]}",
                        )
                    else:
                        vis_params = st.text_area(
                            "Enter visualization parameters",
                            "{}",
                        )
                    try:
                        st.session_state["vis_params"] = eval(vis_params)
                        st.session_state["vis_params"]["palette"] = st.session_state[
                            "palette"
                        ]
                    except Exception as e:
                        st.session_state["vis_params"] = None
                        st.error(
                            f"Invalid visualization parameters. It must be a dictionary."
                        )

        elif collection == "MODIS Gap filled Land Surface Temperature Daily":
            with st.expander("Show dataset details", False):
                st.markdown(
                    """
                See the [Awesome GEE Community Datasets](https://samapriya.github.io/awesome-gee-community-datasets/projects/daily_lst/).
                """
                )

            MODIS_options = ["Daytime (1:30 pm)", "Nighttime (1:30 am)"]
            MODIS_option = st.selectbox("Select a MODIS dataset:", MODIS_options)
            if MODIS_option == "Daytime (1:30 pm)":
                st.session_state[
                    "ee_asset_id"
                ] = "projects/sat-io/open-datasets/gap-filled-lst/gf_day_1km"
            else:
                st.session_state[
                    "ee_asset_id"
                ] = "projects/sat-io/open-datasets/gap-filled-lst/gf_night_1km"

            palette_options = st.selectbox(
                "Color palette",
                cm.list_colormaps(),
                index=90,
            )
            palette_values = cm.get_palette(palette_options, 15)
            palette = st.text_area(
                "Enter a custom palette:",
                palette_values,
            )
            st.write(cm.plot_colormap(cmap=palette_options, return_fig=True))
            st.session_state["palette"] = eval(palette)

        sample_roi = st.selectbox(
            "Select a sample ROI or upload a GeoJSON file:",
            roi_options,
            index=0,
        )

        add_outline = st.checkbox(
            "Overlay an administrative boundary on timelapse", False
        )

        if add_outline:

            with st.expander("Customize administrative boundary", True):

                overlay_options = {
                    "User-defined": None,
                    "Continents": "continents",
                    "Countries": "countries",
                    "US States": "us_states",
                    "China": "china",
                }

                overlay = st.selectbox(
                    "Select an administrative boundary:",
                    list(overlay_options.keys()),
                    index=2,
                )

                overlay_data = overlay_options[overlay]

                if overlay_data is None:
                    overlay_data = st.text_input(
                        "Enter an HTTP URL to a GeoJSON file or an ee.FeatureCollection asset id:",
                        "https://raw.githubusercontent.com/giswqs/geemap/master/examples/data/countries.geojson",
                    )

                overlay_color = st.color_picker(
                    "Select a color for the administrative boundary:", "#000000"
                )
                overlay_width = st.slider(
                    "Select a line width for the administrative boundary:", 1, 20, 1
                )
                overlay_opacity = st.slider(
                    "Select an opacity for the administrative boundary:",
                    0.0,
                    1.0,
                    1.0,
                    0.05,
                )
        else:
            overlay_data = None
            overlay_color = "black"
            overlay_width = 1
            overlay_opacity = 1

    with row1_col1:

        st.markdown(
            "Steps: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button."
        )

        data = st.file_uploader(
            "Upload a GeoJSON file to use as an ROI. Customize timelapse parameters and then click the Submit button 😇👇",
            type=["geojson"],
        )

        crs = {"init": "epsg:4326"}
        if sample_roi == "Uploaded GeoJSON":
            if data is None:
                # st.info(
                #     "Steps to create a timelapse: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click Submit button"
                # )
                if (
                    collection
                    in [
                        "Geostationary Operational Environmental Satellites (GOES)",
                        "USDA National Agriculture Imagery Program (NAIP)",
                    ]
                    and (not keyword)
                ):
                    m.set_center(-100, 40, 3)
                # else:
                #     m.set_center(4.20, 18.63, zoom=2)
        else:
            if collection in [
                "Landsat TM-ETM-OLI Surface Reflectance",
                "Sentinel-2 MSI Surface Reflectance",
            ]:
                gdf = gpd.GeoDataFrame(
                    index=[0], crs=crs, geometry=[landsat_rois[sample_roi]]
                )
            elif (
                collection
                == "Geostationary Operational Environmental Satellites (GOES)"
            ):
                gdf = gpd.GeoDataFrame(
                    index=[0], crs=crs, geometry=[goes_rois[sample_roi]["region"]]
                )
            elif collection == "MODIS Vegetation Indices (NDVI/EVI) 16-Day Global 1km":
                gdf = gpd.GeoDataFrame(
                    index=[0], crs=crs, geometry=[modis_rois[sample_roi]]
                )

        if sample_roi != "Uploaded GeoJSON":

            if collection in [
                "Landsat TM-ETM-OLI Surface Reflectance",
                "Sentinel-2 MSI Surface Reflectance",
            ]:
                gdf = gpd.GeoDataFrame(
                    index=[0], crs=crs, geometry=[landsat_rois[sample_roi]]
                )
            elif (
                collection
                == "Geostationary Operational Environmental Satellites (GOES)"
            ):
                gdf = gpd.GeoDataFrame(
                    index=[0], crs=crs, geometry=[goes_rois[sample_roi]["region"]]
                )
            elif collection in [
                "MODIS Vegetation Indices (NDVI/EVI) 16-Day Global 1km",
                "MODIS Gap filled Land Surface Temperature Daily",
            ]:
                gdf = gpd.GeoDataFrame(
                    index=[0], crs=crs, geometry=[modis_rois[sample_roi]]
                )
            st.session_state["roi"] = geemap.geopandas_to_ee(gdf, geodesic=False)
            m.add_gdf(gdf, "ROI")
        elif data:
            gdf = uploaded_file_to_gdf(data)
            st.session_state["roi"] = geemap.geopandas_to_ee(gdf, geodesic=False)
            m.add_gdf(gdf, "ROI")

        m.to_streamlit(height=600)

    with row1_col2:

        if collection in [
            "Landsat TM-ETM-OLI Surface Reflectance",
            "Sentinel-2 MSI Surface Reflectance",
        ]:

            if collection == "Landsat TM-ETM-OLI Surface Reflectance":
                sensor_start_year = 1984
                timelapse_title = "Landsat Timelapse"
                timelapse_speed = 5
            elif collection == "Sentinel-2 MSI Surface Reflectance":
                sensor_start_year = 2015
                timelapse_title = "Sentinel-2 Timelapse"
                timelapse_speed = 5

            with st.form("submit_landsat_form"):

                roi = None
                if st.session_state.get("roi") is not None:
                    roi = st.session_state.get("roi")
                out_gif = geemap.temp_file_path(".gif")

                title = st.text_input(
                    "Enter a title to show on the timelapse: ", timelapse_title
                )
                RGB = st.selectbox(
                    "Select an RGB band combination:",
                    [
                        "Red/Green/Blue",
                        "NIR/Red/Green",
                        "SWIR2/SWIR1/NIR",
                        "NIR/SWIR1/Red",
                        "SWIR2/NIR/Red",
                        "SWIR2/SWIR1/Red",
                        "SWIR1/NIR/Blue",
                        "NIR/SWIR1/Blue",
                        "SWIR2/NIR/Green",
                        "SWIR1/NIR/Red",
                        "SWIR2/NIR/SWIR1",
                        "SWIR1/NIR/SWIR2",
                    ],
                    index=9,
                )

                frequency = st.selectbox(
                    "Select a temporal frequency:",
                    ["year", "quarter", "month"],
                    index=0,
                )

                with st.expander("Customize timelapse"):

                    speed = st.slider("Frames per second:", 1, 30, timelapse_speed)
                    dimensions = st.slider(
                        "Maximum dimensions (Width*Height) in pixels", 768, 2000, 768
                    )
                    progress_bar_color = st.color_picker(
                        "Progress bar color:", "#0000ff"
                    )
                    years = st.slider(
                        "Start and end year:",
                        sensor_start_year,
                        today.year,
                        (sensor_start_year, today.year),
                    )
                    months = st.slider("Start and end month:", 1, 12, (1, 12))
                    font_size = st.slider("Font size:", 10, 50, 30)
                    font_color = st.color_picker("Font color:", "#ffffff")
                    apply_fmask = st.checkbox(
                        "Apply fmask (remove clouds, shadows, snow)", True
                    )
                    font_type = st.selectbox(
                        "Select the font type for the title:",
                        ["arial.ttf", "alibaba.otf"],
                        index=0,
                    )
                    mp4 = st.checkbox("Save timelapse as MP4", True)

                empty_text = st.empty()
                empty_image = st.empty()
                empty_fire_image = st.empty()
                empty_video = st.container()
                submitted = st.form_submit_button("Submit")
                if submitted:

                    if sample_roi == "Uploaded GeoJSON" and data is None:
                        empty_text.warning(
                            "Steps to create a timelapse: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Alternatively, you can select a sample ROI from the dropdown list."
                        )
                    else:

                        empty_text.text("Computing... Please wait...")

                        start_year = years[0]
                        end_year = years[1]
                        start_date = str(months[0]).zfill(2) + "-01"
                        end_date = str(months[1]).zfill(2) + "-30"
                        bands = RGB.split("/")

                        try:
                            if collection == "Landsat TM-ETM-OLI Surface Reflectance":
                                out_gif = geemap.landsat_timelapse(
                                    roi=roi,
                                    out_gif=out_gif,
                                    start_year=start_year,
                                    end_year=end_year,
                                    start_date=start_date,
                                    end_date=end_date,
                                    bands=bands,
                                    apply_fmask=apply_fmask,
                                    frames_per_second=speed,
                                    dimensions=dimensions,
                                    overlay_data=overlay_data,
                                    overlay_color=overlay_color,
                                    overlay_width=overlay_width,
                                    overlay_opacity=overlay_opacity,
                                    frequency=frequency,
                                    date_format=None,
                                    title=title,
                                    title_xy=("2%", "90%"),
                                    add_text=True,
                                    text_xy=("2%", "2%"),
                                    text_sequence=None,
                                    font_type=font_type,
                                    font_size=font_size,
                                    font_color=font_color,
                                    add_progress_bar=True,
                                    progress_bar_color=progress_bar_color,
                                    progress_bar_height=5,
                                    loop=0,
                                    mp4=mp4,
                                )
                            elif collection == "Sentinel-2 MSI Surface Reflectance":
                                out_gif = geemap.sentinel2_timelapse(
                                    roi=roi,
                                    out_gif=out_gif,
                                    start_year=start_year,
                                    end_year=end_year,
                                    start_date=start_date,
                                    end_date=end_date,
                                    bands=bands,
                                    apply_fmask=apply_fmask,
                                    frames_per_second=speed,
                                    dimensions=dimensions,
                                    overlay_data=overlay_data,
                                    overlay_color=overlay_color,
                                    overlay_width=overlay_width,
                                    overlay_opacity=overlay_opacity,
                                    frequency=frequency,
                                    date_format=None,
                                    title=title,
                                    title_xy=("2%", "90%"),
                                    add_text=True,
                                    text_xy=("2%", "2%"),
                                    text_sequence=None,
                                    font_type=font_type,
                                    font_size=font_size,
                                    font_color=font_color,
                                    add_progress_bar=True,
                                    progress_bar_color=progress_bar_color,
                                    progress_bar_height=5,
                                    loop=0,
                                    mp4=mp4,
                                )
                        except:
                            empty_text.error(
                                "An error occurred while computing the timelapse. Your probably requested too much data. Try reducing the ROI or timespan."
                            )
                            st.stop()

                        if out_gif is not None and os.path.exists(out_gif):

                            empty_text.text(
                                "Right click the GIF to save it to your computer👇"
                            )
                            empty_image.image(out_gif)

                            out_mp4 = out_gif.replace(".gif", ".mp4")
                            if mp4 and os.path.exists(out_mp4):
                                with empty_video:
                                    st.text(
                                        "Right click the MP4 to save it to your computer👇"
                                    )
                                    st.video(out_gif.replace(".gif", ".mp4"))

                        else:
                            empty_text.error(
                                "Something went wrong. You probably requested too much data. Try reducing the ROI or timespan."
                            )

        elif collection == "Geostationary Operational Environmental Satellites (GOES)":


            with st.form("submit_goes_form"):

                roi = None
                if st.session_state.get("roi") is not None:
                    roi = st.session_state.get("roi")
                out_gif = geemap.temp_file_path(".gif")

                satellite = st.selectbox("Select a satellite:", ["GOES-17", "GOES-16"])
                earliest_date = datetime.date(2017, 7, 10)
                latest_date = datetime.date.today()

                if sample_roi == "Uploaded GeoJSON":
                    roi_start_date = today - datetime.timedelta(days=2)
                    roi_end_date = today - datetime.timedelta(days=1)
                    roi_start_time = datetime.time(14, 00)
                    roi_end_time = datetime.time(1, 00)
                else:
                    roi_start = goes_rois[sample_roi]["start_time"]
                    roi_end = goes_rois[sample_roi]["end_time"]
                    roi_start_date = datetime.datetime.strptime(
                        roi_start[:10], "%Y-%m-%d"
                    )
                    roi_end_date = datetime.datetime.strptime(roi_end[:10], "%Y-%m-%d")
                    roi_start_time = datetime.time(
                        int(roi_start[11:13]), int(roi_start[14:16])
                    )
                    roi_end_time = datetime.time(
                        int(roi_end[11:13]), int(roi_end[14:16])
                    )

                start_date = st.date_input("Select the start date:", roi_start_date)
                end_date = st.date_input("Select the end date:", roi_end_date)

                with st.expander("Customize timelapse"):

                    add_fire = st.checkbox("Add Fire/Hotspot Characterization", False)

                    scan_type = st.selectbox(
                        "Select a scan type:", ["Full Disk", "CONUS", "Mesoscale"]
                    )

                    start_time = st.time_input(
                        "Select the start time of the start date:", roi_start_time
                    )

                    end_time = st.time_input(
                        "Select the end time of the end date:", roi_end_time
                    )

                    start = (
                        start_date.strftime("%Y-%m-%d")
                        + "T"
                        + start_time.strftime("%H:%M:%S")
                    )
                    end = (
                        end_date.strftime("%Y-%m-%d")
                        + "T"
                        + end_time.strftime("%H:%M:%S")
                    )

                    speed = st.slider("Frames per second:", 1, 30, 5)
                    add_progress_bar = st.checkbox("Add a progress bar", True)
                    progress_bar_color = st.color_picker(
                        "Progress bar color:", "#0000ff"
                    )
                    font_size = st.slider("Font size:", 10, 50, 20)
                    font_color = st.color_picker("Font color:", "#ffffff")
                    mp4 = st.checkbox("Save timelapse as MP4", True)

                empty_text = st.empty()
                empty_image = st.empty()
                empty_video = st.container()
                empty_fire_text = st.empty()
                empty_fire_image = st.empty()

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if sample_roi == "Uploaded GeoJSON" and data is None:
                        empty_text.warning(
                            "Steps to create a timelapse: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Alternatively, you can select a sample ROI from the dropdown list."
                        )
                    else:
                        empty_text.text("Computing... Please wait...")

                        geemap.goes_timelapse(
                            out_gif,
                            start_date=start,
                            end_date=end,
                            data=satellite,
                            scan=scan_type.replace(" ", "_").lower(),
                            region=roi,
                            dimensions=768,
                            framesPerSecond=speed,
                            date_format="YYYY-MM-dd HH:mm",
                            xy=("3%", "3%"),
                            text_sequence=None,
                            font_type="arial.ttf",
                            font_size=font_size,
                            font_color=font_color,
                            add_progress_bar=add_progress_bar,
                            progress_bar_color=progress_bar_color,
                            progress_bar_height=5,
                            loop=0,
                            overlay_data=overlay_data,
                            overlay_color=overlay_color,
                            overlay_width=overlay_width,
                            overlay_opacity=overlay_opacity,
                            mp4=mp4,
                        )

                        if out_gif is not None and os.path.exists(out_gif):
                            empty_text.text(
                                "Right click the GIF to save it to your computer👇"
                            )
                            empty_image.image(out_gif)

                            out_mp4 = out_gif.replace(".gif", ".mp4")
                            if mp4 and os.path.exists(out_mp4):
                                with empty_video:
                                    st.text(
                                        "Right click the MP4 to save it to your computer👇"
                                    )
                                    st.video(out_gif.replace(".gif", ".mp4"))

                            if add_fire:
                                out_fire_gif = geemap.temp_file_path(".gif")
                                empty_fire_text.text(
                                    "Delineating Fire Hotspot... Please wait..."
                                )
                                geemap.goes_fire_timelapse(
                                    out_fire_gif,
                                    start_date=start,
                                    end_date=end,
                                    data=satellite,
                                    scan=scan_type.replace(" ", "_").lower(),
                                    region=roi,
                                    dimensions=768,
                                    framesPerSecond=speed,
                                    date_format="YYYY-MM-dd HH:mm",
                                    xy=("3%", "3%"),
                                    text_sequence=None,
                                    font_type="arial.ttf",
                                    font_size=font_size,
                                    font_color=font_color,
                                    add_progress_bar=add_progress_bar,
                                    progress_bar_color=progress_bar_color,
                                    progress_bar_height=5,
                                    loop=0,
                                )
                                if os.path.exists(out_fire_gif):
                                    empty_fire_image.image(out_fire_gif)
                        else:
                            empty_text.text(
                                "Something went wrong, either the ROI is too big or there are no data available for the specified date range. Please try a smaller ROI or different date range."
                            )

        elif collection == "MODIS Vegetation Indices (NDVI/EVI) 16-Day Global 1km":


            satellite = st.selectbox("Select a satellite:", ["Terra", "Aqua"])
            band = st.selectbox("Select a band:", ["NDVI", "EVI"])

            with st.form("submit_modis_form"):

                roi = None
                if st.session_state.get("roi") is not None:
                    roi = st.session_state.get("roi")
                out_gif = geemap.temp_file_path(".gif")

                with st.expander("Customize timelapse"):

                    start = st.date_input(
                        "Select a start date:", datetime.date(2000, 2, 8)
                    )
                    end = st.date_input("Select an end date:", datetime.date.today())

                    start_date = start.strftime("%Y-%m-%d")
                    end_date = end.strftime("%Y-%m-%d")

                    speed = st.slider("Frames per second:", 1, 30, 5)
                    add_progress_bar = st.checkbox("Add a progress bar", True)
                    progress_bar_color = st.color_picker(
                        "Progress bar color:", "#0000ff"
                    )
                    font_size = st.slider("Font size:", 10, 50, 20)
                    font_color = st.color_picker("Font color:", "#ffffff")

                    font_type = st.selectbox(
                        "Select the font type for the title:",
                        ["arial.ttf", "alibaba.otf"],
                        index=0,
                    )
                    mp4 = st.checkbox("Save timelapse as MP4", True)

                empty_text = st.empty()
                empty_image = st.empty()
                empty_video = st.container()

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if sample_roi == "Uploaded GeoJSON" and data is None:
                        empty_text.warning(
                            "Steps to create a timelapse: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Alternatively, you can select a sample ROI from the dropdown list."
                        )
                    else:

                        empty_text.text("Computing... Please wait...")

                        geemap.modis_ndvi_timelapse(
                            out_gif,
                            satellite,
                            band,
                            start_date,
                            end_date,
                            roi,
                            768,
                            speed,
                            overlay_data=overlay_data,
                            overlay_color=overlay_color,
                            overlay_width=overlay_width,
                            overlay_opacity=overlay_opacity,
                            mp4=mp4,
                        )

                        geemap.reduce_gif_size(out_gif)

                        empty_text.text(
                            "Right click the GIF to save it to your computer👇"
                        )
                        empty_image.image(out_gif)

                        out_mp4 = out_gif.replace(".gif", ".mp4")
                        if mp4 and os.path.exists(out_mp4):
                            with empty_video:
                                st.text(
                                    "Right click the MP4 to save it to your computer👇"
                                )
                                st.video(out_gif.replace(".gif", ".mp4"))

        elif collection == "Any Earth Engine ImageCollection":

            with st.form("submit_ts_form"):
                with st.expander("Customize timelapse"):

                    title = st.text_input(
                        "Enter a title to show on the timelapse: ", "Timelapse"
                    )
                    start_date = st.date_input(
                        "Select the start date:", datetime.date(2020, 1, 1)
                    )
                    end_date = st.date_input(
                        "Select the end date:", datetime.date.today()
                    )
                    frequency = st.selectbox(
                        "Select a temporal frequency:",
                        ["year", "quarter", "month", "day", "hour", "minute", "second"],
                        index=0,
                    )
                    reducer = st.selectbox(
                        "Select a reducer for aggregating data:",
                        ["median", "mean", "min", "max", "sum", "variance", "stdDev"],
                        index=0,
                    )
                    data_format = st.selectbox(
                        "Select a date format to show on the timelapse:",
                        [
                            "YYYY-MM-dd",
                            "YYYY",
                            "YYMM-MM",
                            "YYYY-MM-dd HH:mm",
                            "YYYY-MM-dd HH:mm:ss",
                            "HH:mm",
                            "HH:mm:ss",
                            "w",
                            "M",
                            "d",
                            "D",
                        ],
                        index=0,
                    )

                    speed = st.slider("Frames per second:", 1, 30, 5)
                    add_progress_bar = st.checkbox("Add a progress bar", True)
                    progress_bar_color = st.color_picker(
                        "Progress bar color:", "#0000ff"
                    )
                    font_size = st.slider("Font size:", 10, 50, 30)
                    font_color = st.color_picker("Font color:", "#ffffff")
                    font_type = st.selectbox(
                        "Select the font type for the title:",
                        ["arial.ttf", "alibaba.otf"],
                        index=0,
                    )
                    mp4 = st.checkbox("Save timelapse as MP4", True)

                empty_text = st.empty()
                empty_image = st.empty()
                empty_video = st.container()
                empty_fire_image = st.empty()

                roi = None
                if st.session_state.get("roi") is not None:
                    roi = st.session_state.get("roi")
                out_gif = geemap.temp_file_path(".gif")

                submitted = st.form_submit_button("Submit")
                if submitted:

                    if sample_roi == "Uploaded GeoJSON" and data is None:
                        empty_text.warning(
                            "Steps to create a timelapse: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Alternatively, you can select a sample ROI from the dropdown list."
                        )
                    else:

                        empty_text.text("Computing... Please wait...")
                        try:
                            geemap.create_timelapse(
                                st.session_state.get("ee_asset_id"),
                                start_date=start_date.strftime("%Y-%m-%d"),
                                end_date=end_date.strftime("%Y-%m-%d"),
                                region=roi,
                                frequency=frequency,
                                reducer=reducer,
                                date_format=data_format,
                                out_gif=out_gif,
                                bands=st.session_state.get("bands"),
                                palette=st.session_state.get("palette"),
                                vis_params=st.session_state.get("vis_params"),
                                dimensions=768,
                                frames_per_second=speed,
                                crs="EPSG:3857",
                                overlay_data=overlay_data,
                                overlay_color=overlay_color,
                                overlay_width=overlay_width,
                                overlay_opacity=overlay_opacity,
                                title=title,
                                title_xy=("2%", "90%"),
                                add_text=True,
                                text_xy=("2%", "2%"),
                                text_sequence=None,
                                font_type=font_type,
                                font_size=font_size,
                                font_color=font_color,
                                add_progress_bar=add_progress_bar,
                                progress_bar_color=progress_bar_color,
                                progress_bar_height=5,
                                loop=0,
                                mp4=mp4,
                            )
                        except:
                            empty_text.error(
                                "An error occurred while computing the timelapse. You probably requested too much data. Try reducing the ROI or timespan."
                            )

                        empty_text.text(
                            "Right click the GIF to save it to your computer👇"
                        )
                        empty_image.image(out_gif)

                        out_mp4 = out_gif.replace(".gif", ".mp4")
                        if mp4 and os.path.exists(out_mp4):
                            with empty_video:
                                st.text(
                                    "Right click the MP4 to save it to your computer👇"
                                )
                                st.video(out_gif.replace(".gif", ".mp4"))

        elif collection == "MODIS Gap filled Land Surface Temperature Daily":

            with st.form("submit_ts_form"):
                with st.expander("Customize timelapse"):

                    title = st.text_input(
                        "Enter a title to show on the timelapse: ",
                        "Land Surface Temperature",
                    )
                    start_date = st.date_input(
                        "Select the start date:", datetime.date(2018, 1, 1)
                    )
                    end_date = st.date_input(
                        "Select the end date:", datetime.date(2020, 12, 31)
                    )
                    frequency = st.selectbox(
                        "Select a temporal frequency:",
                        ["year", "quarter", "month", "week", "day"],
                        index=2,
                    )
                    reducer = st.selectbox(
                        "Select a reducer for aggregating data:",
                        ["median", "mean", "min", "max", "sum", "variance", "stdDev"],
                        index=0,
                    )

                    speed = st.slider("Frames per second:", 1, 30, 5)
                    add_progress_bar = st.checkbox("Add a progress bar", True)
                    progress_bar_color = st.color_picker(
                        "Progress bar color:", "#0000ff"
                    )
                    font_size = st.slider("Font size:", 10, 50, 30)
                    font_color = st.color_picker("Font color:", "#ffffff")
                    font_type = st.selectbox(
                        "Select the font type for the title:",
                        ["arial.ttf", "alibaba.otf"],
                        index=0,
                    )
                    mp4 = st.checkbox("Save timelapse as MP4", True)

                empty_text = st.empty()
                empty_image = st.empty()
                empty_video = st.container()

                roi = None
                if st.session_state.get("roi") is not None:
                    roi = st.session_state.get("roi")
                out_gif = geemap.temp_file_path(".gif")

                submitted = st.form_submit_button("Submit")
                if submitted:

                    if sample_roi == "Uploaded GeoJSON" and data is None:
                        empty_text.warning(
                            "Steps to create a timelapse: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Alternatively, you can select a sample ROI from the dropdown list."
                        )
                    else:

                        empty_text.text("Computing... Please wait...")
                        try:
                            out_gif = geemap.create_timelapse(
                                st.session_state.get("ee_asset_id"),
                                start_date=start_date.strftime("%Y-%m-%d"),
                                end_date=end_date.strftime("%Y-%m-%d"),
                                region=roi,
                                frequency=frequency,
                                reducer=reducer,
                                date_format=None,
                                out_gif=out_gif,
                                bands=None,
                                palette=st.session_state.get("palette"),
                                vis_params=None,
                                dimensions=768,
                                frames_per_second=speed,
                                crs="EPSG:3857",
                                overlay_data=overlay_data,
                                overlay_color=overlay_color,
                                overlay_width=overlay_width,
                                overlay_opacity=overlay_opacity,
                                title=title,
                                title_xy=("2%", "90%"),
                                add_text=True,
                                text_xy=("2%", "2%"),
                                text_sequence=None,
                                font_type=font_type,
                                font_size=font_size,
                                font_color=font_color,
                                add_progress_bar=add_progress_bar,
                                progress_bar_color=progress_bar_color,
                                progress_bar_height=5,
                                loop=0,
                                mp4=mp4,
                            )
                        except:
                            empty_text.error(
                                "Something went wrong. You probably requested too much data. Try reducing the ROI or timespan."
                            )

                        if out_gif is not None and os.path.exists(out_gif):

                            geemap.reduce_gif_size(out_gif)

                            empty_text.text(
                                "Right click the GIF to save it to your computer👇"
                            )
                            empty_image.image(out_gif)

                            out_mp4 = out_gif.replace(".gif", ".mp4")
                            if mp4 and os.path.exists(out_mp4):
                                with empty_video:
                                    st.text(
                                        "Right click the MP4 to save it to your computer👇"
                                    )
                                    st.video(out_gif.replace(".gif", ".mp4"))

                        else:
                            st.error(
                                "Something went wrong. You probably requested too much data. Try reducing the ROI or timespan."
                            )

        elif collection == "USDA National Agriculture Imagery Program (NAIP)":

            with st.form("submit_naip_form"):
                with st.expander("Customize timelapse"):

                    title = st.text_input(
                        "Enter a title to show on the timelapse: ", "NAIP Timelapse"
                    )

                    years = st.slider(
                        "Start and end year:",
                        2003,
                        today.year,
                        (2003, today.year),
                    )

                    bands = st.selectbox(
                        "Select a band combination:", ["N/R/G", "R/G/B"], index=0
                    )

                    speed = st.slider("Frames per second:", 1, 30, 3)
                    add_progress_bar = st.checkbox("Add a progress bar", True)
                    progress_bar_color = st.color_picker(
                        "Progress bar color:", "#0000ff"
                    )
                    font_size = st.slider("Font size:", 10, 50, 30)
                    font_color = st.color_picker("Font color:", "#ffffff")
                    font_type = st.selectbox(
                        "Select the font type for the title:",
                        ["arial.ttf", "alibaba.otf"],
                        index=0,
                    )
                    mp4 = st.checkbox("Save timelapse as MP4", True)

                empty_text = st.empty()
                empty_image = st.empty()
                empty_video = st.container()
                empty_fire_image = st.empty()

                roi = None
                if st.session_state.get("roi") is not None:
                    roi = st.session_state.get("roi")
                out_gif = geemap.temp_file_path(".gif")

                submitted = st.form_submit_button("Submit")
                if submitted:

                    if sample_roi == "Uploaded GeoJSON" and data is None:
                        empty_text.warning(
                            "Steps to create a timelapse: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Alternatively, you can select a sample ROI from the dropdown list."
                        )
                    else:

                        empty_text.text("Computing... Please wait...")
                        try:
                            geemap.naip_timelapse(
                                roi,
                                years[0],
                                years[1],
                                out_gif,
                                bands=bands.split("/"),
                                palette=st.session_state.get("palette"),
                                vis_params=None,
                                dimensions=768,
                                frames_per_second=speed,
                                crs="EPSG:3857",
                                overlay_data=overlay_data,
                                overlay_color=overlay_color,
                                overlay_width=overlay_width,
                                overlay_opacity=overlay_opacity,
                                title=title,
                                title_xy=("2%", "90%"),
                                add_text=True,
                                text_xy=("2%", "2%"),
                                text_sequence=None,
                                font_type=font_type,
                                font_size=font_size,
                                font_color=font_color,
                                add_progress_bar=add_progress_bar,
                                progress_bar_color=progress_bar_color,
                                progress_bar_height=5,
                                loop=0,
                                mp4=mp4,
                            )
                        except:
                            empty_text.error(
                                "Something went wrong. You either requested too much data or the ROI is outside the U.S."
                            )

                        if out_gif is not None and os.path.exists(out_gif):

                            empty_text.text(
                                "Right click the GIF to save it to your computer👇"
                            )
                            empty_image.image(out_gif)

                            out_mp4 = out_gif.replace(".gif", ".mp4")
                            if mp4 and os.path.exists(out_mp4):
                                with empty_video:
                                    st.text(
                                        "Right click the MP4 to save it to your computer👇"
                                    )
                                    st.video(out_gif.replace(".gif", ".mp4"))

                        else:
                            st.error(
                                "Something went wrong. You either requested too much data or the ROI is outside the U.S."
                            )
    st.markdown('Funcion Timelapse creada por Qiusheng Wu')

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

def download():
    st.title('Descargar datos')

    types = st.selectbox(
    '¿Qué tipo de datos quiere descargar?',
        ('Meteorologicos', 'Hidrologicos')
    )

    if types == 'Meteorologicos':
        path = "/Users/34691/Desktop/TWP/AppTimeLapse/meteo_precip_v2.csv"
        df = pd.read_csv(path)
        col1, col2= st.columns((2))

        with col2:
            start_lat, end_lat = st.slider("Selecciona la latitud:",
                            min_value=round(min(df.Latitude),2),
                            max_value=round(max(df.Latitude),2),
                           value=(max(df.Latitude),min(df.Latitude)))
        with col1:
            start_lon, end_lon = st.slider("Selecciona la longitud:",
                            min_value=round(min(df.Longitude),2),
                            max_value=round(max(df.Longitude),2),
                           value=(max(df.Longitude),min(df.Longitude)))

        filtered = df[(df['Latitude']>=start_lat)&(df['Latitude']<=end_lat)&
                      (df['Longitude']>=start_lon)&(df['Longitude']<=end_lon)]

        csv = convert_df(filtered)

        st.download_button(label='Click para descargar', data=csv, file_name='datos.csv')

        if st.checkbox('Muestra los datos'):
            st.table(filtered)

    if types == 'Hidrologicos':
        path = '/Users/34691/Desktop/TWP/AppTimeLapse/sitios_toma_02.csv'
        df = pd.read_csv(path)

        st_list=list(dict.fromkeys(list(df.Nombre)))

        pois = st.multiselect('Selecciona los sitios toma', st_list)

        filtered = df[df['Nombre'].isin(pois)]

        csv = convert_df(filtered)

        st.download_button(label='Click para descargar', data=csv, file_name='datos.csv')

        if st.checkbox('Muestra los datos'):
            st.table(filtered)


##########################################################################################
#                                  SCRIPT
##########################################################################################

menu = st.sidebar.radio("Menu:", ('General','Meteorologico 01','Meteorologico 02','Meteorologico 03',
                                  'Hidrologico',
                                  'Descargar Datos','TimeLapse'))

if menu == "General":
    general()
if menu == "Meteorologico 01":
    meteo_01()
if menu == "Meteorologico 02":
    meteo_02()
if menu == "Meteorologico 03":
    meteo_03()
#if menu == "Meteorologico 04":
#    meteo_04()
if menu == "Hidrologico":
    hidro_02()
#if menu == "Hidrologico 02":
#    hidro_02()
#if menu == "Hidrologico 03":
#    hidro_03()
#if menu == "Hidrologico 04":
#    hidro_04()
if menu == "Descargar Datos":
    download()
if menu == "TimeLapse":
    timelapse()
