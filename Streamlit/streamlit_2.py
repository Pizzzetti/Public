import folium

# Create a map object
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

# Define a function to be called on tooltip click
def on_tooltip_click(feature, layer):
    print("Tooltip clicked!")
    # You can perform any action here when the tooltip is clicked

# Create a GeoJson layer
geojson = {
    "type": "Feature",
    "properties": {"name": "London"},
    "geometry": {
        "type": "Point",
        "coordinates": [-0.1278, 51.5074]
    }
}

# Add GeoJson layer to the map
folium.GeoJson(
    geojson,
    tooltip="Click me!",
    popup="<b>Hello, London!</b>",
    style_function=lambda x: {'color': 'blue'}
).add_to(m)

# Add a custom JavaScript code to handle tooltip click event
m.add_child(folium.features.ClickForMarker(popup="Waypoint"))

# Save the map to an HTML file
m.save("map.html")
