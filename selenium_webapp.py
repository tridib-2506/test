from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route('/scrape')
def scrape():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.google.com")
    title = driver.title
    language = driver.find_element(By.XPATH, '//div[@id="SIvCob"]').text

    data = {'Page Title' : title, 'Language' : language}

    return data

@app.route('/')
def home():
    def home():
    return "Selenium-Wire is working"

if __name__ == '__main__':
    app.run(debug=True, port=3000)
