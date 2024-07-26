from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/scrape')
def scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Use the pre-installed Chrome on Render
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        logging.info("WebDriver initialized successfully")
        
        driver.get("https://www.google.com")
        logging.info(f"Page title after loading: {driver.title}")
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logging.info("Body element found, page seems to be loaded")
        
        # Get page source for debugging
        page_source = driver.page_source
        logging.info(f"Page source length: {len(page_source)}")
        
        # Try to find the language element
        try:
            language_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="SIvCob"]'))
            )
            language = language_element.text
            logging.info(f"Language element found: {language}")
        except TimeoutException:
            logging.error("Language element not found. Trying alternative method.")
            # If the specific element is not found, let's get all text from the body
            body_text = driver.find_element(By.TAG_NAME, "body").text
            language = "Language element not found. Body text snippet: " + body_text[:100]
        
        driver.quit()
        
        data = {'Page Title': driver.title, 'Language Info': language}
        return jsonify(data), 200
    
    except WebDriverException as e:
        logging.error(f"WebDriver error: {str(e)}")
        return jsonify({"error": f"WebDriver error: {str(e)}"}), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/')
def home():
    return "Selenium is working"

if __name__ == '__main__':
    app.run(debug=True, port=10000)
