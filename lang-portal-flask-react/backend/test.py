from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

# Gunicorn will look for the 'app' variable
application = app

if __name__ == '__main__':
    print("Starting Flask server on port 49152...")
    app.run(host='localhost', port=49152, debug=True) 