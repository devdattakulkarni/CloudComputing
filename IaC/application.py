from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    # Requirement 1
    # read env var MY_ENV_VAR
    # return its value
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
