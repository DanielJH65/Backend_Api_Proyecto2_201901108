from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_api import status
import json, os
from Usuario import Usuario
from Pelicula import Pelicula
from Funcion import Funcion

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
    for usu in usuarios:
        if usu.usuario == usuario:
            return jsonify({'mensaje' : 'Error, El usuario ya existe'}), status.HTTP_400_BAD_REQUEST
    usuarios.append(nuevo_usuario)
    return jsonify({'mensaje' : 'Satisfactorio, El usuario se creo correctamente'})

@app.route('/modificarUsuario', methods = ['POST'])
def modificarUsuario():
    datos = request.get_json()
    usuario_actual = datos['usuario_actual']
    nombre = datos['nombre']
    apellido = datos['apellido']
    usuario = datos['usuario']
    contra = datos['contra']
    global usuarios
    for usu in usuarios:
        if usu.usuario == usuario_actual:
            for usu2 in usuarios:
                if usu2.usuario == usuario:
                    return jsonify({'mensaje': 'Error, ya existe en la lista de usuarios el nuevo usuario, prueba otro'}), status.HTTP_400_BAD_REQUEST
            usu.nombre = nombre
            usu.apellido = apellido
            usu.usuario = usuario
            usu.contra = contra
            return jsonify({'mensaje': 'Satisfactorio, el usuario se modificó correctamente'})
    return jsonify({'mensaje': 'Error, el usuario no existe en la lista de usuarios'}), status.HTTP_400_BAD_REQUEST

@app.route('/iniciarSesion', methods = ['GET'])
def iniciarSesion():
    datos = request.get_json()
    usuario = datos['usuario']
    contra = datos['contra']
    print(usuario + " " + contra)
    global usuarios
    for usu in usuarios:
        print(usu.usuario+" "+usu.contra)
        if usu.usuario == usuario and usu.contra == contra:
            return jsonify({'mensaje' : 'Usuario encontrado'})
    return jsonify({'mensaje' : 'Error, El usuario o contraseña son incorrectos'}), status.HTTP_400_BAD_REQUEST

@app.route('/recuperarContra', methods = ['GET'])
def recuperarContra():
    datos = request.get_json()
    usuario = datos['usuario']
    global usuarios
    for usu in usuarios:
        if usu.usuario == usuario:
            return jsonify({'contra' : str(usu.contra)})
    return jsonify({'mensaje' : 'Error, El usuario no existe'}), status.HTTP_400_BAD_REQUEST

@app.route('/agregarPelicula', methods = ['POST'])
def agregarPelicula():
    datos = request.get_json()
    titulo = datos['titulo']
    url_imagen = datos['url_imagen']
    puntuacion = datos['puntuacion']
    duracion = datos['duracion']
    sinopsis = datos['sinopsis']
    nueva_pelicula = Pelicula(titulo, url_imagen, puntuacion, duracion, sinopsis)
    global peliculas
    for pelicula in peliculas:
        if pelicula.titulo == titulo:
            return jsonify({'mensaje': 'Error, la pelicula ya existe'}), status.HTTP_400_BAD_REQUEST
    peliculas.append(nueva_pelicula)
    return jsonify({'mensaje': 'Satisfactorio, la pelicula se agrego correctamente'})

@app.route('/obtenerPeliculas', methods = ['GET'])
def ontenerPeliculas():
    json_peliculas = []
    global peliculas
    for pelicula in peliculas:
        json_peliculas.append({
            'titulo': pelicula.titulo, 
            'url_imagen' : pelicula.url_imagen, 
            'puntuacion': pelicula.puntuacion,
            'duracion' : pelicula.duracion,
            'sinopsis' : pelicula.sinopsis
            })
    return jsonify(json_peliculas)

@app.route('/modificarPelicula', methods = ['POST'])
def modificarPelicula():
    datos = request.get_json()
    titulo_actual = datos['titulo_actual']
    titulo = datos['titulo']
    url_imagen = datos['url_imagen']
    puntuacion = datos['puntuacion']
    duracion = datos['duracion']
    sinopsis = datos['sinopsis']
    global peliculas
    for pelicula in peliculas:
        if pelicula.titulo == titulo_actual:
            for pelicula2 in peliculas:
                if pelicula2.titulo == titulo:
                    return jsonify({'mensaje': 'Error, ya existe en la lista de peliculas el nuevo nombre, prueba otro'}), status.HTTP_400_BAD_REQUEST
            pelicula.titulo = titulo
            pelicula.url_imagen = url_imagen
            pelicula.puntuacion = puntuacion
            pelicula.duracion = duracion
            pelicula.sinopsis = sinopsis
            return jsonify({'mensaje': 'Satisfactorio, la pelicula se modificó correctamente'})
    return jsonify({'mensaje': 'Error, la pelicula no existe en la lista de peliculas'}), status.HTTP_400_BAD_REQUEST

@app.route('/eliminarPelicula', methods = ['POST'])
def eliminarPelicula():
    datos = request.get_json()
    titulo = datos['titulo']
    global peliculas
    i = 0
    for pelicula in peliculas:
        if pelicula.titulo == titulo:
            peliculas.pop(i)
            return jsonify({'mensaje': 'Satisfactorio, la pelicula se eliminó correctamente'})
        i += 1
    return jsonify({'mensaje': 'Error, la pelicula no existe en la lista de peliculas'}), status.HTTP_400_BAD_REQUEST

@app.route('/agregarFuncion', methods = ['POST'])
def agregarFuncion():
    datos = request.get_json()
    nombre = datos['nombre']
    horario = datos['horario']
    nueva_funcion = Funcion(nombre, horario)
    global funciones
    funciones.append(nueva_funcion)
    return jsonify({'mensaje': 'Satisfactorio, la función se agregó Correctamente'})

@app.route('/obtenerFunciones', methods = ['GET'])
def ontenerFunciones():
    json_funciones = []
    global funciones
    for funcion in funciones:
        json_funciones.append({'nombre': funcion.nombre, 'horario':funcion.horario, 'disponible': funcion.disponible()})
    return jsonify(json_funciones)

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')