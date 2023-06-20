from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from Estructuras.EnlazadaSimple import *
from Lectura import *
from usuario import *
from Estructuras.DobleEnlazada import *
from cine import *
from sala import *
from boleto import *
import xml.etree.ElementTree as ET
import os

lector = Lectura() #variable global
class Menu:
    listaUsuario = EnlazadaSimple()
    listaCine = ListaDobleEnlazada()
    listaSala = EnlazadaSimple()
    listaCategorias = EnlazadaSimple()
    listaPeliculas =    CicularDobleEnlazada()
    listaTarjeta = ListaDobleEnlazada()
    listaFavoritos = []
    listaAsientos = []  # Lista para almacenar los números de asientos seleccionados
    listaHistorial = []
    boletos = 0
    
    def __init__(self):
        self.console = Console()
        self.nombre_usuario = None
        self.contrasena = None
        self.admiPorDefecto() #para que se inicialice al ejecutar el programa
    
    def admiPorDefecto(self):
        #se crea el administrador por defecto al iniciar el programa
        rol = "administrador"
        nombre = "admi"
        apellido = "administrador por defecto"
        telefono = "3834657892"
        correo = " admi@gmail.com"
        contrasena = "123"
        self.listaUsuario.agregarUltimo(Usuario(rol,nombre,apellido,telefono,correo,contrasena))

    def mostrar_menu(self):
        console = Console()

        # Imprime el título del panel 
        print()
        title = Text("\t\t    BIENVENIDO USAC-cinema", style="bold")
        # Ajusta el padding izquierdo y derecho del panel
        panel = Panel(title, border_style="bold cyan", width=70, padding=(0, 2, 0, 2))
        console.print(panel)

        # Imprime las opciones del menú 
        console.print("\t[cyan]1. Iniciar sesión[/cyan]")
        console.print("\t[cyan]2. Registrar usuario[/cyan]")
        console.print("\t[cyan]3. Ver listado de películas[/cyan]")
        console.print("\t[red]4. Salir[/red]")

        while True: # Asegura que el menú se muestre repetidamente hasta que el usuario elija la opción de salir
            # Solicita al usuario que seleccione una opción del menú
            opcion = console.input("\n\tSeleccione una opción: ")

            if opcion == "1":
                console.print("\tHas seleccionado la opción 1.\n", style="green")

                while True:
                    title = Text("\t\t        INICIAR SESION", style="bold")
                    panel = Panel(title, border_style="bold green", width=70, padding=(0, 2, 0, 2))
                    console.print(panel)
                    console.print("\t[cyan]1. Iniciar sesión como administrador[/cyan]")
                    console.print("\t[cyan]2. Iniciar sesión como usuario[/cyan]")
                    console.print("\t[red]3. Volver al menú principal[/red]")

                    subopcion = console.input("\n\tSeleccione una opción del menú: ")

                    if subopcion == "1":
                        console.print("\tHas seleccionado Iniciar sesión como administrador.\n", style="green bold")
                        self.sesionAdmi()
                        print()
                        break

                    elif subopcion == "2":
                        console.print("\tHas seleccionado Iniciar sesión como usuario.\n", style="green")
                        # Iniciar sesión como usuario
                        self.sesionCliente()
                        print()
                        break

                    elif subopcion == "3":
                        console.print("\tVolviendo al menú principal...", style="bold yellow")
                        self.mostrar_menu()
                        break

                    else:
                        console.print("\tOpción inválida. Por favor, selecciona una opción válida.", style="bold red")

            elif opcion == "2": #REGISTRAR USUARIO
                console.print("\tHas seleccionado la opción 2.", style="green")
                self.registrarUsuario()
                print()
                break
                
            elif opcion == "3": #VER PELICULAS
                console.print("\tHas seleccionado la opción 3.", style="green")
                self.verPeliculas()
                print()
                break

            elif opcion == "4":
                console.print("\t¡Hasta luego!\n", style="bold red")
                exit(0)

            else:
                console.print("\tOpción inválida. Por favor, selecciona una opción válida.", style="bold red")

    def verPeliculas(self):
        if self.listaCategorias is not None:
            opcion = input("\t¿Desea ver el listado general de películas (G) o filtrar por categoría (C)? ").lower()
            
            if opcion == "g":
                self.listaCategorias.mostrarPeliculas()
            elif opcion == "c":
                categoria = input("\tIngrese el nombre de la categoría: ")
                self.listaCategorias.buscarUnaCategoria(categoria)
            else:
                print("\tOpción no válida. Por favor, seleccione 'G' para el listado general o 'C' para filtrar por categoría.")
            
            self.mostrar_menu()
        else:
            print("\tNo se encontraron datos disponibles.\n")

    def sesionCliente(self):
        self.listaFavoritos = []
        self.listaAsientos = []
        self.listaHistorial = []

        self.nombre_usuario = self.console.input("\tIngresa tu nombre de usuario: ")
        self.contrasena = self.console.input("\tIngresa tu contraseña: ")

        temp = self.listaUsuario.primero
        while temp:
            if temp.dato.rol == "cliente" and temp.dato.nombre == self.nombre_usuario and temp.dato.contrasena == self.contrasena:
                self.console.print("\n\tIngreso exitoso como cliente.\n", style="green")

            self.menuCliente()
            temp = temp.siguiente

        self.console.print("\tCredenciales incorrectas. Vuelve a intentarlo.\n", style="bold red")
        self.sesionCliente()

    def menuCliente(self): #CLIENTE
        title = Text("\t\t       MENU USUARIO", style="bold")
        # Ajusta el padding izquierdo y derecho del panel
        panel = Panel(title, border_style="bold yellow", width=70, padding=(0, 2, 0, 2))  
        self.console.print(panel)

        # Imprime las opciones del menú 
        self.console.print("\t[cyan]1. Ver listado de películas[/cyan]")
        self.console.print("\t[cyan]2.Listado de películas favoritas[/cyan]")
        self.console.print("\t[cyan]3.Comprar boletos[/cyan]")
        self.console.print("\t[cyan]4.Historial de boletos comprados[/cyan]")
        self.console.print("\t[red]5. Regresar[/red]")
        
        while True:  # asegura que el menú se muestre repetidamente hasta que el usuario elija la opción de salir
            # Solicita al usuario que seleccione una opción del menú
            opcion = self.console.input("\n\tSeleccione una opción: ")

            if opcion == "1":
                self.console.print("\tHas seleccionado la opción 1.", style="green")
                self.VerPeliculasCliente()
                print()
                break

            elif opcion == "2":
                self.console.print("\tHas seleccionado la opción 2", style="bold yellow")
                self.peliculasFavoritas()
                print()
                break

            elif opcion == "3":
                self.console.print("\tHas seleccionado la opción 3", style="bold yellow")
                self.comprarBoletos()
                print()
                break

            elif opcion == "4":
                self.console.print("\tHas seleccionado la opción 4", style="bold yellow")
                self.historialBoletos()
                print()
                break
            
            elif opcion == "5":
                self.console.print("\tVolviendo al menú principal...", style="bold yellow")
                print()
                self.mostrar_menu()

    def sesionAdmi(self):
        nombre_usuario = self.console.input("\tIngresa tu nombre de usuario: ")
        contrasena = self.console.input("\tIngresa tu contraseña: ")

        temp = self.listaUsuario.primero
        while temp:
            if temp.dato.rol == "administrador" and temp.dato.nombre == nombre_usuario and temp.dato.contrasena == contrasena:
                print()
                self.console.print("\tIngreso exitoso como administrador.\n", style="green")
                print()
                self.menuAdmi()  # Método para iniciar sesión como administrador
                return
            temp = temp.siguiente

        self.console.print("\tCredenciales incorrectas. Vuelve a intentarlo.\n", style="bold red")
        self.sesionAdmi()

    def menuAdmi(self):
        # Imprime el título del panel 
        title = Text("\t\t     MENU ADMINISTRADOR", style="bold")
        # Ajusta el padding izquierdo y derecho del panel
        panel = Panel(title, border_style="bold magenta", width=70, padding=(0, 2, 0, 2))  
        self.console.print(panel)

        # Imprime las opciones del menú 
        self.console.print("\t[cyan]1. Gestionar Usuarios[/cyan]")
        self.console.print("\t[cyan]2. Gestionar Categorías y películas[/cyan]")
        self.console.print("\t[cyan]3. Gestionar Salas[/cyan]")
        self.console.print("\t[cyan]4. Gestionar boletos comprados[/cyan]")
        self.console.print("\t[red]5. Regresar[/red]")
        
        while True:  # asegura que el menú se muestre repetidamente hasta que el usuario elija la opción de salir
            # Solicita al usuario que seleccione una opción del menú
            opcion = self.console.input("\n\tSeleccione una opción: ")

            if opcion == "1": #GESTION USUARIOS
                self.console.print("\tHas seleccionado la opción 1.\n", style="green")
                print()
                self.gestionUsuarios()
                break
            
            elif opcion == "2":#GESTION DE CATEGORIAS Y PELICULAS
                self.console.print("\tHas seleccionado la opción 2.\n", style="green")
                print()
                self.gestionarCategorias()
                break

            elif opcion == "3": #GESTIONAR SALAS
                self.console.print("\tHas seleccionado la opción 3.\n", style="green")
                print()
                self.gestionarSalas()
                break
                
            elif opcion == "4": #GESTIONAR BOLETOS
                self.console.print("\tHas seleccionado la opción 4.\n", style="green")
                print()
                self.gestionarBoletos()
                break

            elif opcion == "5": #SALIR PARA EL MENU DEL ADMINISTRADOR
                self.console.print("\tVolviendo al menú principal...", style="bold yellow")
                print()
                self.mostrar_menu()

            else:
                self.console.print("\tOpción inválida. Por favor, selecciona una opción válida.\n", style="bold red")
                print()
                self.menuAdmi()
                break

    def registrarUsuario(self): #Clientes unicamente
        self.console.print("[cyan]\n\tIngrese los datos para el usuario nuevo: \n[/cyan]")

        rol = "cliente"
        nombre = input("\tNombre: ")
        apellido = input("\tApellido: ")
        telefono = input("\tTeléfono: ")
        correo = input("\tCorreo: ")
        contrasena = input("\tContraseña: ")

        # Validar si el correo ya existe en la lista
        if self.listaUsuario.buscarPorCorreo(correo) is not None:
            self.console.print("[red]\n\tYa existe un usuario con el correo ingresado.[/red]\n")
        else:
            self.listaUsuario.agregarUltimo(Usuario(rol, nombre, apellido, telefono, correo, contrasena))
            self.console.print("[green]\n\tUsuario agregado con éxito.[/green]\n")
        self.mostrar_menu()

    def gestionUsuarios(self):
        while True:
                    title = Text("\t\t       GESTIONAR USUARIOS", style="bold")
                    panel = Panel(title, border_style="bold magenta", width=70, padding=(0, 2, 0, 2))  
                    self.console.print(panel)
                    self.console.print("\t[cyan]1. Cargar Archivo [/cyan]")
                    self.console.print("\t[cyan]2. Crear usuario[/cyan]")
                    self.console.print("\t[cyan]3. Modificar usuario[/cyan]")
                    self.console.print("\t[cyan]4. Eliminar usuario[/cyan]")
                    self.console.print("\t[cyan]5. Mostrar usuarios[/cyan]")
                    self.console.print("\t[cyan]6. Generar xml[/cyan]")
                    self.console.print("\t[red]7. Volver al menú principal[/red]")
                        
                    subopcion = self.console.input("\n\tSeleccione una opción: ")

                    if subopcion == "1":
                        self.console.print("\tHas seleccionado cargar archivo.\n", style="green")
                        self.cargarArchivoUsuario()

                    elif subopcion == "2":
                        self.console.print("\tHas seleccionado crear usuario.\n", style="green")
                        self.agregarUsuario()
                        
                    elif subopcion == "3":
                        self.console.print("\tHas seleccionado Modificar usuario.\n", style="green")
                        self.modificarUsuario()
                        
                    elif subopcion == "4":
                        self.console.print("\tHas seleccionado Eliminar usuarios.\n", style="green")
                        self.eliminarUsuario()
                        
                    elif subopcion == "5":
                        self.console.print("\tHas seleccionado Mostrar usuario.\n", style="green")
                        self.mostrarUsuario()
                        
                    elif subopcion == "6": #GENERAR XML SALIDA
                        self.console.print("\tHas seleccionado la opción Generar xml\n", style="green")
                        print()
                        self.xml_Usuarios()
                        self.gestionUsuarios()
                        break
                    
                    elif subopcion == "7":
                        self.console.print("\tVolviendo al menú principal...", style="bold yellow")
                        print()
                        self.menuAdmi()

                    else:
                        self.console.print("\tOpción inválida. Por favor, selecciona una opción válida.\n", style="bold red")

    def cargarArchivoUsuario(self):
        console = Console()
        while True:
            console.print("\tIngrese la ruta del archivo: ", style="bold yellow")
            ruta = input('\t »  ')
            
            datosArchivo = lector.lecturaU(ruta)
            
            if self.listaUsuario.estaVacia():
                # Si la lista está vacía, simplemente asignar los datos del archivo a la lista
                self.listaUsuario = datosArchivo
            else:
                # Si la lista no está vacía, agregar los datos del archivo al final de la lista existente
                ultimoNodo = self.listaUsuario.ultimo
                ultimoNodo.siguiente = datosArchivo.primero
                self.listaUsuario.ultimo = datosArchivo.ultimo
            
            console.print("\t[green]Archivo cargado exitosamente.[/green]")

            opcion = input("\n\tDesea agregar otro archivo? (s/n): ")
            if opcion.lower() != "s\n":
                break
        self.gestionUsuarios()

    def agregarUsuario(self):
        self.console.print("[cyan]\tIngrese los datos del usuario: [/cyan]")

        rol = input("\tRol: ")
        nombre = input("\tNombre: ")
        apellido = input("\tApellido: ")
        telefono = input("\tTeléfono: ")
        correo = input("\tCorreo: ")
        contrasena = input("\tContraseña: ")

        # Validar si el correo ya existe en la lista
        if self.listaUsuario.buscarPorCorreo(correo) is not None:
            self.console.print("[red]\n\tYa existe un usuario con el correo ingresado.[/red]\n")
        else:
            self.listaUsuario.agregarUltimo(Usuario(rol, nombre, apellido, telefono, correo, contrasena))
            self.console.print("[green]\n\tUsuario agregado con éxito.[/green]\n")
        self.gestionUsuarios()

    def modificarUsuario(self):
        self.console.print("[cyan]\tIngrese el correo del usuario el cual desea modificar: [/cyan]")
        correo = input("\tCorreo: ")
        self.listaUsuario.modificarPorCorreo(correo)

    def eliminarUsuario(self):
        self.console.print("[cyan]\tIngrese el correo del usuario el cual desea eliminar: [/cyan]")
        correo = input("\tCorreo: ")
        self.listaUsuario.eliminarPorCorreo(correo)

    def mostrarUsuario(self):
        if self.listaUsuario is not None:
            self.listaUsuario.recorrer()
        else:
            print("\tNo se encontraron datos disponibles.\n")

    def gestionarSalas(self):
        while True:
                    title = Text("\t\t        GESTIONAR SALAS", style="bold")
                    panel = Panel(title, border_style="bold magenta", width=70, padding=(0, 2, 0, 2))  
                    self.console.print(panel)
                    self.console.print("\t[cyan]1. Cargar Archivo [/cyan]")
                    self.console.print("\t[cyan]2. Añadir cine[/cyan]")
                    self.console.print("\t[cyan]3. Modificar cine[/cyan]")
                    self.console.print("\t[cyan]4. Eliminar cine[/cyan]")
                    self.console.print("\t[cyan]5. Mostrar cines[/cyan]")
                    self.console.print("\t[cyan]6. Generar xml[/cyan]")
                    self.console.print("\t[red]7. Volver al menú principal[/red]")
                        
                    subopcion = self.console.input("\n\tSeleccione una opción: ")

                    if subopcion == "1":
                        self.console.print("\tHas seleccionado cargar archivo.\n", style="green")
                        self.cargarArhivosSala()

                    elif subopcion == "2":
                        self.console.print("\tHas seleccionado Añadir cine.\n", style="green")
                        self.agregarSala()
                        
                    elif subopcion == "3":
                        self.console.print("\tHas seleccionado Modificar cine.\n", style="green")
                        self.modificarSala()
                        
                    elif subopcion == "4":
                        self.console.print("\tHas seleccionado Eliminar cine.\n", style="green")
                        self.eliminarSala()
                        
                    elif subopcion == "5":
                        self.console.print("\tHas seleccionado Mostrar cine.\n", style="green")
                        self.mostrarSala()
                        
                    elif subopcion == "6": #GENERAR XML SALIDA
                        self.console.print("\tHas seleccionado la opción Generar xml\n", style="green")
                        print()
                        self.xml_Salas()
                        self.gestionarSalas()
                        break

                    elif subopcion == "7":
                        self.console.print("\tVolviendo al menú principal...", style="bold yellow")
                        print()
                        self.menuAdmi()

                    else:
                        self.console.print("\tOpción inválida. Por favor, selecciona una opción válida.\n", style="bold red")

    def cargarArhivosSala(self):
        console = Console()
        lector = Lectura()  # Crear una instancia de la clase Lectura
        while True:
            console.print("\tIngrese la ruta del archivo: ", style="bold yellow")
            ruta = input('\t »  ')
            
            resultado = lector.lecturaS(ruta)  # Obtener el resultado de la función lecturaS

            if resultado is not None:
                self.listaCine, self.listaSala = resultado  # Desempaquetar los resultados en las variables
                console.print("\t[green]Archivo cargado exitosamente.[/green]")
            else:
                console.print("\t[red]Error al cargar el archivo.[/red]")
            
            opcion = input("\n\tDesea agregar otro archivo? (s/n): ")
            if opcion.lower() != "s\n":
                break
        self.gestionarSalas()

    def agregarSala(self):
        self.console.print("[cyan]\n\tIngrese los datos para el cine nuevo: \n[/cyan]")

        nombre = input("\tNombre del cine: ")

        # Buscar el cine por nombre en la lista
        cine = self.listaCine.buscarCine(nombre)

        if cine is not None:
            opcion = input("\n\tEl cine ya existe. ¿Desea agregar más salas al cine? (s/n): ")
            if opcion.lower() == "s":
                while True:
                    numero = input("\tNúmero de sala: ")
                    asientos = input("\tCantidad de asientos: ")

                    sala = Sala(numero, asientos)

                    cine.sala.agregarUltimo(sala)

                    opcion = input("\n\t¿Desea agregar otra sala al cine? (s/n): ")
                    print()
                    if opcion.lower() != "s":
                        break
                self.console.print("[green]\n\tSalas agregadas con éxito al cine existente.[/green]\n")
            else:
                self.console.print("[yellow]\n\tNo se agregaron nuevas salas al cine existente.[/yellow]\n")
        else:
            # El cine no existe, se agrega uno nuevo con su lista de salas
            salas = EnlazadaSimple()
            while True:
                numero = input("\tNúmero de sala: ")
                asientos = input("\tCantidad de asientos: ")

                sala = Sala(numero, asientos)

                salas.agregarUltimo(sala)

                opcion = input("\n\t¿Desea agregar otra sala al cine? (s/n): ")
                if opcion.lower() != "s":
                    break
            self.listaCine.agregarUltimo(Cine(nombre, salas))
            self.console.print("[green]\n\tCine y salas agregados con éxito.[/green]\n")

        self.gestionarSalas()

        self.gestionarSalas()

    def modificarSala(self):
        self.console.print("[cyan]\tIngrese el nombre del cine el cual desea modificar: [/cyan]")
        cine = input("\tNombre del Cine: ")
        self.listaCine.modificarPorCine(cine)

    def eliminarSala(self):
        self.console.print("[cyan]\tIngrese el nombre del cine el cual desea eliminar: [/cyan]")
        cine = input("\tNombre del Cine: ")
        self.listaCine.eliminarPorCine(cine)

    def mostrarSala(self):
        if self.listaCine is not None:
            self.listaCine.recorrerInicio()
        else:
            print("\tNo se encontraron datos disponibles.\n")

    def gestionarCategorias(self):
        while True:
                    title = Text("\t\t   GESTIONAR CATEGORIAS Y PELICULAS", style="bold")
                    panel = Panel(title, border_style="bold magenta", width=70, padding=(0, 2, 0, 2))  
                    self.console.print(panel)
                    self.console.print("\t[cyan]1. Cargar Archivo [/cyan]")
                    self.console.print("\t[cyan]2. Añadir pelicula[/cyan]")
                    self.console.print("\t[cyan]3. Modificar pelicula[/cyan]")
                    self.console.print("\t[cyan]4. Eliminar pelicula[/cyan]")
                    self.console.print("\t[cyan]5. Mostrar peliculas[/cyan]")
                    self.console.print("\t[cyan]6. Generar xml[/cyan]")
                    self.console.print("\t[red]7. Volver al menú principal[/red]")
                        
                    subopcion = self.console.input("\n\tSeleccione una opción: ")

                    if subopcion == "1":
                        self.console.print("\tHas seleccionado cargar archivo.\n", style="green")
                        self.cargarArhivosCategorias()

                    elif subopcion == "2":
                        self.console.print("\tHas seleccionado Añadir pelicula.\n", style="green")
                        self.agregarCategoria()
                        
                    elif subopcion == "3":
                        self.console.print("\tHas seleccionado Modificar pelicula.\n", style="green")
                        self.modificarCategoria()
                        
                    elif subopcion == "4":
                        self.console.print("\tHas seleccionado Eliminar pelicula.\n", style="green")
                        self.eliminarCategoria()
                        
                    elif subopcion == "5":
                        self.console.print("\tHas seleccionado Mostrar peliculas.\n", style="green")
                        self.mostrarCategoria()

                    elif subopcion == "6": #GENERAR XML SALIDA
                        self.console.print("\tHas seleccionado la opción Generar xml\n", style="green")
                        print()
                        self.xml_Categorias()
                        self.gestionarCategorias()
                        break

                    elif subopcion == "7":
                        self.console.print("\tVolviendo al menú principal...\n", style="bold yellow")
                        self.menuAdmi()

                    else:
                        self.console.print("\tOpción inválida. Por favor, selecciona una opción válida.\n", style="bold red")

    def cargarArhivosCategorias(self):
        console = Console()
        lector = Lectura()
        while True:
            console.print("\tIngrese la ruta del archivo: ", style="bold yellow")
            ruta = input('\t »  ')
            
            resultado = lector.lecturaCP(ruta)
            
            if resultado is not None:
                categorias_nuevas, peliculas_nuevas = resultado
                if self.listaCategorias.estaVacia():
                    self.listaCategorias = categorias_nuevas
                else:
                    temp = categorias_nuevas.primero
                    while temp:
                        self.listaCategorias.agregarUltimo(temp.dato)
                        temp = temp.siguiente
                console.print("\t[green]Archivo cargado exitosamente.[/green]")
            else:
                console.print("\t[red]Error al cargar el archivo.[/red]")
            
            opcion = input("\n\tDesea agregar otro archivo? (s/n): ")
            if opcion.lower() != "s":
                break

        self.gestionarCategorias()

    def agregarCategoria(self):
        self.console.print("[cyan]\n\tIngrese los datos para la categoría nueva: \n[/cyan]")

        nombre = input("\tNombre de la categoría: ")
        categoria = self.listaCategorias.buscarPorCategoria(nombre)

        if categoria is not None:
            opcion = input("\n\tLa categoría ya existe. ¿Desea agregar más películas a la categoría? (s/n): ")
            if opcion.lower() == "s":
                while True:
                    titulo = input("\tTítulo de la película: ")
                    director = input("\tDirector de la película: ")
                    anio = input("\tAño de la película: ")
                    fecha = input("\tFecha de la película: ")
                    hora = input("\tHora de la película: ")
                    imagen = input("\tImagen de la película: ")
                    precio = float(input("\tPrecio de la película (Q):"))

                    pelicula = Pelicula(titulo, director, anio, fecha, hora,imagen, precio)

                    categoria.peliculas.agregarFinal(pelicula)  # Agrega la película a la doble circular enlazada

                    opcion = input("\n\t¿Desea agregar otra película? (s/n): ")
                    print()
                    if opcion.lower() != "s":
                        break
                self.console.print("[green]\n\tPelículas agregadas con éxito a la categoría existente.[/green]\n")
            else:
                self.console.print("[yellow]\n\tNo se agregaron nuevas películas a la categoría existente.[/yellow]\n")
        else:
            # La categoría no existe, se crea una nueva con su lista de películas
            peliculas = CicularDobleEnlazada()  # Crear instancia de CicularDobleEnlazada
            while True:
                titulo = input("\tTítulo de la película: ")
                director = input("\tDirector de la película: ")
                anio = input("\tAño de la película: ")
                fecha = input("\tFecha de la película: ")
                hora = input("\tHora de la película: ")
                imagen = input("\tImagen de la película: ")
                precio = float(input("\tPrecio de la película (Q):"))

                pelicula = Pelicula(titulo, director, anio, fecha, hora,imagen, precio)

                peliculas.agregarFinal(pelicula)  # Agrega la película a la doble circular enlazada

                opcion = input("\n\t¿Desea agregar otra película? (s/n): ")
                print()
                if opcion.lower() != "s":
                    break
            nueva_categoria = Categoria(nombre, peliculas)
            self.listaCategorias.agregarUltimo(nueva_categoria)
            self.console.print("[green]\n\tCategoría y películas agregadas con éxito.[/green]\n")

    def modificarCategoria(self):
        self.console.print("[cyan]\tIngrese el nombre de la categoria  cual desea modificar: [/cyan]")
        categoria = input("\tNombre de la categoria: ")
        self.listaCategorias.buscarCategoria(categoria)

    def eliminarCategoria(self):
        self.console.print("[cyan]\tIngrese el nombre de la categoria la cual desea eliminar: [/cyan]")
        nombre = input("\tNombre de la categoria: ")
        self.listaCategorias.eliminarPorCategoria(nombre)

    def mostrarCategoria(self):
        if self.listaCategorias is not None:
            self.listaCategorias.recorrerCategorias()
        else:
            print("\tNo se encontraron datos disponibles.\n")

    def gestionarBoletos(self): #ADMINISTRADOR
        # Imprimir los números de boleto disponibles
        print("\n\tNúmeros de boleto disponibles:")
        for boleto in self.listaHistorial:
            print("\t"+ boleto.numero_boleto)

        boletoCancelado = input("\n\tIngrese el numero de boleto que desea cancelar: ")
        self.cancelarBoleto(boletoCancelado)

    def VerPeliculasCliente(self): #CLIENTE
        if self.listaCategorias is not None:
            print()
            title = Text("\t\t    VER LISTADO DE PELICULAS", style="bold")
            # Ajusta el padding izquierdo y derecho del panel
            panel = Panel(title, border_style="bold yellow", width=70, padding=(0, 2, 0, 2))  
            self.console.print(panel)
            self.console.print("[cyan]\n\t1. Ver el listado general de películas[/cyan]")
            self.console.print("[cyan]\t2. Filtrar por categoría[/cyan]")
            self.console.print("[cyan]\t3. Ver detalles de una película[/cyan]")
            self.console.print("[red]\t4. Regresar[/red]")
            
            opcion = input("\n\tSeleccione una opción:")

            if opcion == "1":
                self.listaCategorias.mostrarPeliculas()
            elif opcion == "2":
                categoria = input("\tIngrese el nombre de la categoría: ")
                self.listaCategorias.buscarUnaCategoria(categoria)
            elif opcion == "3":
                categoria = input("\tIngrese el nombre de la categoría: ")
                categoria_actual = self.listaCategorias.buscarPorCategoria(categoria)
                if categoria_actual is not None:
                    titulo = input("\tIngrese el título de la película: ")
                    categoria_actual.pelicula.buscarPeliculaPorNombre(titulo)
                else:
                    print("\tLa categoría no se encontró en la lista.")
            elif opcion == "4":
                self.console.print("\tVolviendo al menú principal...", style="bold yellow")
                self.menuCliente()
                print()
            else:
                print("\tOpción no válida. Por favor, seleccione una opción válida.")
            
            self.VerPeliculasCliente()
        else:
            print("\tNo se encontraron datos disponibles.\n")
            self.menuCliente()
    
    def peliculasFavoritas(self): #sub menu de ver peliculas cliente
        if self.listaCategorias is not None:
            print()
            title = Text("\t\t  LISTADO DE PELICULAS FAVORITAS", style="bold")
            # Ajusta el padding izquierdo y derecho del panel
            panel = Panel(title, border_style="bold yellow", width=70, padding=(0, 2, 0, 2))  
            self.console.print(panel)
            self.console.print("[cyan]\n\t1. Agregar peliculas favoritas[/cyan]")
            self.console.print("[cyan]\t2. Ver listado de peliculas favoritas[/cyan]")
            self.console.print("[red]\t3. Regresar[/red]")
            
            opcion = input("\n\tSeleccione una opción:")

            if opcion == "1":
                self.agregarFavorito()
                print()
            if opcion == "2":
                self.verPeliculaFavorito()
                self.peliculasFavoritas()
                print()
            if opcion == "3":
                self.console.print("\tVolviendo al menú principal...", style="bold yellow")
                self.menuCliente()
                print()
            else:
                print("\tOpción no válida. Por favor, seleccione una opción válida.")
                self.peliculasFavoritas()

    def agregarFavorito(self): #sub menu de ver peliculas cliente
        categoria = input("\tIngrese el nombre de la categoría: ")
        # Buscar la categoría en la lista enlazada de categorías
        categoria_actual = self.listaCategorias.buscarPorCategoria(categoria)
        if categoria_actual is not None:
            # Mostrar las películas de la categoría encontrada
            categoria_actual.pelicula.verSoloPeliculas()
            # Solicitar el nombre de la película para agregar a favoritos
            nombre_pelicula = input("\n\tIngrese el nombre de la película: ")
            self.listaFavoritos.append(nombre_pelicula)
            print("\tLa película se ha agregado a la lista de favoritos.")
        else:
            print("\tLa categoría no se encontró en la lista.")

        self.peliculasFavoritas()

    def verPeliculaFavorito(self): #sub menu de ver peliculas cliente
        print("\n\t====================Peliculas Favoritas====================\n")
        if len(self.listaFavoritos) > 0:
            contador = 1
            for pelicula in self.listaFavoritos:
                print("\t{}. {}".format(contador, pelicula))
                contador += 1
        else:
            print("\n\tNo hay películas favoritas en la lista.")

    def comprarBoletos(self):
        print()
        title = Text("\t\t  COMPRAR BOLETOS", style="bold")
        # Ajusta el padding izquierdo y derecho del panel
        panel = Panel(title, border_style="bold yellow", width=70, padding=(0, 2, 0, 2))
        self.console.print(panel)

        print("\n\t====================CINE==================\n")
        self.listaCine.recorrerInicio()  # Retorna los datos
        print("\n\t===========================================================\n")

        cine = input("\n\tSeleccione Cine de su preferencia: ")
        cine_actual = self.listaCine.buscarCine(cine)

        if cine_actual is not None:
            sala = input("\tIngrese el número de sala de su preferencia: ")
            sala_encontrada = cine_actual.sala.buscarPorSala(sala)

            if sala_encontrada is not None:
                rango_asientos = range(1, int(sala_encontrada.asientos) + 1)  # Rango de asientos disponibles (convertido a entero)

                numero_asiento = int(input("\tIngrese el número de asiento de su preferencia: "))

                if numero_asiento in rango_asientos:
                    if numero_asiento not in self.listaAsientos:
                        self.listaAsientos.append(numero_asiento)
                        print("\n\tAsiento seleccionado: ", numero_asiento)

                        print("\n\t====================Peliculas Disponibles==================\n")
                        self.listaCategorias.mostrarPeliculas()
                        print("\n\t===========================================================\n")

                        categoria = input("\tIngrese el nombre de la categoría: ")
                        categoria_actual = self.listaCategorias.buscarPorCategoria(categoria)
                        if categoria_actual is not None:
                            titulo = input("\tIngrese el título de la película: ")
                            pelicula_encontrada = categoria_actual.pelicula.buscarPeliculaParaBoleto(titulo)
                            if pelicula_encontrada is not None:
                                num_boletos = int(input("\n\tIngrese la cantidad de boletos a comprar: "))
                                totalCompra = pelicula_encontrada.precio * num_boletos
                                self.boletos += 1  # Incrementar el número de boleto
                                self.generarFactura(categoria,cine_actual.nombre, titulo, num_boletos,sala, self.boletos, totalCompra, numero_asiento)  # Generar factura con los detalles de la compra
                            else:
                                print("\n\tNo se encontró la película especificada")
                                self.comprarBoletos()
                        else:
                            print("\n\tNo se encontró la categoría especificada")
                            self.comprarBoletos()
                    else:
                        print("\n\tEl asiento ya está ocupado por otro usuario")
                        self.comprarBoletos()
                else:
                    print("\n\tEl número de asiento ingresado no es válido")
                    self.comprarBoletos()
            else:
                print("\n\tNo se encontró la sala especificada")
                self.comprarBoletos()
        else:
            print("\n\tNo se encontró el cine especificado")
            self.comprarBoletos()

    def generarFactura(self, categoria, cine, pelicula, num_boletos,sala, boletos, total, numero_asiento):
        nombre = input("\tIngrese el nombre para la factura: ")
        if nombre == "C/F":
            print("\n\n\t======================== FACTURA =======================")
            print("\tCine: ", cine)
            print("\tNúmero de boleto: ", "#USACIPC2_202000558_" + str(boletos))  # Número de boleto con formato
            print("\tNombre:" + nombre)
            print("\tPelícula: ", pelicula)

            categoria_actual = self.listaCategorias.buscarPorCategoria(categoria)
            peli = categoria_actual.pelicula.buscarPeli(pelicula)

            fecha = peli.fecha
            hora = peli.hora
            print("\tFecha función: ", fecha)
            print("\tHora función: ", hora)
            print("\tNúmero de sala: ", sala)
            print("\n\tNúmero de boletos: ", num_boletos)
            print("\tNúmero de asiento: ", numero_asiento)
            print("\tTotal a pagar: Q", total)
            print("\n\t¡Gracias por su compra!")
            print("\n\t===========================================================\n")

            # Agregar boleto al historial
            boleto = Boleto(nombre, cine, "#USACIPC2_202000558_" + str(boletos), pelicula, fecha, hora, num_boletos,sala, numero_asiento, total,False)
            self.listaHistorial.append(boleto)
            self.menuCliente()
        else:
            NIT = input("\tIngrese el NIT para la factura: ")
            direccion = input("\tDirección: ")

            print("\n\n\t======================== FACTURA ========================\n")
            print("\tCine: ", cine)
            print("\tNúmero de boleto: ", "#USACIPC2_202000558_" + str(boletos))  # Número de boleto con formato
            print("\tNombre:" + nombre)
            print("\tNIT:" + NIT)
            print("\tDirección:" + direccion)
            print("\tNúmero de sala: ", sala)
            print("\tPelícula: ", pelicula)

            categoria_actual = self.listaCategorias.buscarPorCategoria(categoria)
            peli = categoria_actual.pelicula.buscarPeli(pelicula)

            fecha = peli.fecha
            hora = peli.hora
            print("\tFecha función: ", fecha)
            print("\tHora función: ", hora)
            print("\tNúmero de boletos: ", num_boletos)
            print("\tNúmero de asiento: ", numero_asiento)
            print("\tTotal a pagar: Q", total)
            print("\n\t¡Gracias por su compra!")
            print("\n\t===========================================================\n")

            # Agregar boleto al historial
            boleto = Boleto(nombre, cine, "#USACIPC2_202000558_" + str(boletos), pelicula, fecha, hora, num_boletos,sala, numero_asiento, total,False)
            self.listaHistorial.append(boleto)
            self.menuCliente()

    def historialBoletos(self):
        if len(self.listaHistorial) == 0:
            print("\n\tEl historial de boletos está vacío.")
        else:
            print("\n\n\t==================== HISTORIAL DE BOLETOS ====================")
            for boleto in self.listaHistorial:
                print("\n\tNombre:", boleto.nombre)
                print("\tCine:", boleto.cine)
                print("\tNúmero de boleto:", boleto.numero_boleto)
                print("\tNúmero de sala: ", boleto.sala_encontrada)
                print("\tPelícula:", boleto.pelicula)
                print("\tFecha función:", boleto.fecha_funcion)
                print("\tHora función:", boleto.hora_funcion)
                print("\tNúmero de boletos:", boleto.num_boletos)
                print("\tNúmero de asiento:", boleto.numero_asiento)
                print("\tMonto pagado: Q", boleto.monto_pagado) 
                estado = "Cancelado" 
                if boleto.cancelado:
                    print("\tEstado:", estado)
                print("\n\t==============================================================\n")
        
        #Verifica si se estan agregando la lista de peliculas al usuario y historial de boletos
        temp = self.listaUsuario.primero
        while temp:
            if temp.dato.nombre == self.nombre_usuario and temp.dato.contrasena == self.contrasena:
                self.agregarHistorialFavoritos(self.nombre_usuario , self.contrasena)
                #self.listaUsuario.mostrarUsuario()
            temp = temp.siguiente
        self.menuCliente()

    def cancelarBoleto(self, numero_boleto):
        boleto_encontrado = None
        for boleto in self.listaHistorial:
            if boleto.numero_boleto == numero_boleto:
                boleto_encontrado = boleto
                break
        if boleto_encontrado:
            boleto_encontrado.cancelado = True
            print("\n\t¡El boleto ha sido cancelado exitosamente!")
        else:
            print("\n\tNo se encontró ningún boleto con el número proporcionado.")
        
        self.menuAdmi()

    def agregarHistorialFavoritos(self, nombre_usuario, contrasena):
        # Buscar el nodo del usuario que inició sesión
        temp = self.listaUsuario.primero
        while temp:
            if  temp.dato.nombre == nombre_usuario and temp.dato.contrasena == contrasena:
                # Añadir el historial de boletos y las películas favoritas al nodo del usuario
                temp.dato.historial_Boletos = self.listaHistorial
                temp.dato.peliculas_Favoritas = self.listaFavoritos
                #self.console.print("\n\tHistorial de boletos y películas favoritas añadidos al usuario.", style="green")
                self.nombre_usuario = None
                self.contrasena = None
                return
            temp = temp.siguiente

        #self.console.print("\n\tUsuario no encontrado. No se pudo agregar el historial y las películas favoritas.", style="bold red")                                

    def xml_Usuarios(self):
        # Nombre de la carpeta para almacenar los archivos XML
        carpeta = "archivos_salida"

        # Crear la carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Crear el elemento raíz del XML
        root = ET.Element("usuarios")

        # Recorrer la lista de usuarios y crear elementos XML para cada usuario
        temp = self.listaUsuario.primero
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

                nombre_boleto = ET.SubElement(boleto_element, "nombre")
                nombre_boleto.text = boleto.nombre

                cine = ET.SubElement(boleto_element, "cine")
                cine.text = boleto.cine

                numero_boleto = ET.SubElement(boleto_element, "numero_boleto")
                numero_boleto.text = boleto.numero_boleto

                pelicula = ET.SubElement(boleto_element, "pelicula")
                pelicula.text = boleto.pelicula

                fecha_funcion = ET.SubElement(boleto_element, "fecha_funcion")
                fecha_funcion.text = boleto.fecha_funcion

                hora_funcion = ET.SubElement(boleto_element, "hora_funcion")
                hora_funcion.text = boleto.hora_funcion

                num_boletos = ET.SubElement(boleto_element, "num_boletos")
                num_boletos.text = str(boleto.num_boletos)

                sala_encontrada = ET.SubElement(boleto_element, "sala_encontrada")
                sala_encontrada.text = boleto.sala_encontrada

                numero_asiento = ET.SubElement(boleto_element, "numero_asiento")
                numero_asiento.text = str(boleto.numero_asiento)

                monto_pagado = ET.SubElement(boleto_element, "monto_pagado")
                monto_pagado.text = str(boleto.monto_pagado)

                cancelado = ET.SubElement(boleto_element, "estado_boleto")
                estado = "Cancelado" if boleto.cancelado else "Activo"
                cancelado.text = estado

            temp = temp.siguiente

        # Combinar la ruta de la carpeta con el nombre del archivo XML
        ruta_archivo = os.path.join(carpeta, "usuarios.xml")

        # Convertir el árbol XML en una cadena con formato
        xml_string = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

        # Escribir la cadena con formato en el archivo
        with open(ruta_archivo, "w") as file:
            file.write(xml_string)

    def xml_Categorias(self):
        # Nombre de la carpeta para almacenar los archivos XML
        carpeta = "archivos_salida"

        # Crear la carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Crear el elemento raíz del XML
        root = ET.Element("categorias")

        temp = self.listaCategorias.primero
        while temp is not None:
            # Crea el elemento categoria
            categoria = ET.Element("categoria")

            # Crea el elemento nombre_categoria y agrega el nombre
            nombre_categoria = ET.SubElement(categoria, "nombre")
            nombre_categoria.text = temp.dato.nombre

            # Crea el elemento de peliculas
            peliculas = ET.SubElement(categoria, "peliculas")

            # Buscar la categoría en la lista de categorías por nombre
            categoria_buscada = self.listaCategorias.buscarPorCategoria(temp.dato.nombre)
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
            if temp == self.listaCategorias.primero:
                break

        # Combinar la ruta de la carpeta con el nombre del archivo XML
        ruta_archivo = os.path.join(carpeta, "categorias.xml")

        # Convertir el árbol XML en una cadena con formato
        xml_string = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

        # Escribir la cadena con formato en el archivo
        with open(ruta_archivo, "w") as file:
            file.write(xml_string)

    def xml_Salas(self):
        # Nombre de la carpeta para almacenar los archivos XML
        carpeta = "archivos_salida"

        # Crear la carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Crear el elemento raíz del XML
        root = ET.Element("cines")

        temp = self.listaCine.primero
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