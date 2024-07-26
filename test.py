from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/')
def home():
    return "Playwright is working"

@app.route('/scrape')
def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://www.google.com")
            title = page.title()
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            browser.close()

    return jsonify({"title": title})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
