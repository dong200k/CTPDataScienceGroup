import streamlit as st
from PIL import Image

ctp_logo = Image.open("images/ctp icon.png")
st.set_page_config(
    page_icon=ctp_logo,
    layout="wide"
)

# Create a page header
st.header("Dataset")

col1,col2=st.columns(2)
with col1:
    image = Image.open('images/BA_DS.webp')
    st.image(image, caption='BA vs DS')

with col2:
    image = Image.open('images/DS_DA.jpeg')
    st.image(image, caption='DS vs DA')

st.markdown('''
The **purpose** of this project is:
1. to understand the current job market for data science
1. to understand the difference between DS, DA, and BA
1. to potentially land a role as a full time data scientist
The **web application** would allow you to:
* visualize data science salaries based on locations and sectors
* predict the role based on job descriptions
''')