import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st
import pycountry
from countryinfo import CountryInfo
import plotly.express as px


st.set_page_config(
    page_title="Full Width App",
    layout="wide"   
)

st.title('Hotel booking dashboard')
file='hotel_booking.csv'
countries_file='countries_loc.csv'
if file is not None :
    df= pd.read_csv(file)
else:
    st.write('File not found') 
       
if countries_file is not None :
    countries=pd.read_csv(countries_file)
else:
    st.write('Countries  file  not found')     




with st.sidebar:
    selected_column=st.selectbox('Select Columns',df.columns.to_list())

    if pd.api.types.is_numeric_dtype(df[selected_column]):
        value=st.slider(f'the {selected_column}number' ,df[selected_column].min(),df[selected_column].max())
        
        
    if pd.api.types.is_string_dtype(df[selected_column]) :
        selected_value=st.selectbox('Value',df[selected_column].values)   


 
 
 
 
 
countries=countries.rename(columns={"Latitude": "lat", "Longitude": "lon"})    
#Defining The columns  for the widgets 
cols=st.columns(3) 
with cols[0]:
    st.bar_chart(data=df,x='market_segment',y='lead_time',color='is_canceled')



# st.subheader('data summary')
# st.write(df.describe()) 
# st.map(data=countries,latitude="lat",
#     longitude="lon",
#     size="Count")


# df_countries should have Country_Code (ISO-3) and Count
fig = px.choropleth(
    countries,
    locations="Country_Code",         # ISO-3 country codes (FRA, USA, DZA, etc.)
    color="Count",                    # what determines color intensity
    hover_name="Country_Code",        # tooltip info
    color_continuous_scale=[
        (0.0, "lightblue"),   # low values
        (0.5, "blue"),      # mid values
        (1.0, "darkblue")          # high values
    ], # try "Plasma", "Cividis", "Turbo", etc.
    projection="natural earth",       # world projection
    title="🌍 Country Distribution by Count",
)

# Optional: Customize the layout
fig.update_layout(
    template="plotly_dark",
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    margin=dict(l=0, r=0, t=30, b=0),
    height=500
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)




# st.subheader('data checking')
col=df.columns.tolist()
# sel_col=st.selectbox('select column',col)
# unique_values=df[sel_col].unique() 
# st.write(unique_values)
# selected_v=st.selectbox('select a value',unique_values)
# f_df=df[df[sel_col]==selected_v]
# st.write(f_df)
st.subheader('The countries')
st.write(df['country'].value_counts())
st.subheader('data visualization')
x=st.selectbox('select x_column',col)
y=st.selectbox('select y_column',col)

if st.button('generate'):
    st.line_chart(df.set_index(x)[y])
    
else:
    st.write('Please , select any column ')    