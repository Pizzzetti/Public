import streamlit as st
from streamlit_folium import folium_static
import folium

# Define a Streamlit column layout with a responsive width
st.set_page_config(layout="wide")

col1,col2 = st.columns(2)

col1.header('Sinistra')
col2.header('Destra')
col2.container()
# Create a Folium map
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)
folium.Marker(location=[51.5074, -0.1278], popup="London").add_to(m)
folium.Marker(location=[48.8566, 2.3522], popup="Paris").add_to(m)
folium.Marker(location=[40.7128, -74.0060], popup="New York").add_to(m)
folium.Marker(location=[34.0522, -118.2437], popup="Los Angeles").add_to(m)

# Render the Folium map inside the container
with col2:
    fs = folium_static(m)
    #st.write(fs)

    #col2.write(fs)
    # Add some content below the map
col1.write("Some content below the map.")
