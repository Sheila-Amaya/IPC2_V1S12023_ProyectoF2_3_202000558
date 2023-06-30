from flask import Flask, redirect, render_template, request
from Lectura import *
from Estructuras.EnlazadaSimple import *
from usuario import *
from Estructuras.DobleEnlazadaCircular import *
from Estructuras.DobleEnlazada import *
from favorito import *
from boleto import *
from flask import Flask, jsonify
import xml.etree.ElementTree as ET
import os
from factura import *

app = Flask(__name__)


# Declarar una variable global como una instancia de EnlazadaSimple
listaUsuarios = EnlazadaSimple()
listaCategorias = EnlazadaSimple()
listaPeliculas = CicularDobleEnlazada()
listaCine = ListaDobleEnlazada()
listaSala = EnlazadaSimple()
listaTarjetas = ListaDobleEnlazada()
listaFavoritos = []
listaAsientos = []
listaHistorial = []
boletos = 0
listaFacturas = []
correo = None
contrasena = None


def crear_usuario_por_defecto():  # usuario administrador
    # Crear un usuario por defecto
    rol = "administrador"
    nombre = "admi"
    apellido = "admi"
    telefono = "3834657892"
    correo = "admi@mail.com"
    contrasena = "123"
    usuario = Usuario(rol, nombre, apellido, telefono, correo, contrasena)

    # Agregar el usuario a la lista de usuarios
    listaUsuarios.agregarUltimo(usuario)

@app.route('/')  # PANTALLA INICIO
def home():
    return render_template('home.html', categorias=listaCategorias)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        temp = listaUsuarios.primero
        while temp:
            if temp.dato.rol == "cliente" and temp.dato.correo == correo and temp.dato.contrasena == contrasena:
                # Inicio de sesión exitoso como cliente
                return redirect('/ventana_cliente')

            if temp.dato.rol == "administrador" and temp.dato.correo == correo and temp.dato.contrasena == contrasena:
                # Inicio de sesión exitoso como administrador
                return redirect('/ventana_administrador')

            temp = temp.siguiente
        # Si no se encuentra un usuario con las credenciales correctas, se muestra un mensaje de error
        error = "Credenciales incorrectas. Vuelve a intentarlo."
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/ventana_cliente')
def ventana_cliente():
    # Lógica y renderizado de la página del panel de cliente
    return render_template('cliente.html')

@app.route('/ventana_administrador')
def ventana_administrador():
    # ..
    return render_template('administrador.html')

# GESTION USUARIOS
@app.route('/gestionar_usuarios')
def gestion_usuario():
    return render_template('gestionU.html')

# CARGAR XML DE USUARIO
@app.route('/upload', methods=['GET', 'POST'])
def upload_xml():
    global listaUsuarios
    if request.method == 'POST':
        if 'xml_file' not in request.files:
            return jsonify({'error': 'No se ha seleccionado ningún archivo'})

        xml_file = request.files['xml_file']

        if xml_file.filename == '':
            return jsonify({'error': 'No se ha seleccionado ningún archivo'})

        if xml_file and xml_file.filename.endswith('.xml'):
            # Crear una instancia de la clase Lectura
            lectura = Lectura()
            # Llamar al método lecturaU() para procesar el XML
            datosArchivo = lectura.lecturaU(xml_file)

            if listaUsuarios.estaVacia():
                # Si la lista está vacía, simplemente asignar los datos del archivo a la lista
                listaUsuarios = datosArchivo
            else:
                # Si la lista no está vacía, agregar los datos del archivo al final de la lista existente
                ultimoNodo = listaUsuarios.ultimo
                ultimoNodo.siguiente = datosArchivo.primero
                listaUsuarios.ultimo = datosArchivo.ultimo
            return jsonify({'bien': 'Archivo XML cargado y procesado con exito'})
        else:
            return jsonify({'error': 'El archivo debe tener extensión .xml'})

    # Si la solicitud es GET, simplemente muestra el formulario
    return render_template('gestionU.html')

@app.route('/usuarios')
def mostrar_usuarios():
    # Utiliza la variable global listaUsuarios para pasar la lista de usuarios a la plantilla HTML
    return render_template('usuarios.html', usuarios=listaUsuarios)

@app.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        rol = request.form['rol']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        if listaUsuarios.estaVacia():
            # Si la lista está vacía, simplemente asignar los datos del nuevo usuario a la lista
            usuario = Usuario(rol, nombre, apellido,
                            telefono, correo, contrasena)
            listaUsuarios.agregarUltimo(usuario)
            mensaje = "Usuario agregado con éxito."
        else:
            # Si la lista no está vacía, verificar si el correo ya existe en la lista
            if listaUsuarios.buscarPorCorreo(correo) is not None:
                mensaje = "Ya existe un usuario con el correo ingresado."
            else:
                usuario = Usuario(rol, nombre, apellido,
                                telefono, correo, contrasena)
                listaUsuarios.agregarUltimo(usuario)
                mensaje = "Usuario agregado con éxito."

        return render_template('agregar_usuario.html', mensaje=mensaje)

    return render_template('agregar_usuario.html')

@app.route('/eliminar_usuario', methods=['GET', 'POST'])
def eliminar_usuario():
    if request.method == 'POST':
        correo = request.form['correo']
        listaUsuarios.eliminarPorCorreo(correo)  # Eliminar el nodo de la lista
        return render_template('eliminar_usuario.html')
    return render_template('eliminar_usuario.html')

