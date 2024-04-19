import folium
import streamlit as st
from streamlit_folium import folium_static
import requests


# Read the GeoJSON file
#geojson_data_path = "C:/Users/luca.pizzetti/OneDrive - Engineering Group SA/_WORKING_PROGRESS/PRJ-100880_A9_SchaGaDu - General/GIS/geojson/SchaGaDu_v3.json"
geojson_data_path = "https://raw.githubusercontent.com/Pizzzetti/Public/main/Streamlit/SchaGaDu_v3.json"

# Function to get unique values for a specific property in GeoJSON
def get_unique_property_values(geojson_data, property_name):
    unique_values = set()
    for feature in geojson_data['features']:
        value = feature['properties'].get(property_name)
        if value is not None:
            unique_values.add(value)
    return sorted(list(unique_values))

# Streamlit app
st.set_page_config(layout = 'wide')

st.title('Filter GeoJSON')

# Read GeoJSON data
geojson_data = None
with st.spinner('Loading GeoJSON data...'):
    response = requests.get(geojson_data_path)
    if response.status_code == 200:
        geojson_data = response.json()

# Sidebar for filter selection
with st.sidebar:
    st.subheader('Filter Selection')
    filter_field = st.selectbox('Choose a property:', options=list(['ALL'] +list(geojson_data['features'][0]['properties'].keys())))
    filter_value = st.selectbox('Choose a value:', options=get_unique_property_values(geojson_data, filter_field))

# Filter GeoJSON features based on selected criteria
if filter_field == 'ALL':
    filtered_geojson = geojson_data
else:
    filtered_features = []
    for feature in geojson_data['features']:
        if feature['properties'].get(filter_field) == filter_value:
            filtered_features.append(feature)
    filtered_geojson = {
        "type": "FeatureCollection",
        "features": filtered_features
    }

# Create a Folium map centered at a specific location
m = folium.Map(location=[46.29518, 8.04795], zoom_start=14, tiles=None, width='100%')

# Define a function to map "KB" values to RGB colors
def color_by_kb(kb_value):
    kb_value = int(kb_value)
    if kb_value == 1:
        return '#46c846'  # Green (70, 200, 70)
    elif kb_value == 2:
        return '#e6e61e'  # Yellow (200, 230, 30)
    elif kb_value == 3:
        return '#ffff00'  # Yellow (255, 255, 0)
    elif kb_value == 4:
        return '#ff9900'  # Orange (255, 153, 0)
    elif kb_value == 5:
        return '#ff0000'  # Red (255, 0, 0)
    else:
        return '#808080'  # Gray for other values
    
# Function to style the GeoJSON features based on the "KB" property
def style_function(feature):
    kb_value = feature['properties']['KB']
    fill_color = color_by_kb(kb_value)
    
    # Check if the geometry type is Polygon
    if feature['geometry']['type'] == 'Polygon' or feature['geometry']['type'] == 'MultiPolygon':
        border_color = '#000000'  # Set border color to black for polygons
        weight_shape = 0.5
    else:
        border_color = fill_color  # Set border color to fill color for other geometries
        weight_shape = 2

    # Create a custom tooltip with the name of the feature and additional fields
    tooltip_content = '<h5>{}</h5>'.format(feature['properties']['INV_KEY'])  # Initial tooltip content
    tooltip_content += '<p>Field 1: {}</p>'.format(feature['properties']['OBJ_NAME'])  # Additional field 1
    tooltip_content += '<p>Field 2: {}</p>'.format(feature['properties']['KB'])  # Additional field 2
    
    return {
        'fillColor': fill_color,
        'color': border_color,    # Set border color to the same as fill color
        'weight': weight_shape,            # Border weight
        'fillOpacity': 0.5,     # Opacity of the filled area
        'tooltip': tooltip_content  # Add custom tooltip
    }

wms_url = 'https://wms.geo.admin.ch/'
wms_layer = folium.raster_layers.WmsTileLayer(
    url=wms_url,
    name='swiss_wms',
    layers='ch.swisstopo.landeskarte-grau-10',
    fmt='image/jpeg',
    transparent=True,
    opacity=0.5  # Set opacity to 50%
)
wms_layer.add_to(m)

# Filter GeoJSON features based on selected criteria
filtered_features = []
for feature in geojson_data['features']:
    if feature['properties'].get(filter_field) == filter_value:
        filtered_features.append(feature)

# Add GeoJSON layer to the map with styled features and custom tooltip
folium.GeoJson(
    filtered_geojson,
    style_function=style_function,
    highlight_function=lambda x: {
        'fillOpacity':1
    },
    tooltip=folium.features.GeoJsonTooltip(
        fields=['INV_KEY', 'OBJ_NAME', 'KB'],  # Add more fields here
        aliases=['KEY:', 'OBJ:', 'ZK:'],  # Add aliases for the fields
    ),
).add_to(m)

# Display Folium map using Streamlit
folium_static(m,width=1000, height=500)   