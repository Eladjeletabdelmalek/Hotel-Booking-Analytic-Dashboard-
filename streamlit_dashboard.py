import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st
import pycountry
from countryinfo import CountryInfo
import plotly.express as px
import plotly.graph_objects as go




st.set_page_config(
    page_title="Hotel booking App",
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

cols=st.columns(4) 

countries=countries.rename(columns={"Latitude": "lat", "Longitude": "lon"})    
#Defining The columns  for the widgets 

# df_countries should have Country_Code (ISO-3) and Count
with st.container(border=True):
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

st.markdown("""
<style>
.card {
  width: 200px;
  height: 150px;
  border-radius: 20px;
  padding: 5px;  /* this creates the border space */
  box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
  background-image: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin: 15px;
}

.card:hover {
  transform: scale(1.05);
  box-shadow: rgba(151, 65, 252, 0.4) 0 25px 40px -5px;
}

/* inner content */
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
  padding: 20px;
}

.card__content h3 {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.card__content p {
  font-size: 0.9rem;
  color: #bfbfbf;
}
</style>
""", unsafe_allow_html=True)


# for col, title, desc in zip(
#     cols,
#     ["Analytics", "Reports", "AI Tools",'new thing'],
#     ["See trends", "Generate insights", "Explore models",'its content']
# ):
#     with col:
#         st.markdown(f"""
#         <div class="card">
#           <div class="card__content">
#             <h3>{title}</h3>
#             <p>{desc}</p>
#           </div>
#         </div>
#         """, unsafe_allow_html=True)

values={
    "Countries":len(df['country'].unique()),
    "Customers":len(df['name'].unique()),
    "Customers1":len(df['name'].unique()),
    "Customers2":len(df['name'].unique())
        }


containers1=[st.container(border=True) for _ in range(4)]
for i, col in enumerate(cols):
    with col:
        with st.container(border=True,height=100):
            st.metric(label="Countries", value=len(df['country'].unique()))
            
    

with st.sidebar:
    selected_column=st.selectbox('Select Columns',df.columns.to_list())

    if pd.api.types.is_numeric_dtype(df[selected_column]):
        value=st.slider(f'the {selected_column}number' ,df[selected_column].min(),df[selected_column].max())
        
        
    if pd.api.types.is_string_dtype(df[selected_column]) :
        selected_value=st.selectbox('Value',df[selected_column].unique())   


 
 
 
 
 

fig1=px.line(data_frame=df,y='stays_in_week_nights',x='adults',color='is_canceled')    
fig2=px.bar(data_frame=df,x='market_segment',y='lead_time',color='is_canceled')
fig3=go.Figure(data=[go.Pie(labels=df['customer_type'].unique(), values=df['customer_type'].value_counts(), hole=.3)])

cols2=st.columns(3)
with cols2[0]:
    with st.container(border=True):
        st.plotly_chart(fig1)
with cols2[1]:
    with st.container(border=True):
        #st.bar_chart(data=df,x='market_segment',y='lead_time',color='is_canceled')
        st.plotly_chart(fig2)    
with cols2[2]:
    with st.container(border=True): 
        st.plotly_chart(fig3)    
    




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