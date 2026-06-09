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