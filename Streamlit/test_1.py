import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import json

# Sample GeoJSON data
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
            },
            "properties": {"name": "Polygon 1", "area": 100}
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]]
            },
            "properties": {"name": "Polygon 2", "area": 200}
        }
    ]
}

# Streamlit code
st.title("Click on a Polygon")

# Display the Streamlit table
table_placeholder = st.empty()

# Display the Folium map
folium_map = folium.Map(location=[0.5, 0.5], zoom_start=6)

folium.GeoJson(
    geojson_data,
    tooltip=folium.GeoJsonTooltip(fields=['name', 'area'], labels=True),
    ).add_to(folium_map)

# JavaScript function to handle click event and send data back to Streamlit
click_handler_js = """
    <script>
        function handle_click(e) {
            var props = e.target.feature.properties;
            var props_json = JSON.stringify(props);
            // Send JSON data back to Streamlit
            const jsonString = JSON.stringify({ clicked_feature: props_json });
            const event = new Event('submit', { bubbles: true });
            event.formData = new FormData();
            event.formData.append('data', jsonString);
            document.dispatchEvent(event);
        }
        document.getElementById('mapid').on('click', handle_click);
    </script>
"""

st.write(folium_map._repr_html_() + click_handler_js, unsafe_allow_html=True)

# Receive clicked feature properties from JavaScript and display in Streamlit table
if 'clicked_feature' in st.session_state:
    clicked_feature_json = st.session_state['clicked_feature']
    clicked_feature = json.loads(clicked_feature_json)
    table_placeholder.table(pd.DataFrame(clicked_feature.items(), columns=['Property', 'Value']))
