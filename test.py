from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/')
def home():
    return "Selenium is working"

@app.route('/scrape')
def scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Path to Chrome on Render

    service = Service("/usr/bin/chromedriver")  # Path to ChromeDriver on Render

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.google.com")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        title = driver.title
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        driver.quit()

    return jsonify({"title": title})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
