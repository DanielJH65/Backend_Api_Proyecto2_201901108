from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_api import status
import json, os
from Usuario import Usuario

app = Flask(__name__)
CORS(app)

usuarios = []
peliculas = []
funciones = []

@app.route('/', methods = ['GET'])
def inicio():
    return "<h1>Api Iniciada</h1>"

@app.route('/crearUsuario', methods = ['POST'])
def crearUsuario():
    datos = request.get_json()
    nombre = datos['nombre']
    apellido = datos['apellido']
    usuario = datos['usuario']
    contra = datos['contra']
    rol = datos['rol']
    nuevo_usuario = Usuario(nombre, apellido, usuario, contra, rol)
    global usuarios
    for usuario in usuarios:
        if usuario.nombre == nombre:
            return jsonify({'mensaje' : 'Error, El usuario ya existe'}), status.HTTP_400_BAD_REQUEST
    usuario.append(nuevo_usuario)
    return jsonify({'mensaje' : 'Satisfactorio, El usuario se creo correctamente'})

@app.route('/iniciarSesion', methods = ['GET'])
def iniciarSesion():
    datos = request.get_json()
    usuario = datos['usuario']
    contra = datos['contra']
    global usuarios
    for usuario in usuarios:
        if usuario.usuario == usuario and usuario.contra == contra:
            return jsonify({'mensaje' : 'Usuario encontrado'})
    return jsonify({'mensaje' : 'Error, El usuario no existe'}), status.HTTP_400_BAD_REQUEST

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')