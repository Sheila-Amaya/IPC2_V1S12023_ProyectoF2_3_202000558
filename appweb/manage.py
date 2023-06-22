from flask import Flask, redirect, render_template, request
from Lectura import *
from Estructuras.EnlazadaSimple import *
from usuario import *

app = Flask(__name__)

# Declarar una variable global como una instancia de EnlazadaSimple
listaUsuarios = EnlazadaSimple()

def crear_usuario_por_defecto():
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

@app.route('/logout')
def logout():
    #...
    return redirect('/login')

if __name__=='__main__':
    crear_usuario_por_defecto()
    app.run(debug=True)