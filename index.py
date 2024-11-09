import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import time

# Set page configuration
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌦️",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .title {
        font-size:50px !important;
        color: #1F77B4;
        text-align: center;
        font-weight: bold;
    }
    .subtitle {
        font-size:24px !important;
        color: #FF7F0E;
        text-align: center;
    }
    .dataframe {
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and subtitle with emojis
st.markdown('<p class="title">🌤️ Weather Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time Weather Data for Multiple Cities</p>', unsafe_allow_html=True)

# Simulated HTML content (for demonstration purposes)
html_content = '''
<div class="city-weather">
    <h2>New York</h2>
    <span class="temp">22°C</span>
    <span class="condition">Sunny</span>
</div>
<div class="city-weather">
    <h2>London</h2>
    <span class="temp">18°C</span>
    <span class="condition">Cloudy</span>
</div>
<div class="city-weather">
    <h2>Tokyo</h2>
    <span class="temp">25°C</span>
    <span class="condition">Rainy</span>
</div>
<div class="city-weather">
    <h2>Sydney</h2>
    <span class="temp">20°C</span>
    <span class="condition">Windy</span>
</div>
<div class="city-weather">
    <h2>Mumbai</h2>
    <span class="temp">30°C</span>
    <span class="condition">Humid</span>
</div>
<div class="city-weather">
    <h2>Cairo</h2>
    <span class="temp">28°C</span>
    <span class="condition">Sunny</span>
</div>
<div class="city-weather">
    <h2>Moscow</h2>
    <span class="temp">15°C</span>
    <span class="condition">Snowy</span>
</div>
<div class="city-weather">
    <h2>Paris</h2>
    <span class="temp">19°C</span>
    <span class="condition">Clear</span>
</div>
<div class="city-weather">
    <h2>São Paulo</h2>
    <span class="temp">26°C</span>
    <span class="condition">Thunderstorms</span>
</div>
<div class="city-weather">
    <h2>Toronto</h2>
    <span class="temp">17°C</span>
    <span class="condition">Foggy</span>
</div>
'''

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

cities = []
temperatures = []
conditions = []

# Extract data from the HTML
for city_div in soup.find_all('div', class_='city-weather'):
    city_name = city_div.find('h2').text.strip()
    temperature = city_div.find('span', class_='temp').text.strip()
    condition = city_div.find('span', class_='condition').text.strip()
    cities.append(city_name)
    temperatures.append(float(temperature.replace('°C', '')))
    conditions.append(condition)

# Create a pandas DataFrame with the collected data
data = pd.DataFrame({
    'City': cities,
    'Temperature (°C)': temperatures,
    'Condition': conditions
})

# Simulate loading animation
with st.spinner('Loading weather data...'):
    time.sleep(2)  # Simulate a delay in loading data
st.success('Data loaded successfully!')

# Search Functionality
search_city = st.text_input('🔎 Search for a city')
if search_city:
    filtered_data = data[data['City'].str.contains(search_city, case=False)]
else:
    filtered_data = data

# Sort Functionality
sort_by_temp = st.checkbox('🌡️ Sort by Temperature')
if sort_by_temp:
    filtered_data = filtered_data.sort_values(by='Temperature (°C)', ascending=False)

# Reset index for display purposes
filtered_data.reset_index(drop=True, inplace=True)

# Display the DataFrame with some styling
st.markdown("## 📋 Weather Data")
st.table(filtered_data.style.set_properties(**{
    'background-color': '#F9F9F9',
    'border-color': 'black',
    'color': 'black'
}))

# Animated footer
st.markdown("""
    <div style='text-align: center; padding-top: 50px;'>
        <lottie-player src="https://assets7.lottiefiles.com/packages/lf20_jtbfg2nb.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px; margin: 0 auto;"  loop  autoplay></lottie-player>
    </div>
    """, unsafe_allow_html=True)

# Include the LottieFiles script
st.markdown("""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    """, unsafe_allow_html=True)