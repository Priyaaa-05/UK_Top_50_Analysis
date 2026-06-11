import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. SETUP & DATA CLEANING
df = pd.read_csv('data/artist_level.csv', encoding='latin1')
df.columns = df.columns.str.strip().str.lower() # Standardize column names

# Create all necessary columns for the 5 problems
df['is_collaboration'] = df['artist_name'].str.contains(',|feat|&', case=False, na=False)
# Add your origin logic here...
uk_artists = ['central cee', 'raye', 'dave', 'coldplay', 'fred again..'] # Add your full list
df['origin'] = df['artist_name'].apply(lambda x: 'UK' if x.lower() in [a.lower() for a in uk_artists] else 'International')
# Ensure 'is_explicit' and 'total_tracks' exist in your CSV

st.title("🎵 UK Music Market Insights Dashboard")

# 2. DEFINE THE 5 CHARTS
# Problem 1: Artist Dominance (HHI)
st.subheader("1. Artist Market Dominance (HHI)")
# (Add your HHI calculation logic here)
st.write("Visualizing the concentration of artist popularity.")

# Problem 2: Localization
st.subheader("2. UK vs. International Performance")
fig2, ax2 = plt.subplots()
df.groupby('origin')['popularity'].sum().plot.pie(ax=ax2, autopct='%1.1f%%')
st.pyplot(fig2)

# Problem 3: Collaboration Impact
st.subheader("3. Impact of Collaborations")
fig3, ax3 = plt.subplots()
sns.barplot(x='is_collaboration', y='popularity', data=df, ax=ax3)
st.pyplot(fig3)

# Problem 4: Explicit Content
st.subheader("4. Explicit vs. Clean Content")
fig4, ax4 = plt.subplots()
sns.boxplot(x='is_explicit', y='popularity', data=df, ax=ax4)
st.pyplot(fig4)

# Problem 5: Album Structure
st.subheader("5. Album Structure vs. Success")
fig5, ax5 = plt.subplots()
sns.regplot(x='total_tracks', y='popularity', data=df, ax=ax5)
st.pyplot(fig5)

# --- SIDEBAR INTERACTIVITY ---
st.sidebar.header("Dashboard Controls")

# Multi-select for Origin
selected_origins = st.sidebar.multiselect("Filter by Origin:", df['origin'].unique(), default=df['origin'].unique())

# Slider for Track Count
min_tracks, max_tracks = st.sidebar.slider("Track Count Range:", 0, int(df['total_tracks'].max()), (0, int(df['total_tracks'].max())))

# Apply Filters
filtered_df = df[
    (df['origin'].isin(selected_origins)) & 
    (df['total_tracks'].between(min_tracks, max_tracks))
]

# --- NOW RENDER CHARTS USING filtered_df ---
# Example:
fig3, ax3 = plt.subplots()
sns.barplot(x='is_collaboration', y='popularity', data=filtered_df, ax=ax3)
st.pyplot(fig3)

if 'counter' not in st.session_state:
    st.session_state.counter = 0

# A button that triggers a persistent action
if st.button("Refresh Data"):
    st.session_state.counter += 1
    st.write(f"Refreshed {st.session_state.counter} times")

    if filtered_df.empty:
        st.warning("No data matches your current filter selection.")
    else:
        ("Render your charts here")

# Streamlit Dashboard
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="UK Top 50 Market Analysis", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Replace 'uk_top_50.csv' with your actual filename
    try:
        df = pd.read_csv('data/artist_level.csv', encoding='latin1')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure 'uk_top_50.csv' is in the project folder.")
        return None

df = load_data()

if df is not None:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Dashboard Filters")
    date_range = st.sidebar.date_input("Date Range", [df['date'].min(), df['date'].max()])
    artist_filter = st.sidebar.multiselect("Select Artists", options=df['artist_name'].unique())
    album_filter = st.sidebar.multiselect("Album Type", options=df['album_type'].unique())
    collab_toggle = st.sidebar.radio("Solo vs Collaboration", ["All", "Solo", "Collaboration"])

    # Apply Filters
    filtered_df = df[(df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])]
    if artist_filter:
        filtered_df = filtered_df[filtered_df['artist_name'].isin(artist_filter)]
    if album_filter:
        filtered_df = filtered_df[filtered_df['album_type'].isin(album_filter)]
    
    # Simple Collaboration Logic: assuming comma in name indicates collaboration
    if collab_toggle == "Solo":
        filtered_df = filtered_df[~filtered_df['artist_name'].str.contains(',')]
    elif collab_toggle == "Collaboration":
        filtered_df = filtered_df[filtered_df['artist_name'].str.contains(',')]

    # --- MAIN DASHBOARD ---
    st.title("📊 UK Top 50 Playlist Analytics")

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Unique Artists", filtered_df['artist_name'].nunique())
    col2.metric("Avg Popularity", round(filtered_df['popularity'].mean(), 2))
    col3.metric("Explicit Content", f"{round((filtered_df['is_explicit'].sum() / len(filtered_df)) * 100, 1)}%")

    # Tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["Dominance & Diversity", "Content Analysis", "Structure & Duration"])

    with tab1:
        st.subheader("Artist Dominance Leaderboard")
        artist_counts = filtered_df['artist_name'].value_counts().reset_index().head(10)
        fig = px.bar(artist_counts, x='artist_name', y='count', title="Top 10 Artists")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Explicit vs Clean Content")
        fig2 = px.pie(filtered_df, names='is_explicit', title="Explicit Content Share")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Album Structure & Duration")
        colA, colB = st.columns(2)
        with colA:
            fig3 = px.histogram(filtered_df, x='album_type', title="Album Type Distribution")
            st.plotly_chart(fig3, use_container_width=True)
        with colB:
            fig4 = px.box(filtered_df, x='album_type', y='duration_ms', title="Track Duration by Album Type")
            st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("Upload your dataset to begin analysis.")