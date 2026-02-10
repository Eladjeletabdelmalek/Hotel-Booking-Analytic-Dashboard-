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



st.markdown("""
<style>
.card {
  width: 100%;
  max-width: 220px;
  height: 150px;
  border-radius: 20px;
  padding: 5px;
  box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
  background-image: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin: 15px auto;
}

.card:hover {
  transform: scale(1.05);
  box-shadow: rgba(151, 65, 252, 0.4) 0 25px 40px -5px;
}

.card__content {
  background: rgb(5, 6, 45);
  border-radius: 17px;
  width: 100%;
  height: 100%;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  padding: 10px;
}

.card__content h3 {
  font-size: 1.2rem;
  margin: 0;
  font-weight: 500;
  display: flex;
  align-items: center; /* vertically center icon with text */
  justify-content: center; /* center horizontally */
  gap: 8px; /* space between label and icon */
}

.card__content h2 {
  font-size: 2rem;
}

.card__content p {
  font-size: 0.9rem;
  color: #bfbfbf;
}
</style>
""", unsafe_allow_html=True)

# st.markdown("""
# <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
# """, unsafe_allow_html=True)
