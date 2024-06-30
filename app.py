from extensions import app
from flask import Flask


if __name__ == "__main__":
    from routes import *
    app.run(debug=True)