@app.route('/modificar_usuario', methods=['GET', 'POST'])
def modificar_usuario():
    if request.method == 'POST':
        correo = request.form['correo']
        # Buscar el usuario por correo en la lista de usuarios
        usuario = listaUsuarios.buscarPorCorreo(correo)
        if usuario is not None:
            nuevoNombre = request.form['nuevo_nombre']
            nuevoApellido = request.form['nuevo_apellido']
            nuevoTelefono = request.form['nuevo_telefono']
            nuevoCorreo = request.form['nuevo_correo']
            nuevaContrasena = request.form['nueva_contrasena']

            # Modificar los datos del usuario
            usuario.nombre = nuevoNombre
            usuario.apellido = nuevoApellido
            usuario.telefono = nuevoTelefono
            usuario.correo = nuevoCorreo
            usuario.contrasena = nuevaContrasena

            mensaje = "Los datos del usuario han sido modificados con éxito."
        else:
            mensaje = "No se encontró ningún usuario con el correo especificado."
        return render_template('modificar_usuario.html', mensaje=mensaje)
    return render_template('modificar_usuario.html')

# GESTION CATEGORIAS Y PELICULAS
@app.route('/gestionar_categorias')
def gestion_categoria():
    return render_template('gestionC.html')

# CARGAR XML CATEGORIAS Y PELICULAS
@app.route('/upload2', methods=['GET', 'POST'])
def xml_categoria():
    global listaCategorias
    global listaPeliculas

    if request.method == 'POST':
        if 'xml_file' not in request.files:
            return "Error: No se ha seleccionado ningún archivo"

        xml_file = request.files['xml_file']

        if xml_file.filename == '':
            return "Error: No se ha seleccionado ningún archivo"

        if xml_file and xml_file.filename.endswith('.xml'):
            # Crear una instancia de la clase Lectura
            lectura = Lectura()
            # Llamar al método lecturaCP() para procesar el XML
            resultado = lectura.lecturaCP(xml_file)

            if resultado is not None:
                categorias_nuevas, peliculas_nuevas = resultado
                if listaCategorias.estaVacia():
                    listaCategorias = categorias_nuevas
                else:
                    temp = categorias_nuevas.primero
                    while temp:
                        listaCategorias.agregarUltimo(temp.dato)
                        temp = temp.siguiente

                return jsonify({'bien': 'Archivo XML cargado y procesado con exito'})
            else:
                return jsonify({'error': 'El archivo debe tener extensión .xml'})
        # Si la solicitud es GET, simplemente muestra el formulario
        return render_template('gestionC.html')

@app.route('/mostrar_cp')
def mostrar_c():
    # Utiliza la variable global listaUsuarios para pasar la lista de usuarios a la plantilla HTML
    return render_template('categorias.html', categorias=listaCategorias)

@app.route('/agregar_categoria', methods=['GET', 'POST'])
def agregar_categoria():
    if request.method == 'POST':
        nombre_categoria = request.form['nombre_categoria']
        agregar_pelicula = request.form.get('agregar_pelicula')
        if agregar_pelicula == 'si':
            titulo = request.form['titulo']
            director = request.form['director']
            anio = request.form['anio']
            fecha = request.form['fecha']
            hora = request.form['hora']
            imagen = request.form['imagen']
            precio = float(request.form['precio'])
            categoria = listaCategorias.buscarPorCategoria(nombre_categoria)
            if categoria is not None:
                pelicula = Pelicula(titulo, director, anio,
                                    fecha, hora, imagen, precio)
                categoria.pelicula.agregarFinal(pelicula)
                mensaje = "Película agregada a la categoría existente."
            else:
                peliculas = CicularDobleEnlazada()
                pelicula = Pelicula(titulo, director, anio,
                                    fecha, hora, imagen, precio)
                peliculas.agregarFinal(pelicula)
                nueva_categoria = Categoria(nombre_categoria, peliculas)
                listaCategorias.agregarUltimo(nueva_categoria)
                mensaje = "Categoría y película agregadas con éxito."
        else:
            mensaje = "No se agregó ninguna película a la categoría."
        return render_template('agregar_categoria.html', mensaje=mensaje)
    return render_template('agregar_categoria.html')

@app.route('/modificar_categoria', methods=['GET', 'POST'])
def modificar_categoria():
    if request.method == 'POST':
        nombre_categoria_actual = request.form['nombre_categoria_actual']
        # Buscar la categoría por nombre actual en la lista de categorías
        categoria = listaCategorias.buscarPorCategoria(nombre_categoria_actual)
        if categoria is not None:
            mensaje = "Categoría encontrada. ¿Desea modificar alguna película?"
            if request.form.get('modificar_pelicula') == 'si':
                nombre_pelicula = request.form['nombre_pelicula']
                # Buscar la película por nombre en la lista de películas de la categoría
                pelicula = categoria.pelicula.buscarPeli(nombre_pelicula)
                if pelicula is not None:
                    # Obtener los nuevos datos de la película
                    nuevo_titulo = request.form['nuevo_titulo']
                    nuevo_director = request.form['nuevo_director']
                    nuevo_anio = request.form['nuevo_anio']
                    nuevo_fecha = request.form['nuevo_fecha']
                    nuevo_hora = request.form['nuevo_hora']
                    nuevo_imagen = request.form['nuevo_imagen']
                    nuevo_precio = float(request.form['nuevo_precio'])
                    # Modificar los datos de la película
                    pelicula.titulo = nuevo_titulo
                    pelicula.director = nuevo_director
                    pelicula.anio = nuevo_anio
                    pelicula.fecha = nuevo_fecha
                    pelicula.hora = nuevo_hora
                    pelicula.imagen = nuevo_imagen
                    pelicula.precio = nuevo_precio
                    mensaje = "La película ha sido modificada con éxito."
                else:
                    mensaje = "No se encontró ninguna película con el nombre especificado."
            # Modificar el nombre de la categoría si se proporcionó uno nuevo
            nuevo_nombre_categoria = request.form['nuevo_nombre_categoria']
            if nuevo_nombre_categoria:
                categoria.nombre = nuevo_nombre_categoria
            return render_template('modificar_categoria.html', categoria=categoria, mensaje=mensaje)
        else:
            mensaje = "No se encontró ninguna categoría con el nombre especificado."
            return render_template('modificar_categoria.html', mensaje=mensaje)
    return render_template('modificar_categoria.html')

