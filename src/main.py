from flask import Flask

from src.core import load_plugins

app = Flask(__name__)
load_plugins(app)

if __name__ == '__main__':
    app.run(debug=True)
