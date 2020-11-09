from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_api import status
import json
import os
from Usuario import Usuario
from Pelicula import Pelicula
from Funcion import Funcion

app = Flask(__name__)
CORS(app)

usuarios = []
peliculas = []
funciones = []

usuarios.append(Usuario("Usuario", "Maestro", "ADMIN", "admin", "Administrador"))


@app.route('/', methods=['GET'])
def inicio():
    return "<h1>Api Iniciada</h1>"


@app.route('/crearUsuario', methods=['POST'])
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
            return jsonify({'mensaje': 'Error, El usuario ya existe'}), status.HTTP_400_BAD_REQUEST
    usuarios.append(nuevo_usuario)
    return jsonify({'mensaje': 'Satisfactorio, El usuario se creo correctamente'}), status.HTTP_200_OK


@app.route('/obtenerUsuarios', methods=['GET'])
def ontenerUsuarios():
    json_usuarios = []
    global usuarios
    for contenido in usuarios:
        json_usuarios.append({
            'nombre': contenido.nombre,
            'apellido': contenido.apellido,
            'usuario': contenido.usuario,
            'contra': contenido.contra,
            'rol': contenido.rol
        })
    return jsonify(json_usuarios)


@app.route('/modificarUsuario', methods=['POST'])
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
                    if usu2.usuario == usuario_actual:
                        continue
                    else:
                        return jsonify({'mensaje': 'Error, ya existe en la lista de usuarios el nuevo usuario, prueba otro'}), status.HTTP_400_BAD_REQUEST
            usu.nombre = nombre
            usu.apellido = apellido
            usu.usuario = usuario
            usu.contra = contra
            return jsonify({'mensaje': 'Satisfactorio, el usuario se modificó correctamente'})
    return jsonify({'mensaje': 'Error, el usuario no existe en la lista de usuarios'}), status.HTTP_400_BAD_REQUEST


@app.route('/iniciarSesion', methods=['POST'])
def iniciarSesion():
    datos = request.get_json()
    usuario = datos['usuario']
    contra = datos['contra']
    print(usuario + " " + contra)
    global usuarios
    for usu in usuarios:
        if usu.usuario == usuario and usu.contra == contra:
            return jsonify({'mensaje': 'Usuario encontrado', 'rol': usu.rol, 'usuario': usu.usuario})
    return jsonify({'mensaje': 'Error, El usuario o contraseña son incorrectos'}), status.HTTP_400_BAD_REQUEST


@app.route('/recuperarContra', methods=['POST'])
def recuperarContra():
    datos = request.get_json()
    usuario = datos['usuario']
    global usuarios
    print(usuario)
    for usu in usuarios:
        if usu.usuario == usuario:
            return jsonify({'contra': str(usu.contra)})
    return jsonify({'mensaje': 'Error, El usuario no existe'}), status.HTTP_400_BAD_REQUEST


@app.route('/agregarPelicula', methods=['POST'])
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


@app.route('/obtenerPeliculas', methods=['GET'])
def ontenerPeliculas():
    json_peliculas = []
    global peliculas
    for pelicula in peliculas:
        json_peliculas.append({
            'titulo': pelicula.titulo,
            'url_imagen': pelicula.url_imagen,
            'puntuacion': pelicula.puntuacion,
            'duracion': pelicula.duracion,
            'sinopsis': pelicula.sinopsis,
            'resenas': pelicula.resenas
        })
    return jsonify(json_peliculas)


@app.route('/modificarPelicula', methods=['POST'])
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


@app.route('/eliminarPelicula', methods=['POST'])
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


@app.route('/agregarFuncion', methods=['POST'])
def agregarFuncion():
    datos = request.get_json()
    pelicula = datos['pelicula']
    sala = datos['sala']
    hora = datos['hora']
    global funciones
    id = 1
    for funcion in funciones:
        id = funcion.id + 1
    nueva_funcion = Funcion(id,pelicula, sala, hora)
    funciones.append(nueva_funcion)
    return jsonify({'mensaje': 'Satisfactorio, la función se agregó Correctamente'})


@app.route('/obtenerFunciones', methods=['GET'])
def ontenerFunciones():
    json_funciones = []
    global funciones
    for funcion in funciones:
        json_funciones.append({
            'id': funcion.id,
            'pelicula': funcion.pelicula,
            'sala': funcion.sala,
            'hora': funcion.hora, 
            'disponible': funcion.disponible(), 
            'asientos': funcion.asientos})
    return jsonify(json_funciones)

@app.route('/eliminarFuncion', methods=['POST'])
def eliminarFuncion():
    datos = request.get_json()
    id = int(datos['id'])
    global funciones
    i = 0
    for funcion in funciones:
        if funcion.id == id:
            funciones.pop(i)
            return jsonify({'mensaje': 'Satisfactorio, la funcion se eliminó correctamente'})
        else:
            i += 1
    return jsonify({'mensaje': 'Error, la funcion no existe en la lista de funciones'}), status.HTTP_400_BAD_REQUEST

@app.route('/obtenerUnaFuncion', methods=['GET'])
def obtenerUnaFuncion():
    datos = request.args.get('id')
    id = int(datos)
    global funciones
    for funcion in funciones:
        if funcion.id == id:
            return jsonify({'pelicula':funcion.pelicula,'asientos':funcion.asientos})
    return jsonify({"mensaje":"La función no existe"})

@app.route('/apartar', methods=['POST'])
def apartar():
    datos = request.get_json()
    identificador = datos['identificador']
    usuario = datos['usuario']
    id = int(datos['id'])
    print(id)
    global funciones
    for funcion in funciones:
        if funcion.id == id:
            funcion.apartar(identificador,usuario)
            return jsonify({"mensaje":"Completo"})
    return jsonify({"mensaje":"Error"}), status.HTTP_400_BAD_REQUEST

@app.route('/agregarResena', methods=['POST'])
def agregarResena():
    datos = request.get_json()
    titulo = datos['titulo']
    usuario = datos['usuario']
    texto = datos['texto']
    global peliculas
    for pelicula in peliculas:
        if pelicula.titulo == titulo:
            pelicula.resenas.append({
                "usuario": usuario,
                "texto": texto
            })
    return jsonify({'mensaje': 'Satisfactorio, la reseña se agregó Correctamente'})


@app.route('/cargaMasiva', methods=['POST'])
def cargaMasiva():
    datos = request.get_json()
    contenido = datos['contenido']
    filas = contenido.split("\r\n")
    global peliculas
    valido = False
    for fila in filas:
        if valido == False:
            valido = True
        else:
            columnas = fila.split(",")
            titulo = columnas[0]
            url_imagen = columnas[1]
            puntuacion = columnas[2]
            duracion = columnas[3]
            sinopsis = columnas[4]
            nueva_pelicula = Pelicula(titulo, url_imagen, puntuacion, duracion, sinopsis)
            print(titulo)
            global peliculas
            for pelicula in peliculas:
                if pelicula.titulo == titulo:
                    break
            peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify({'mensaje': 'Satisfactorio, las peliculas se agregarón correctamente'})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
