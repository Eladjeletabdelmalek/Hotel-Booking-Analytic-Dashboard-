import pandas as pd  
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Hotel booking App",
    layout="wide"   
)

st.title('Hotel booking dashboard')
file='hotel_booking_cleaned.csv'
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
with st.sidebar:
    selected_column=st.selectbox('Select Columns',df.columns.to_list())

    if pd.api.types.is_numeric_dtype(df[selected_column]):
        value=st.slider(f'the {selected_column}number' ,df[selected_column].min(),df[selected_column].max())
        
        
    if pd.api.types.is_string_dtype(df[selected_column]) :
        selected_value=st.selectbox('Value',df[selected_column].unique())   

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

containers1=[st.container(border=True) for _ in range(4)]
with cols[0]:
    with st.container(border=True,height=100):
        st.metric(label="Countries", value=len(df['country'].unique()))
with cols[1]:
    with st.container(border=True,height=100):
        st.metric(label="Customers", value=len(df))
with cols[2]:
    with st.container(border=True,height=100):
        st.metric(label="Resort Hotels", value=df['hotel'].value_counts()[0])
with cols[3]:
    with st.container(border=True,height=100):
        st.metric(label="City Hotels", value=df['hotel'].value_counts()[1])               
    

fig1=px.sunburst(data_frame=df,path=['hotel','customer_type','meal'],values='total_nights', title="Total revenue over nights by hotel type")  

fig2=px.bar(data_frame=df,x='market_segment',y='lead_time',color='is_canceled')
fig3=go.Figure(data=[go.Pie(labels=df['customer_type'].unique(),values=df['customer_type'].value_counts(), hole=.3)])
fig4=px.bar(data_frame=df,y='adr',x='arrival_date_month',color='hotel',barmode='group',labels={'x':'month','y':'average daily rate'},)
fig5=px.bar(data_frame=df,x='season',color='hotel')
fig6=px.histogram(data_frame=df,x='lead_time',color='is_canceled')


df["arrival_date"] = pd.to_datetime(df["arrival_date"])
df["day_of_year"] = df["arrival_date"].dt.day_of_year

daily_counts = (
    df.groupby(["day_of_year", "hotel"])
      .size()
      .reset_index(name="count")
)

fig7 = px.scatter(
    daily_counts,
    x="day_of_year",
    y="count",
    color="hotel",
    labels={
        "day_of_year": "Day of Year",
        "count": "Number of Reservations",
        "hotel": "Hotel Type"
    },
    title="Daily Hotel Arrivals Throughout the Year"
)
df_polar = (
    df.groupby(['hotel', 'customer_type'], as_index=False)
      .agg(total_revenue=('total_revenue', 'sum'))
)
fig8=px.line_polar(data_frame=df_polar,r='total_revenue',
                   theta='customer_type',color='hotel',line_close=True,
                   title='Total revenue by customer type and hotel',
                   template="plotly_dark",
                   )
fig9=px.scatter(data_frame=df,x='adr',y='lead_time',size='total_nights',color='hotel',title='Lead time vs Average Daily Rate')

#fig7=px.scatter(x=df['arrival_date'].dt.day_of_year.value_counts(),color=df['hotel'])
cols2=st.columns(3)
with cols2[0]:
    with st.container(border=True):
        st.plotly_chart(fig8,key="fig8")
with cols2[1]:
    with st.container(border=True):
        #st.bar_chart(data=df,x='market_segment',y='lead_time',color='is_canceled')
        st.plotly_chart(fig4,key="fig4")    
with cols2[2]:
    with st.container(border=True): 
        st.plotly_chart(fig5,key="fig5")    


cols3=st.columns(1)
with cols3[0]:
    with st.container(border=True):
        st.plotly_chart(fig6,key="fig6")
cols5=st.columns(2)
with cols5[0]:
    with st.container(border=True):
        st.plotly_chart(fig1,key="fig1")
with cols5[1]:
    with st.container(border=True):
        st.plotly_chart(fig9,key="fig9")            
cols4=st.columns(1)
with cols4[0]:
    with st.container(border=True):
        st.plotly_chart(fig7,key="fig7") 
                     
        
# cols6=st.columns(1)
# with cols6[0]:
#     with st.container(border=True):
#         st.plotly_chart(fig1)         
               


# st.subheader('data checking')
col=df.columns.tolist()
st.subheader('The countries')
st.write(df['country'].value_counts())

# st.subheader('data visualization')
# x=st.selectbox('select x_column',col)
# y=st.selectbox('select y_column',col)

# if st.button('generate'):
#     st.line_chart(df.set_index(x)[y])
    
# else:
#     st.write('Please , select any column ')    