@app.route('/eliminar_categoria', methods=['GET', 'POST'])
def eliminar_categoria():
    if request.method == 'POST':
        nombre_categoria = request.form['nombre_categoria']
        categoria = listaCategorias.buscarPorCategoria(nombre_categoria)
        if categoria is not None:
            mensaje = "Categoría encontrada. ¿Desea eliminar alguna película?"
            if request.form.get('eliminar_pelicula') == 'si':
                nombre_pelicula = request.form['nombre_pelicula']
                pelicula = categoria.pelicula.buscarPeli(nombre_pelicula)
                if pelicula is not None:
                    categoria.pelicula.eliminar(nombre_pelicula)
                    mensaje = "La película ha sido eliminada de la categoría."
                else:
                    mensaje = "No se encontró ninguna película con el nombre especificado."
            else:
                listaCategorias.eliminarPorCategoria(nombre_categoria)
                mensaje = "La categoría y todas sus películas han sido eliminadas."
        else:
            mensaje = "No se encontró ninguna categoría con el nombre especificado."
        return render_template('eliminar_categoria.html', mensaje=mensaje)
    return render_template('eliminar_categoria.html')

# GESTIONAR SALAS Y CINE
@app.route('/gestionar_salas')
def gestion_salas():
    # ...
    return render_template('gestionS.html')

@app.route('/upload3', methods=['GET', 'POST'])
def xml_sala():
    global listaSala
    global listaCine

    if request.method == 'POST':
        if 'xml_file' not in request.files:
            return "Error: No se ha seleccionado ningún archivo"

        xml_file = request.files['xml_file']

        if xml_file.filename == '':
            return "Error: No se ha seleccionado ningún archivo"

        if xml_file and xml_file.filename.endswith('.xml'):
            # Crear una instancia de la clase Lectura
            lectura = Lectura()
            # Llamar al método lecturaS() para procesar el XML
            resultado = lectura.lecturaS(xml_file)

            if resultado is not None:
                listaCine, listaSala = resultado
                return jsonify({'bien': 'Archivo XML cargado y procesado con exito'})
            else:
                return jsonify({'error': 'El archivo debe tener extensión .xml'})

        # Si la solicitud es GET, simplemente muestra el formulario
        return render_template('gestionU.html')

@app.route('/mostrar_s')
def mostrar_s():
    return render_template('salas.html', cines=listaCine)

@app.route('/modificar_cine', methods=['GET', 'POST'])
def modificar_cine():
    if request.method == 'POST':
        nombre_cine = request.form['nombre_cine']
        nuevo_nombre_cine = request.form['nuevo_nombre_cine']
        numero_sala = request.form['numero_sala']
        nuevo_numero_sala = request.form['nuevo_numero_sala']
        nuevo_asientos_sala = request.form['nuevo_asientos_sala']

        cine_encontrado = None
        for cine in listaCine:  # listaCine es la lista doblemente enlazada de cines
            if cine.nombre == nombre_cine:
                cine_encontrado = cine
                break

        if cine_encontrado is not None:
            cine_encontrado.nombre = nuevo_nombre_cine

            sala_encontrada = None
            for sala in cine_encontrado.sala:  # salas es la lista simple de salas dentro del cine
                if sala.num == numero_sala:
                    sala_encontrada = sala
                    break

            if sala_encontrada is not None:
                sala_encontrada.num = nuevo_numero_sala
                sala_encontrada.asientos = nuevo_asientos_sala
                mensaje = "Cine y sala modificados con éxito."
            else:
                mensaje = "No se encontró ninguna sala con el número especificado."
        else:
            mensaje = "No se encontró ningún cine con el nombre especificado."

        return render_template('modificar_cine.html', mensaje=mensaje)

    return render_template('modificar_cine.html')

@app.route('/agregar_salas', methods=['GET', 'POST'])
def agregar_sala():
    if request.method == 'POST':
        nombre_cine = request.form['nombre_cine']
        agregar_sala = request.form.get('agregar_sala')

        if agregar_sala == 'si':
            numero_sala = request.form['numero_sala']
            asientos_sala = request.form['asientos_sala']

            if not listaCine.estaVacia():
                cine = listaCine.buscarCine(nombre_cine)

                if cine is not None:
                    sala = Sala(numero_sala, asientos_sala)
                    cine.sala.agregarUltimo(sala)
                    mensaje = "Sala agregada al cine existente."
                else:
                    salas = EnlazadaSimple()
                    sala = Sala(numero_sala, asientos_sala)
                    salas.agregarUltimo(sala)
                    nuevo_cine = Cine(nombre_cine, salas)
                    listaCine.agregarUltimo(nuevo_cine)
                    mensaje = "Cine y sala agregados con éxito."
            else:
                salas = EnlazadaSimple()
                sala = Sala(numero_sala, asientos_sala)
                salas.agregarUltimo(sala)
                nuevo_cine = Cine(nombre_cine, salas)
                listaCine.agregarUltimo(nuevo_cine)
                mensaje = "Se creó un nuevo cine con la sala."
        else:
            mensaje = "No se agregó ninguna sala al cine."

        return render_template('agregar_salas.html', mensaje=mensaje)

    return render_template('agregar_salas.html')

