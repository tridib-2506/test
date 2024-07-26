import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# Define a function to scrape the title from Google
def scrape_google_title():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.google.com")
        title = driver.title
    except Exception as e:
        title = f"Error: {str(e)}"
    finally:
        driver.quit()

    return title

# Streamlit UI
st.title("Google Title Scraper")

if st.button("Scrape Google Title"):
    title = scrape_google_title()
    st.write(f"Google Page Title: {title}")
