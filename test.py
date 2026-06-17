from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Server Working"

print("Starting Flask...")

if __name__ == "__main__":
    print("Running app...")
    app.run(host="127.0.0.1", port=5000, debug=True)