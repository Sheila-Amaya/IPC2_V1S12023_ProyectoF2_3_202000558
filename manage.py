from flask import Flask, redirect, render_template, request
from Lectura import *
from Estructuras.EnlazadaSimple import *
from usuario import *
from Estructuras.DobleEnlazadaCircular import *
from Estructuras.DobleEnlazada import *

app = Flask(__name__)


listaUsuarios = EnlazadaSimple() # Declarar una variable global como una instancia de EnlazadaSimple
listaCategorias = EnlazadaSimple()
listaPeliculas =    CicularDobleEnlazada()
listaCine = ListaDobleEnlazada()
listaSala = EnlazadaSimple()

def crear_usuario_por_defecto(): #usuario administrador
    # Crear un usuario por defecto
    rol = "administrador"
    nombre = "admi"
    apellido = "administrador por defecto"
    telefono = "3834657892"
    correo = "admi@gmail.com"
    contrasena = "123"
    usuario = Usuario(rol, nombre, apellido, telefono, correo, contrasena)

    # Agregar el usuario a la lista de usuarios
    listaUsuarios.agregarUltimo(usuario)

@app.route('/') #PANTALLA INICIO
def home():
    return render_template('home.html')

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

#GESTION USUARIOS
@app.route('/gestionar_usuarios')
def gestion_usuario():
    return render_template('gestionU.html')

#CARGAR XML DE USUARIO
@app.route('/upload', methods=['GET', 'POST'])
def upload_xml():
    global listaUsuarios
    if request.method == 'POST':
        if 'xml_file' not in request.files:
            return "Error: No se ha seleccionado ningún archivo"
        
        xml_file = request.files['xml_file']
        
        if xml_file.filename == '':
            return "Error: No se ha seleccionado ningún archivo"
        
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
            return "Archivo XML cargado y procesado con éxito"
        else:
            return "Error: El archivo debe tener extensión .xml"
    
    # Si la solicitud es GET, simplemente muestra el formulario
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="xml_file">
        <input type="submit" value="Cargar">
    </form>
    '''

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
            usuario = Usuario(rol, nombre, apellido, telefono, correo, contrasena)
            listaUsuarios.agregarUltimo(usuario)
            mensaje = "Usuario agregado con éxito."
        else:
            # Si la lista no está vacía, verificar si el correo ya existe en la lista
            if listaUsuarios.buscarPorCorreo(correo) is not None:
                mensaje = "Ya existe un usuario con el correo ingresado."
            else:
                usuario = Usuario(rol, nombre, apellido, telefono, correo, contrasena)
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

#GESTION CATEGORIAS Y PELICULAS
@app.route('/gestionar_categorias')
def gestion_categoria():
    # Lógica y renderizado de la página del panel de categorias
    return render_template('gestionC.html')

#CARGAR XML CATEGORIAS Y PELICULAS
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

                return "Archivo XML cargado y procesado con éxito"
            else:
                return "Error al procesar el archivo XML"
        else:
            return "Error: El archivo debe tener extensión .xml"
    
    # Si la solicitud es GET, simplemente muestra el formulario
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="xml_file">
        <input type="submit" value="Cargar">
    </form>
    '''

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
                pelicula = Pelicula(titulo, director, anio, fecha, hora, imagen, precio)
                categoria.pelicula.agregarFinal(pelicula)
                mensaje = "Película agregada a la categoría existente."
            else:
                peliculas = CicularDobleEnlazada()
                pelicula = Pelicula(titulo, director, anio, fecha, hora, imagen, precio)
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

#GESTIONAR SALAS Y CINE
@app.route('/gestionar_salas')
def gestion_salas():
    # Lógica y renderizado de la página del panel de categorias
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
                return "Archivo XML cargado y procesado con éxito"
            else:
                return "Error al procesar el archivo XML"
        else:
            return "Error: El archivo debe tener extensión .xml"
    
    # Si la solicitud es GET, simplemente muestra el formulario
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="xml_file">
        <input type="submit" value="Cargar">
    </form>
    '''

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

#GESTION BOLETOS


#CLIENTE

@app.route('/logout')
def logout():
    #...
    return redirect('/login')

if __name__=='__main__':
    crear_usuario_por_defecto()
    app.run(debug=True)