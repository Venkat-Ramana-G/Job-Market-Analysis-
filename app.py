import streamlit as st
import pandas as pd
from scraper import scrape_remoteok_jobs, save_to_csv
from analysis import analyze_jobs, load_data

# Add copyright notice
st.markdown("<h1 style='text-align: center;'>Job Market Analysis Web Scraper</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>&copy; 2024 done by 24MAI0070 PRIYA RAI</p>", unsafe_allow_html=True)

# Inputs
job_title = st.text_input("Enter job title (e.g., data-scientist):", "data-scientist")
num_pages = st.number_input("Number of pages to scrape:", min_value=1, max_value=5, value=1)

# Scrape jobs
if st.button("Scrape Jobs"):
    with st.spinner(f"Scraping {job_title} jobs..."):
        jobs_df = scrape_remoteok_jobs(job_title, num_pages)
        if not jobs_df.empty:
            save_to_csv(jobs_df)
            st.success(f"Scraped {len(jobs_df)} job listings and saved to job_listings.csv!")
            st.dataframe(jobs_df)
        else:
            st.error("No job listings found.")

# Analyze jobs
if st.button("Analyze Jobs"):
    with st.spinner("Analyzing job data..."):
        df = load_data()
        if not df.empty:
            analyze_jobs(df)
        else:
            st.error("No job data available. Please scrape jobs first.")

st.write("Note: Only a few pages are scraped to avoid overloading the website.")
