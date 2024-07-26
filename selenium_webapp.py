from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

app = Flask(__name__)

@app.route('/scrape')
def scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Use the pre-installed Chrome on Render
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        
        title = driver.title
        
        # Wait for the language element to be present
        wait = WebDriverWait(driver, 10)
        language_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="SIvCob"]')))
        language = language_element.text
        
        driver.quit()
        
        data = {'Page Title': title, 'Language': language}
        return jsonify(data), 200
    
    except TimeoutException:
        return jsonify({"error": "Timed out waiting for page elements"}), 500
    except WebDriverException as e:
        return jsonify({"error": f"WebDriver error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/')
def home():
    return "Selenium is working"

if __name__ == '__main__':
    app.run(debug=True, port=10000)
