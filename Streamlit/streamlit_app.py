import folium
import streamlit as st
from streamlit_folium import folium_static
import requests
import pandas as pd


# Read the GeoJSON file
geojson_data_path = "https://raw.githubusercontent.com/Pizzzetti/Public/main/Streamlit/SchaGaDu_v3.json"
geojson_data_path = "https://raw.githubusercontent.com/Pizzzetti/Public/main/Streamlit/SchaGaDu_v5_filtered_add.json"
link_path = f'<a href="https://www.gazzetta.it">Gazzetta</a>'

# Function to get unique values for a specific property in GeoJSON
def get_unique_property_values(geojson_data, property_name):
    if property_name == 'ALL':
        property_name = 'MISTRA_ID'
    unique_values = set()
    for feature in geojson_data['features']:
        feature["properties"]["link"] = link_path
        value = feature['properties'].get(property_name)
        if value is not None:
            unique_values.add(value)
    return sorted(list(unique_values))

# Function to create DataFrame from selected GeoJSON feature properties
def create_dataframe(selected_feature):
    data = {}
    for key, value in selected_feature.items():
        data[key] = [value]
    df = pd.DataFrame(data)
    return df

def get_filtered_GeoJSON(geojson_data_path):
    # Streamlit app
    st.set_page_config(layout='wide')
    st.title('Filter GeoJSON')

    # Read GeoJSON data
    geojson_data = None
    with st.spinner('Loading GeoJSON data...'):
        response = requests.get(geojson_data_path)
        if response.status_code == 200:
            geojson_data = response.json()

    # Sidebar for filter selection
    st.sidebar.subheader('Filter Selection')
    property_vec = ['ALL'] + list(geojson_data['features'][0]['properties'].keys())
    filter_field = st.sidebar.selectbox('Choose a property:', options = property_vec)
    #filter_field = st.multiselect('Choose a property:', options = property_vec)
    property_unique_value = get_unique_property_values(geojson_data, filter_field)
    #filter_value = st.sidebar.selectbox('Choose a value:', options = property_unique_value)
    filter_values = st.multiselect('Choose a value:', options = property_unique_value)


    # Filter GeoJSON features based on selected criteria
    if filter_field == 'ALL' or filter_values == []:
        filtered_geojson = geojson_data
    else:
        filtered_features = []
        for filter_value in filter_values:
            for feature in geojson_data['features']:
                if feature['properties'].get(filter_field) == filter_value:
                    filtered_features.append(feature)
        filtered_geojson = {
            "type": "FeatureCollection",
            "features": filtered_features
        }
    return filtered_geojson,property_vec,property_unique_value

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
        weight_shape = 3

    # Create a custom tooltip with the name of the feature and additional fields
    tooltip_content = '<h5>{}</h5>'.format(feature['properties']['INV_KEY'])  # Initial tooltip content
    tooltip_content += '<p>Field 1: {}</p>'.format(feature['properties']['OBJ_NAME'])  # Additional field 1
    tooltip_content += '<p>Field 2: {}</p>'.format(feature['properties']['KB'])  # Additional field 2
    
    return {
        'fillColor': fill_color,
        'color': border_color,    # Set border color to the same as fill color
        'weight': weight_shape,            # Border weight
        'fillOpacity': 0.5,     # Opacity of the filled area
        'tooltip': tooltip_content,  # Add custom tooltip
        'interactive': True  # Disable interactivity to hide selection rectangle
    }

# Create a Folium map centered at a specific location
height = 900
m = folium.Map(location=[46.29518, 8.04795], zoom_start=14, tiles=None, width='100%', height=height)

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

tooltip = folium.GeoJsonTooltip(
    fields=['INV_KEY', 'OBJ_NAME', 'KB'],
    aliases=['KEY:', 'OBJ:', 'ZK:'],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #FFFFFF;
        border: 1px solid black;
        border-radius: 2px;
        box-shadow: 2px;
    """,
    max_width=800,
)

GeoJsonPopup = folium.GeoJsonPopup(
    fields=["INV_KEY", "OBJ_NAME","link"],
    aliases=["KEY", "OBJ","url"],
    localize=True,
    labels=True,
    style="background-color: yellow;"
)
# Update GeoJsonPopup's HTML content to include clickable link

filtered_geojson,property_vec,property_unique_value = get_filtered_GeoJSON(geojson_data_path)
# Add GeoJSON layer to the map with styled features
geojson_layer = folium.GeoJson(
    filtered_geojson,
    style_function=style_function,
    highlight_function=lambda feature: {
        'fillColor': 'red',  # Change fill color of highlighted feature
        'color': 'red',  # Change border color of highlighted feature
        'weight': 2,  # Adjust border weight of highlighted feature
        'fillOpacity': 0.5,  # Adjust opacity of highlighted feature
    },
    tooltip=tooltip,
    popup=GeoJsonPopup).add_to(m)

# Define custom CSS styles

# Display the Folium map with click event handler
#folium_element = folium.Element(m._repr_html_() + js_click_handler)
folium_element = folium_static(m, width=2000, height=height)
#popup_html = "href=https://example.com/"
#m.add_child(folium.Popup("outline Popup on GeoJSON"))
st.markdown(f'<iframe srcdoc="{m}" style="width: 100%; height: 500px; border: none"></iframe>', unsafe_allow_html=True)




