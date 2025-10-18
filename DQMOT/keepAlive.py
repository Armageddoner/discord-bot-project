from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    print("got pinged")
    
    return "DQMOT Still Live", 200

def run():
    app.run(host="0.0.0.0", port=5000)

def keepAlive():
    t = Thread(target=run)

    t.start()
