from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def inicio():
    return "<h1>Inicio</h1>"

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')