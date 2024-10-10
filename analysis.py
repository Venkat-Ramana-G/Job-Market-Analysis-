import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def load_data(filename='job_listings.csv'):
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        st.error(f"Error: {filename} not found.")
        return pd.DataFrame()

def analyze_jobs(df):
    if df.empty:
        st.error("No data available for analysis.")
        return

    # Basic statistics
    st.subheader("Job Data Statistics")
    st.write(df.describe())

    # Plot: Jobs per Company
    st.subheader("Top 10 Companies Posting Jobs")
    top_companies = df['Company'].value_counts().head(10)
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    top_companies.plot(kind='bar', color='skyblue', ax=ax1)
    plt.title('Top 10 Companies Posting Jobs')
    plt.xlabel('Company')
    plt.ylabel('Number of Jobs')
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # Plot: Jobs per Location
    st.subheader("Top 10 Job Locations")
    top_locations = df['Location'].value_counts().head(10)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    top_locations.plot(kind='bar', color='lightgreen', ax=ax2)
    plt.title('Top 10 Job Locations')
    plt.xlabel('Location')
    plt.ylabel('Number of Jobs')
    plt.xticks(rotation=45)
    st.pyplot(fig2)

if __name__ == "__main__":
    df = load_data()
    analyze_jobs(df)
