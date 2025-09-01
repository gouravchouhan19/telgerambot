from flask import Flask
from threading import Thread

# Flask app create karte hain
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

# Webserver run karne ka function
def run():
    app.run(host='0.0.0.0', port=8080)

# Thread me server ko background me chalane ke liye function
def keep_alive():
    t = Thread(target=run)
    t.start()
