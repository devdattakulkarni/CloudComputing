from flask import Flask, request
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# Add "greetings" route
# Read "GREETING" environment variable and return its value

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) # Change port to 5001