@app.route('/eliminar_cine', methods=['GET', 'POST'])
def eliminar_cine():
    if request.method == 'POST':
        nombre_cine = request.form['nombre_cine']
        cine = listaCine.buscarCine(nombre_cine)
        if cine is not None:
            listaCine.eliminarPorCine(nombre_cine)
            mensaje = "El cine ha sido eliminado exitosamente."
            return render_template('eliminar_cine.html', mensaje=mensaje)
        else:
            mensaje = "No se encontró ningún cine con el nombre especificado."
            return render_template('eliminar_cine.html', mensaje=mensaje)

    return render_template('eliminar_cine.html')

# GESTION TARJETAS
@app.route('/gestionar_tarjeta')
def gestion_tarjeta():
    # ...
    return render_template('gestionT.html')

@app.route('/upload4', methods=['GET', 'POST'])
def upload_tarjetas():
    global listaTarjetas
    if request.method == 'POST':
        if 'xml_file' not in request.files:
            return jsonify({'error': 'No se ha seleccionado ningún archivo'})

        xml_file = request.files['xml_file']

        if xml_file.filename == '':
            return jsonify({'error': 'No se ha seleccionado ningún archivo'})

        if xml_file and xml_file.filename.endswith('.xml'):
            # Crear una instancia de la clase Lectura
            lectura = Lectura()
            # Llamar al método lecturaT() para procesar el XML
            datosArchivo = lectura.lecturaT(xml_file)

            if listaTarjetas.estaVacia():
                # Si la lista está vacía, simplemente asignar los datos del archivo a la lista
                listaTarjetas = datosArchivo
            else:
                # Si la lista no está vacía, agregar los datos del archivo al final de la lista existente
                listaTarjetas.agregarUltimo(datosArchivo)

            return jsonify({'bien': 'Archivo XML cargado y procesado con éxito'})
        else:
            return jsonify({'error': 'El archivo debe tener extensión .xml'})

    # Si la solicitud es GET, simplemente muestra el formulario
    return render_template('gestionT.html')

#asigno la tarjeta a los usuarios
@app.route('/mostrar_t')
def mostrar_t():
    # Obtener la lista de usuarios y tarjetas
    global listaUsuarios
    global listaTarjetas

    if listaTarjetas is not None:
        # Asignar las tarjetas a los usuarios correspondientes
        for tarjeta in listaTarjetas:
            #print("Número de tarjeta:", tarjeta.numero)
            for usuario in listaUsuarios:
                nombre_completo = usuario.nombre + " " + usuario.apellido
                if nombre_completo == tarjeta.titular:
                    usuario.tarjeta = tarjeta

    return render_template('tarjetas.html', usuarios=listaUsuarios)

@app.route('/agregar_tarjeta', methods=['GET', 'POST'])
def agregar_tarjeta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo_tarjeta = request.form['tipo_tarjeta']
        numero_tarjeta = request.form['numero_tarjeta']
        fecha_expiracion = request.form['fecha_expiracion']

        # Buscar el usuario en la listaUsuarios
        usuario = None
        for u in listaUsuarios:
            if u.nombre == nombre and u.apellido == apellido:
                usuario = u
                break

        if usuario is not None:
            # Crear una instancia de Tarjeta con los datos ingresados
            tarjeta = Tarjeta(tipo_tarjeta, numero_tarjeta,
                            f"{nombre} {apellido}", fecha_expiracion)

            # Asignar la tarjeta al usuario
            usuario.tarjeta = tarjeta

            return "Tarjeta agregada correctamente."
        else:
            return "No se encontró el usuario."

    return render_template('agregar_tarjeta.html')


@app.route('/modificar_tarjeta', methods=['GET', 'POST'])
def modificar_tarjeta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo = request.form['tipo']
        numero_tarjeta = request.form['numero_tarjeta']
        titular = request.form['titular']
        fecha_expiracion = request.form['fecha_expiracion']

        # Buscar el usuario en la listaUsuarios
        usuario = None
        for u in listaUsuarios:
            if u.nombre == nombre and u.apellido == apellido:
                usuario = u
                break

        if usuario is not None:
            # Verificar si el usuario tiene una tarjeta asignada
            if usuario.tarjeta is not None:
                # Actualizar los datos de la tarjeta
                usuario.tarjeta.tipo = tipo
                usuario.tarjeta.numero = numero_tarjeta
                usuario.tarjeta.titular = titular
                usuario.tarjeta.fecha_expiracion = fecha_expiracion
            else:
                # Si el usuario no tiene una tarjeta asignada, crear una nueva tarjeta con los datos proporcionados
                tarjeta = Tarjeta(numero_tarjeta, titular, fecha_expiracion)
                usuario.tarjeta = tarjeta

            return "Tarjeta modificada exitosamente."
        else:
            return "No se encontró el usuario."

    return render_template('modificar_tarjeta.html')

@app.route('/eliminar_tarjeta', methods=['GET', 'POST'])
def eliminar_tarjeta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        numero_tarjeta = request.form['tarjeta']

        # Buscar al usuario correspondiente
        usuario = listaUsuarios.buscarUsuario(nombre)

        if usuario is not None:
            # Verificar si el usuario tiene tarjetas asignadas
            if usuario.tarjeta is None:
                mensaje = "El usuario no tiene tarjetas asignadas."
            else:
                # Buscar la tarjeta en la lista de tarjetas del usuario
                tarjeta_encontrada = listaTarjetas.buscarT(numero_tarjeta)
                if tarjeta_encontrada is not None:
                    # Eliminar la tarjeta del usuario
                    listaTarjetas.eliminarTarjeta(numero_tarjeta)
                    usuario.tarjeta = None
                    mensaje = "Tarjeta eliminada exitosamente."
                else:
                    mensaje = "No se encontró la tarjeta en la lista de tarjetas."
        else:
            mensaje = "No se encontró al usuario."

        return render_template('eliminar_tarjeta.html', mensaje=mensaje)

    return render_template('eliminar_tarjeta.html')

