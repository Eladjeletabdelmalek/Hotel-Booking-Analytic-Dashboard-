import pydeck as pdk
import streamlit as st
import pandas as pd
df=pd.read_csv('countries_loc.csv')
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
    get_radius=200000,
    get_fill_color='[255, 140, 0]',
    pickable=True
)

view = pdk.ViewState(latitude=0, longitude=0, zoom=1)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/dark-v10"
)

st.pydeck_chart(deck)
