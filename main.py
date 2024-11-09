import requests
import pandas as pd
import streamlit as st
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="News Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .title {
        font-size:50px !important;
        color: #2E86C1;
        text-align: center;
        font-weight: bold;
    }
    .subtitle {
        font-size:24px !important;
        color: #117A65;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and subtitle with emojis
st.markdown('<p class="title">📰 Latest News Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Stay updated with the latest news articles</p>', unsafe_allow_html=True)

# Sidebar for filters
st.sidebar.header('Filter Articles')

# User inputs for filters
category = st.sidebar.selectbox('Select Category', [
    'All', 'Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'
])

from_date = st.sidebar.date_input('From Date', datetime.now().date())
to_date = st.sidebar.date_input('To Date', datetime.now().date())

# Convert dates to strings
from_date_str = from_date.strftime('%Y-%m-%d')
to_date_str = to_date.strftime('%Y-%m-%d')

# NewsAPI endpoint and API key
API_KEY = 'd4d6e979efed43e8a19c52843d465981'  # Replace with your actual API key
url = 'https://newsapi.org/v2/top-headlines'

# Parameters for the API request
params = {
    'apiKey': API_KEY,
    'language': 'en',
    'from': from_date_str,
    'to': to_date_str,
    'pageSize': 100,
}

# Add category to parameters if not 'All'
if category != 'All':
    params['category'] = category.lower()

# Fetch data from NewsAPI
try:
    with st.spinner('Fetching latest news articles...'):
        response = requests.get(url, params=params)
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get('articles', [])
        st.success('Data fetched successfully!')
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# Extract data into a DataFrame
if articles:
    df = pd.DataFrame(articles)
    # Select relevant columns
    df = df[['source', 'author', 'title', 'description', 'publishedAt', 'url', 'urlToImage']]
    # Clean and rename columns
    df['source'] = df['source'].apply(lambda x: x['name'])
    df.rename(columns={
        'source': 'Source',
        'author': 'Author',
        'title': 'Title',
        'description': 'Summary',
        'publishedAt': 'Publication Date',
        'url': 'Article URL',
        'urlToImage': 'Image URL'
    }, inplace=True)
    # Convert publication date to datetime
    df['Publication Date'] = pd.to_datetime(df['Publication Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
else:
    st.warning('No articles found for the selected filters.')
    st.stop()

# Search functionality
search_term = st.sidebar.text_input('Search in Titles')

if search_term:
    df = df[df['Title'].str.contains(search_term, case=False, na=False)]

# Display articles
st.markdown("## 🗞️ News Articles")

for index, row in df.iterrows():
    st.markdown(f"### {row['Title']}")
    st.write(f"*Source:* {row['Source']}")
    st.write(f"*Author:* {row['Author'] if row['Author'] else 'N/A'}")
    st.write(f"*Published At:* {row['Publication Date']}")
    st.write(f"*Summary:* {row['Summary']}")
    if row['Image URL']:
        st.image(row['Image URL'], use_column_width=True)
    st.markdown(f"[Read more]({row['Article URL']})")
    st.markdown("---")