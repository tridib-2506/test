from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Selenium is working"

@app.route('/scrape')
def scrape():
    chrome_options = Options()
    options.binary_location = '/opt/headless-chromium'
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome('/opt/chromedriver', service=service, options=chrome_options)

    try:
        driver.get("https://www.google.com")
        title = driver.title
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        driver.quit()

    return jsonify({"title": title})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
