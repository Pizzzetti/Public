import streamlit as st
from streamlit_folium import folium_static
import folium

# Create two columns
col1, col2 = st.columns(2)

# Create a Folium map
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)
folium.Marker(location=[51.5074, -0.1278], popup="London").add_to(m)
folium.Marker(location=[48.8566, 2.3522], popup="Paris").add_to(m)
folium.Marker(location=[40.7128, -74.0060], popup="New York").add_to(m)
folium.Marker(location=[34.0522, -118.2437], popup="Los Angeles").add_to(m)

# Add elements to the first column
with col1:
    st.header("Column 1")
    folium_static(m)

# Add elements to the second column
with col2:
    st.header("Column 2")
    st.write("This is column 2 content.")
