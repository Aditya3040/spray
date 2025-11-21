# app.py
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

BACKEND_URL = "http://localhost:8001"  # change when using mobile phone

st.set_page_config(layout="wide", page_title="Vineyard Spray Tracker")

st.title("🍇 Vineyard Spray Tracking System")

# ----------------------------------------------------------
# Select Farm Plot
# ----------------------------------------------------------
plot_name = st.selectbox("Select Plot", ["My Vineyard"])
st.write("Selected:", plot_name)

# ----------------------------------------------------------
# Buttons for spraying session
# ----------------------------------------------------------
col1, col2 = st.columns(2)

if col1.button("Start Spraying Session"):
    st.success("Session Started! Use your phone to send GPS.")

if col2.button("Stop Session"):
    st.warning("Session stopped.")

st.markdown("---")

# ----------------------------------------------------------
# Map Display (Static rows + dynamic spray color)
# ----------------------------------------------------------
# Get latest rows from backend
try:
    res = requests.get(BACKEND_URL + "/rows")
except:
    res = None

# Since backend doesn't have /rows API in this minimal version, use sample below:
rows_data = [
    {"row_index": 1, "coords": [(18.5204, 73.8567), (18.5208, 73.8567)], "sprayed": False},
    {"row_index": 2, "coords": [(18.5204, 73.8569), (18.5208, 73.8569)], "sprayed": False},
    {"row_index": 3, "coords": [(18.5204, 73.8571), (18.5208, 73.8571)], "sprayed": False}
]

# Create map
m = folium.Map(location=(18.5206, 73.8569), zoom_start=18)

for row in rows_data:
    color = "green" if row["sprayed"] else "red"
    folium.PolyLine(row["coords"], color=color, weight=6).add_to(m)

st_folium(m, width=900, height=550)

st.markdown("---")
st.subheader("📍 Mobile GPS Sender Page")

st.write("""
Open this link on your mobile phone browser:  
### 👉 `http://<your-laptop-ip>:8501/mobile`
""")

# ----------------------------------------------------------
# Mobile Page Rendering
# ----------------------------------------------------------
page = st.experimental_get_query_params().get("page", ["main"])[0]

if page == "mobile":
    st.header("Send GPS Location")

    st.write("Click the button to send your current GPS coordinates to backend.")

    if st.button("Send GPS"):
        st.markdown("""
        <script>
        navigator.geolocation.getCurrentPosition(function(pos) {
            fetch("http://localhost:8001/update_location", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude
                })
            }).then(r => r.json())
            .then(data => alert("GPS sent: " + JSON.stringify(data)))
            .catch(err => alert("Error: " + err));
        });
        </script>
        """, unsafe_allow_html=True)
