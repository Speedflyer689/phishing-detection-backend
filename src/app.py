from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Base URL retrieved for root URL"

if __name__ == '__main__':
    app.run(debug=True)