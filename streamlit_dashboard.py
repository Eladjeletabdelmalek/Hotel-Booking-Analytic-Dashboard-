import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st

st.set_page_config(
    page_title="Full Width App",
    layout="wide"   # 👈 this makes it full width
)

st.title('Hotel booking dashboard')
file='hotel_booking.csv'
if file is not None :
    df= pd.read_csv(file)
    
    
#Defining The columns  for the widgets 
cols=st.columns(3) 
with cols[0]:
    st.bar_chart(data=df,x='market_segment',y='lead_time',color='is_canceled')

st.subheader('data summary')
st.write(df.describe()) 
st.subheader('data checking')
col=df.columns.tolist()
sel_col=st.selectbox('select column',col)
unique_values=df[sel_col].unique() 
st.write(unique_values)
selected_v=st.selectbox('select a value',unique_values)
f_df=df[df[sel_col]==selected_v]
st.write(f_df)
st.subheader('data visualization')
x=st.selectbox('select x_column',col)
y=st.selectbox('select y_column',col)

if st.button('generate'):
    st.line_chart(f_df.set_index(x)[y])
    
else:
    st.write('Please , select any column ')    