# GESTION BOLETOS ADMINISTRADOR



# REGISTRAR USUARIO CLIENTE
@app.route('/agregar_usuario_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        rol = "cliente"
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        if listaUsuarios.estaVacia():
            # Si la lista está vacía, simplemente asignar los datos del nuevo usuario a la lista
            usuario = Usuario(rol, nombre, apellido,
                            telefono, correo, contrasena)
            listaUsuarios.agregarUltimo(usuario)
            mensaje = "Usuario agregado con éxito."
        else:
            # Si la lista no está vacía, verificar si el correo ya existe en la lista
            if listaUsuarios.buscarPorCorreo(correo) is not None:
                mensaje = "Ya existe un usuario con el correo ingresado."
            else:
                usuario = Usuario(rol, nombre, apellido,
                                telefono, correo, contrasena)
                listaUsuarios.agregarUltimo(usuario)
                mensaje = "Usuario agregado con éxito."

        return render_template('agregar_usuario_cliente.html', mensaje=mensaje)

    return render_template('agregar_usuario_cliente.html')

# CLIENTE
# VER PELICULAS-GENERAL-POR CATEGORIA-DETALLES
@app.route('/ver_general', methods=['GET', 'POST'])
def ver_peliculas():
    return render_template('ver_general.html', categorias=listaCategorias)

@app.route('/ver_filtrar', methods=['GET', 'POST'])
def ver_filtrar():
    mensaje = None

    if request.method == 'POST':
        categoria = request.form.get('nombre_categoria')

        if categoria:
            categoria_actual = listaCategorias.buscarUnaCategoria(categoria)
            if categoria_actual is not None:
                return render_template('ver_filtrar.html', categoria_actual=categoria_actual)
            else:
                mensaje = "No se encontró la categoría en la lista."
        else:
            mensaje = "Debe ingresar la categoría."

    return render_template('ver_filtrar.html', mensaje=mensaje)

@app.route('/ver_detalles_pelicula', methods=['GET', 'POST'])
def ver_detalles_pelicula():
    if request.method == 'POST':
        categoria = request.form.get('categoria')
        titulo = request.form.get('titulo')

        # Buscar la categoría por nombre
        categoria_actual = listaCategorias.buscarPorCategoria(categoria)
        if categoria_actual:
            # Buscar la película por nombre en la categoría encontrada
            pelicula = categoria_actual.pelicula.buscarPeliculaPorNombre(
                titulo)
            if pelicula:
                return render_template('ver_detalles_pelicula.html', pelicula=pelicula)

    return render_template('ver_detalles_pelicula.html')

# lISTADO DE PELICULAS FAVORIAS-VER-AGREGAR
@app.route('/agregar_favoritas', methods=['GET', 'POST'])
def agregar_favoritas():
    if request.method == 'POST':
        categoria = request.form.get('categoria')
        nombre_pelicula = request.form.get('nombre_pelicula')

        # Buscar la categoría en la lista enlazada de categorías
        categoria_actual = listaCategorias.buscarPorCategoria(categoria)
        if categoria_actual:
            # Buscar la película en la categoría
            pelicula = categoria_actual.pelicula.buscarPeli(nombre_pelicula)

            if pelicula:
                # Crear el objeto Favorito con el título e imagen de la película
                favorito = Favorito(pelicula.titulo, pelicula.imagen)

                # Agregar el objeto Favorito a la lista de favoritos
                listaFavoritos.append(favorito)

                mensaje = "La película se ha agregado a la lista de favoritos."
            else:
                mensaje = "La película no se encontró en la categoría seleccionada."
        else:
            mensaje = "La categoría no se encontró en la lista."

        return render_template('agregar_favoritas.html', mensaje=mensaje)

    return render_template('agregar_favoritas.html')

# mostrar la lista favoritos
@app.route('/lista_favoritas')
def lista_favoritas():
    return render_template('lista_favoritas.html', favoritos=listaFavoritos)


# COMPRAR BOLETO
@app.route('/comprar_boletos', methods=['GET', 'POST'])
def comprar_boletos():
    boletos = 0
    if request.method == 'POST':
        cine = request.form.get('cine')
        sala = request.form.get('sala')
        numero_asiento = request.form.get('numero_asiento')
        categoria = request.form.get('categoria')
        titulo = request.form.get('titulo')
        num_boletos = request.form.get('num_boletos')
        #GENERAR FACTURA
        nombre = request.form.get('nombre')
        NIT = request.form.get('nit')
        direccion = request.form.get('direccion')
        
        cine_actual = listaCine.buscarCine(cine)
        print(cine_actual)
        if cine_actual is not None:
            sala_encontrada = cine_actual.sala.buscarPorSala(sala)
            print(sala_encontrada)
            if sala_encontrada is not None:
                rango_asientos = range(1, int(sala_encontrada.asientos) + 1)
                if int(numero_asiento) in rango_asientos:
                    if numero_asiento not in listaAsientos:
                        listaAsientos.append(numero_asiento)
                        totalCompra = 0

                        categoria_actual = listaCategorias.buscarPorCategoria(categoria)
                        if categoria_actual is not None:
                            pelicula_encontrada = categoria_actual.pelicula.buscarPeliculaParaBoleto(titulo)
                            if pelicula_encontrada is not None:
                                #print("Precio de la película:", pelicula_encontrada.precio)
                                #print("Cantidad de boletos:", num_boletos)
                                totalCompra = pelicula_encontrada.precio * int(num_boletos)
                                boletos += 1  # Inicializar la variable boletos
                                generarFactura(nombre ,NIT,direccion,categoria, cine_actual.nombre, titulo, num_boletos, sala, boletos, totalCompra, numero_asiento)

                                error = "No se encontró la película especificada"
                        else:
                            error = "No se encontró la categoría especificada"
                    else:
                        error = "El asiento ya está ocupado por otro usuario"
                else:
                    error = "El número de asiento ingresado no es válido"
            else:
                error = "No se encontró la sala especificada"
        else:
            error = "No se encontró el cine especificado"

        return render_template('comprar_boletos.html', cines=listaCine,categorias=listaCategorias, error=error)

    return render_template('comprar_boletos.html', cines=listaCine,categorias=listaCategorias)

@app.route('/facturas', methods=['GET'])
def mostrar_facturas():
    return render_template('facturas.html', facturas=listaFacturas)

def generarFactura(nombre ,NIT,direccion, categoria, cine, pelicula, num_boletos, sala, boletos, total, numero_asiento):
    categoria_actual = listaCategorias.buscarPorCategoria(categoria)
    peli = categoria_actual.pelicula.buscarPeli(pelicula)
        
    fecha = peli.fecha
    hora = peli.hora
    
    if nombre == "C/F":
        NIT ="N/A"
        direccion ="N/A"
        factura = Factura(nombre,NIT,direccion,cine, "#USACIPC2_202000558_" + str(boletos), nombre, '', '', pelicula, fecha, hora, sala, num_boletos, numero_asiento, total)
    else:
        factura = Factura(nombre ,NIT,direccion,cine, "#USACIPC2_202000558_" + str(boletos), nombre, NIT, direccion, pelicula, fecha, hora, sala, num_boletos, numero_asiento, total)
    
    listaFacturas.append(factura)
    boleto = Boleto(nombre, cine, "#USACIPC2_202000558_" + str(boletos), pelicula, fecha, hora, num_boletos,sala, numero_asiento, total,False)
    listaHistorial.append(boleto)


# HISTORIAL BOLETO
@app.route('/lista_historial')
def lista_():
    if len(listaHistorial) == 0:
        print("\n\tEl historial de boletos está vacío.")
    else:
        temp = listaUsuarios.primero
        while temp:
            if temp.dato.nombre == correo and temp.dato.contrasena == contrasena:
                agregarHistorialFavoritos(correo , contrasena)
                    #self.listaUsuario.mostrarUsuario()
            temp = temp.siguiente
    return render_template('historial_boletos.html', historial=listaHistorial)



def cancelarBoleto(numero_boleto):
    boleto_encontrado = None
    for boleto in listaHistorial:
        if boleto.numero_boleto == numero_boleto:
            boleto_encontrado = boleto
            break
    if boleto_encontrado:
        boleto_encontrado.cancelado = True
        print("\n\t¡El boleto ha sido cancelado exitosamente!")
    else:
        print("\n\tNo se encontró ningún boleto con el número proporcionado.")
        

def agregarHistorialFavoritos(correo, contrasena):
    # Buscar el nodo del usuario que inició sesión
    temp = listaUsuarios.primero
    while temp:
        if  temp.dato.nombre == correo and temp.dato.contrasena == contrasena:
            # Añadir el historial de boletos y las películas favoritas al nodo del usuario
            temp.dato.historial_Boletos = listaHistorial
            temp.dato.peliculas_Favoritas = listaFavoritos
            correo = None
            contrasena = None
            return
        temp = temp.siguiente




# API
@app.route('/getUsuarios', methods=['GET'])
def getUsuarios():
    try:
        retorno = [
            {
                "usuario": [
                    {
                        "rol": "cliente",
                        "nombre": "kiara",
                        "apellido": "Sanches",
                        "telefono": "00220022",
                        "correo": "kiara@mail.com",
                        "contrasena": "passd123"
                    },
                    {
                        "rol": "administrador",
                        "nombre": "Bonnie",
                        "apellido": "Smith",
                        "telefono": "98713672",
                        "correo": "Bom@example.com",
                        "contrasena": "pass456"
                    }
                ]
            }
        ]

        usuarios = []  # Lista para almacenar los usuarios

        for data in retorno:
            for usuario in data["usuario"]:
                usuarios.append(usuario)

        return jsonify(usuarios)

    except:
        return {"mensaje": "Error interno en el servidor", "status": 500}

@app.route('/getPeliculas', methods=['GET'])
def getPeliculas():
    try:
        if request.method == 'GET':
            retorno = {
                "categoria": [
                    {
                        "nombre": "Aventura",
                        "peliculas": {
                            "pelicula": [
                                {
                                    "titulo": "Las momias del faraon",
                                    "director": "Luc Besson",
                                    "anio": "2010",
                                    "fecha": "2023-02-05",
                                    "hora": "19:30",
                                    "imagen": "https://m.media-amazon.com/images/I/81GtN22pDML._AC_UF894,1000_QL80_.jpg",
                                    "precio": "52"
                                },
                                {
                                    "titulo": "Aladdin",
                                    "director": "Chad Stahelski",
                                    "anio": "2019",
                                    "fecha": "2023-06-06",
                                    "hora": "20:00",
                                    "imagen": "https://m.media-amazon.com/images/M/MV5BMjQ2ODIyMjY4MF5BMl5BanBnXkFtZTgwNzY4ODI2NzM@._V1_FMjpg_UX1000_.jpg",
                                    "precio": "55"
                                }
                            ]
                        }
                    },
                    {
                        "nombre": "Infantil",
                        "peliculas": {
                            "pelicula": [
                                {
                                    "titulo": "Sing 2",
                                    "director": "Garth Jenningsr",
                                    "anio": "2021",
                                    "fecha": "2023-04-05",
                                    "hora": "14:30",
                                    "imagen": "https://www.universalpictures.com.ar/tl_files/content/movies/sing2/posters/01.jpg",
                                    "precio": "75"
                                },
                                {
                                    "titulo": "spirited away",
                                    "director": "Hayao Miyazaki",
                                    "anio": "2001",
                                    "fecha": "2023-07-07",
                                    "hora": "21:15",
                                    "imagen": "https://miro.medium.com/v2/resize:fit:1000/1*Dkbs_BcI7NjUkresXt9R1w.jpeg",
                                    "precio": "82"
                                }
                            ]
                        }
                    }
                ]}
        else:
            retorno = {'mensaje': 'Error en la petición, método incorrecto'}
        return jsonify(retorno)
    except:
        return {"mensaje": "Error interno en el servidor", "status": 500}

@app.route('/getCine', methods=['GET'])
def getCine():
    try:
        if request.method == 'GET':
            retorno = {
                "cine": {
                    "nombre": "Cinemark",
                    "salas": {
                        "sala": [
                            {
                                "numero": "#USACIPC2_202212333_10",
                                "asientos": "110"
                            },
                            {
                                "numero": "#USACIPC2_202212333_11",
                                "asientos": "84"
                            },
                            {
                                "numero": "#USACIPC2_202212333_12",
                                "asientos": "130"
                            }
                        ]
                    }
                }
            }

        else:
            retorno = {'mensaje': 'Error en la petición, método incorrecto'}
        return jsonify(retorno)
    except:
        return {"mensaje": "Error interno en el servidor", "status": 500}

@app.route('/getTarjeta', methods=['GET'])
def getTarjeta():
    try:
        if request.method == 'GET':
            retorno = {
                    "tarjeta": [
                        {
                            "tipo": "Debito",
                            "numero": "405060708090100",
                            "titular": "Bonnie Smith",
                            "fecha_expiracion": "15/2024"
                        },
                        {
                            "tipo": "Credito",
                            "numero": "102030740506070",
                            "titular": "kiara Sanches",
                            "fecha_expiracion": "27/2023"
                        }
                    ]
            }

        else:
            retorno = {'mensaje': 'Error en la petición, método incorrecto'}
        return jsonify(retorno)
    except:
        return {"mensaje": "Error interno en el servidor", "status": 500}

#XML SALIDA
@app.route('/xml_usuarios', methods=['GET'])
def xml_usuarios():
    # Nombre de la carpeta para almacenar los archivos XML
    carpeta = "archivos_salida"

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Crear el elemento raíz del XML
    root = ET.Element("usuarios")

    # Recorrer la lista de usuarios y crear elementos XML para cada usuario
    temp = listaUsuarios.primero
    while temp is not None:
        # Crea el elemento de usuario
        usuario = ET.SubElement(root, "usuario")

        # Agregar elementos dentro del usuario
        rol = ET.SubElement(usuario, "rol")
        rol.text = temp.dato.rol

        nombre = ET.SubElement(usuario, "nombre")
        nombre.text = temp.dato.nombre

        apellido = ET.SubElement(usuario, "apellido")
        apellido.text = temp.dato.apellido

        telefono = ET.SubElement(usuario, "telefono")
        telefono.text = temp.dato.telefono

        correo = ET.SubElement(usuario, "correo")
        correo.text = temp.dato.correo

        contrasena = ET.SubElement(usuario, "contrasena")
        contrasena.text = temp.dato.contrasena

        # Crea el elemento de películas favoritas y agregar elementos de películas
        peliculas_favoritas = ET.SubElement(usuario, "peliculas_favoritas")
        for pelicula in temp.dato.peliculas_Favoritas:
            pelicula_element = ET.SubElement(peliculas_favoritas, "pelicula")
            pelicula_element.text = pelicula

        # Crear elemento de historial de boletos y agregar elementos de boletos
        historial_boletos = ET.SubElement(usuario, "historial_boletos")
        for boleto in temp.dato.historial_Boletos:
            boleto_element = ET.SubElement(historial_boletos, "boleto")
            # Agregar elementos de boleto

            # ...

        # Agregar tarjeta de crédito al usuario
        if temp.dato.tarjeta is not None:
            tarjeta = ET.SubElement(usuario, "tarjeta")

            tipo = ET.SubElement(tarjeta, "tipo")
            tipo.text = temp.dato.tarjeta.tipo

            numero = ET.SubElement(tarjeta, "numero")
            numero.text = temp.dato.tarjeta.numero

            titular = ET.SubElement(tarjeta, "titular")
            titular.text = temp.dato.tarjeta.titular

            fecha_expiracion = ET.SubElement(tarjeta, "fecha_expiracion")
            fecha_expiracion.text = temp.dato.tarjeta.fecha_expiracion

        temp = temp.siguiente

    # Combinar la ruta de la carpeta con el nombre del archivo XML
    ruta_archivo = os.path.join(carpeta, "usuarios.xml")

    # Convertir el árbol XML en una cadena con formato
    xml_string = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    # Escribir la cadena con formato en el archivo
    with open(ruta_archivo, "w") as file:
        file.write(xml_string)

    return jsonify({'message': 'XML usuarios generado correctamente.'})

@app.route('/xml_categorias', methods=['GET'])
def xml_categorias():
    # Nombre de la carpeta para almacenar los archivos XML
    carpeta = "archivos_salida"

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Crear el elemento raíz del XML
    root = ET.Element("categorias")

    temp = listaCategorias.primero
    while temp is not None:
        # Crea el elemento categoria
        categoria = ET.Element("categoria")

        # Crea el elemento nombre_categoria y agrega el nombre
        nombre_categoria = ET.SubElement(categoria, "nombre")
        nombre_categoria.text = temp.dato.nombre

        # Crea el elemento de peliculas
        peliculas = ET.SubElement(categoria, "peliculas")

        # Buscar la categoría en la lista de categorías por nombre
        categoria_buscada = listaCategorias.buscarPorCategoria(temp.dato.nombre)
        if categoria_buscada is not None:
            pelicula_actual = categoria_buscada.pelicula.primero
            while pelicula_actual is not None:
                # Crear el elemento pelicula
                pelicula_element = ET.SubElement(peliculas, "pelicula")

                # Crear las etiquetas para los atributos de la película y asignar sus valores
                titulo = ET.SubElement(pelicula_element, "titulo")
                titulo.text = pelicula_actual.dato.titulo

                director = ET.SubElement(pelicula_element, "director")
                director.text = pelicula_actual.dato.director

                anio = ET.SubElement(pelicula_element, "anio")
                anio.text = str(pelicula_actual.dato.anio)

                fecha = ET.SubElement(pelicula_element, "fecha")
                fecha.text = pelicula_actual.dato.fecha

                hora = ET.SubElement(pelicula_element, "hora")
                hora.text = pelicula_actual.dato.hora

                precio = ET.SubElement(pelicula_element, "precio")
                precio.text = str(pelicula_actual.dato.precio)

                pelicula_actual = pelicula_actual.siguiente
                if pelicula_actual == categoria_buscada.pelicula.primero:
                    break

        # Agregar el elemento categoria al elemento raíz
        root.append(categoria)

        temp = temp.siguiente
        if temp == listaCategorias.primero:
            break

    # Combinar la ruta de la carpeta con el nombre del archivo XML
    ruta_archivo = os.path.join(carpeta, "categorias.xml")

    # Convertir el árbol XML en una cadena con formato
    xml_string = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    # Escribir la cadena con formato en el archivo
    with open(ruta_archivo, "w") as file:
        file.write(xml_string)

    return jsonify({'message': 'XML categorias generado correctamente.'})

@app.route('/xml_salas', methods=['GET'])
def xml_salas():
    # Nombre de la carpeta para almacenar los archivos XML
    carpeta = "archivos_salida"

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Crear el elemento raíz del XML
    root = ET.Element("cines")

    temp = listaCine.primero
    while temp is not None:
        # Crea el elemento cine
        cine = ET.Element("cine")

        # Crea el elemento nombre_cine y agrega el nombre
        nombre_cine = ET.SubElement(cine, "nombre")
        nombre_cine.text = temp.dato.nombre

        # Crea el elemento de salas
        salas = ET.SubElement(cine, "salas")

        # Recorrer la lista de salas del cine actual
        temp.dato.sala.recorrerSalas()
        sala_actual = temp.dato.sala.primero
        while sala_actual is not None:
            # Crear el elemento sala
            sala_element = ET.SubElement(salas, "sala")

            # Crear las etiquetas para los atributos de la sala y asignar sus valores
            numero = ET.SubElement(sala_element, "numero")
            numero.text = sala_actual.dato.num

            asientos = ET.SubElement(sala_element, "asientos")
            asientos.text = sala_actual.dato.asientos

            sala_actual = sala_actual.siguiente

        # Agregar el elemento cine al elemento raíz
        root.append(cine)

        temp = temp.siguiente

    # Combinar la ruta de la carpeta con el nombre del archivo XML
    ruta_archivo = os.path.join(carpeta, "salas.xml")

    # Convertir el árbol XML en una cadena con formato
    xml_string = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    # Escribir la cadena con formato en el archivo
    with open(ruta_archivo, "w") as file:
        file.write(xml_string)

    return jsonify({'message': 'XML salas generado correctamente.'})

@app.route('/xml_tarjetas', methods=['GET'])
def xml_tarjetas():
    # Nombre de la carpeta para almacenar los archivos XML
    carpeta = "archivos_salida"

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Crear el elemento raíz del XML
    root = ET.Element("tarjetas")

    # Recorrer la lista de tarjetas y crear elementos XML para cada tarjeta
    for tarjeta in listaTarjetas:
        # Crear el elemento de tarjeta
        tarjeta_element = ET.SubElement(root, "tarjeta")

        # Agregar elementos dentro de la tarjeta
        tipo = ET.SubElement(tarjeta_element, "tipo")
        tipo.text = tarjeta.tipo

        numero = ET.SubElement(tarjeta_element, "numero")
        numero.text = tarjeta.numero

        titular = ET.SubElement(tarjeta_element, "titular")
        titular.text = tarjeta.titular

        fecha_expiracion = ET.SubElement(tarjeta_element, "fecha_expiracion")
        fecha_expiracion.text = tarjeta.fecha_expiracion

    # Combinar la ruta de la carpeta con el nombre del archivo XML
    ruta_archivo = os.path.join(carpeta, "tarjetas.xml")

    # Convertir el árbol XML en una cadena con formato
    xml_string = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    # Escribir la cadena con formato en el archivo
    with open(ruta_archivo, "w") as file:
        file.write(xml_string)

    return jsonify({'message': 'XML tarjetas generado correctamente.'})

@app.route('/logout')
def logout():
    # ...
    return redirect('/login')


if __name__ == '__main__':
    crear_usuario_por_defecto()
    app.run(debug=True)
