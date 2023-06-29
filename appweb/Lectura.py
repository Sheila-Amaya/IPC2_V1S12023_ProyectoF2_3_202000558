import xml.etree.ElementTree as ET

from flask import request
from Estructuras.EnlazadaSimple import *
from usuario import *
from Estructuras.DobleEnlazada import *
from cine import *
from sala import *
from Estructuras.DobleEnlazadaCircular import *
from categoria import *
from pelicula import *
from tarjeta import *
import requests

class Lectura:
    
    def lecturaU(self,dato): #GESTIONAR USUARIOS > LISTA SIMPLE
        
        try:
            tree = ET.parse(dato)
            root = tree.getroot()
            
            listaUsuario = EnlazadaSimple()
            
            # API Obtener los datos de la API
            response = requests.get('http://localhost:5000/getUsuarios')
            if response.status_code == 200:
                usuarios_API = response.json()
                for usuario_api in usuarios_API:
                    usuario = Usuario(
                        usuario_api['rol'],
                        usuario_api['nombre'],
                        usuario_api['apellido'],
                        usuario_api['telefono'],
                        usuario_api['correo'],
                        usuario_api['contrasena']
                    )
                    listaUsuario.agregarUltimo(usuario)
                    print(usuario_api)
                    
            for elemento in root: #root etiqueta usuarios
                
                #USUARIO
                rol = ""
                nombre = ""
                apellido = ""
                telefono = ""
                correo = ""
                contrasena = ""
                
                if elemento.tag == "usuario":
                    for subelememto in elemento: #sub elemento son las etiquetas dentro de usuario
                        #print(subelememto)
                        if subelememto.tag == "rol":
                            rol = subelememto.text
                        elif subelememto.tag == "nombre":
                            nombre = subelememto.text
                        elif subelememto.tag == "apellido":
                            apellido = subelememto.text
                        elif subelememto.tag == "telefono":
                            telefono = subelememto.text
                        elif subelememto.tag == "correo":
                            correo = subelememto.text
                        elif subelememto.tag == "contrasena":
                            contrasena = subelememto.text
                    listaUsuario.agregarUltimo(Usuario(rol,nombre,apellido,telefono,correo,contrasena))
                
            #clistaUsuario.recorrer()
                
            #correo = input("ingrese el correo: ")
            #listaUsuario.eliminarPorBusqueda(correo)
            #listaUsuario.eliminarPorBusqueda(correo)
            #listaUsuario.modificarPorCorreo(correo)
            #listaUsuario.recorrer()
            return listaUsuario

        except:
            print(' Error al cargar el archivo...\n')  # Mensaje de error cuando ocurre una excepción al cargar el archivo

    def lecturaS(self, dato): #SALAS > DOBLEMENTE ENLAZADA
        try:
            tree = ET.parse(dato)
            root = tree.getroot()

            listaCine = ListaDobleEnlazada()

            # API Obtener los datos de la API
            response = requests.get('http://localhost:5000/getCine')
            if response.status_code == 200:
                salasAPI = response.json()
                listaCine = ListaDobleEnlazada()
                
                cineAPI = salasAPI['cine']
                nombre_cine = cineAPI['nombre']
                salas_cine = EnlazadaSimple()
                datos_sala = cineAPI['salas']['sala']
                for sala in datos_sala:
                    numero = sala['numero']
                    asientos = sala['asientos']
                    salas_cine.agregarUltimo(Sala(numero, asientos))
                listaCine.agregarUltimo(Cine(nombre_cine, salas_cine))
                        
            for elemento in root: #raiz = cines
                #CINE
                nombre = ""
                #SALAS
                salas = EnlazadaSimple()

                if elemento.tag == "cine":
                    for subelemento in elemento: # etiquetas dentro de cine, nombre, salas
                        if subelemento.tag == "nombre":
                            nombre = subelemento.text
                        if subelemento.tag == "salas":
                            for sub in subelemento:
                                if sub.tag == "sala": 
                                    numero = ""
                                    asientos = ""
                                    for s in sub:
                                        if s.tag == "numero":
                                            numero = s.text
                                        if s.tag == "asientos":
                                            asientos = s.text
                                    salas.agregarUltimo(Sala(numero, asientos))
                    listaCine.agregarUltimo(Cine(nombre, salas))

            #listaCine.recorrerInicio()
            #cine = input("ingrese el cine: ")
            #listaCine.eliminarPorCine(cine)
            #listaCine.modificarPorCine(cine)
            
            #listaCine.recorrerInicio()

            return listaCine, salas
        except:
            print('Error al cargar el archivo...\n')  # Mensaje de error cuando ocurre una excepción al cargar el archivo

    def lecturaCP(self, dato):
        try:
            tree = ET.parse(dato)  # Parsea el archivo XML y crea un objeto de árbol
            root = tree.getroot()  # Obtiene la etiqueta raíz del árbol

            listaCategorias = EnlazadaSimple()

            # API Obtener los datos de la API
            response = requests.get('http://localhost:5000/getPeliculas')
            if response.status_code == 200:
                peliculasAPI = response.json()
                for categoriaAPI in peliculasAPI['categoria']:
                    nombre_categoria = categoriaAPI['nombre']
                    #print("Categoría:", nombre_categoria)

                    listaPeliculas = CicularDobleEnlazada()  # Crea una instancia de la lista de películas para cada categoría

                    datos_peliculas = categoriaAPI['peliculas']['pelicula']
                    for pelicula in datos_peliculas:
                        titulo = pelicula['titulo']
                        director = pelicula['director']
                        anio = pelicula['anio']
                        fecha = pelicula['fecha']
                        hora = pelicula['hora']
                        imagen = pelicula['imagen']
                        precio = float(pelicula['precio'])

                        # Agregar los datos de la película a la lista de películas de la categoría actual
                        listaPeliculas.agregarFinal(Pelicula(titulo, director, anio, fecha, hora, imagen, precio))

                    listaCategorias.agregarUltimo(Categoria(nombre_categoria, listaPeliculas))

            # Itera sobre los elementos hijos de la raíz (raiz=categorias)
            for elemento in root:
                # Verifica si el elemento actual tiene la etiqueta "categoria"
                if elemento.tag == "categoria":
                    nombre = ""

                    # Itera sobre los subelementos de la etiqueta "categoria" -> nombre, peliculas
                    for subelemento in elemento:
                        if subelemento.tag == "nombre":
                            nombre = subelemento.text

                        elif subelemento.tag == "peliculas":
                            listaPeliculas = CicularDobleEnlazada()  # Crea una instancia de la lista de películas para cada categoría

                            # Itera sobre las etiquetas "pelicula" dentro de "peliculas"
                            for sub in subelemento:
                                if sub.tag == "pelicula":
                                    titulo = ""
                                    director = ""
                                    anio = ""
                                    fecha = ""
                                    hora = ""
                                    imagen = ""
                                    precio = 0

                                    # Itera sobre las subetiquetas de "pelicula" y extrae los datos
                                    for s in sub:
                                        if s.tag == "titulo":
                                            titulo = s.text
                                        elif s.tag == "director":
                                            director = s.text
                                        elif s.tag == "anio":
                                            anio = s.text
                                        elif s.tag == "fecha":
                                            fecha = s.text
                                        elif s.tag == "hora":
                                            hora = s.text
                                        elif s.tag == "imagen":
                                            imagen = s.text
                                        elif s.tag == "precio":
                                            precio = float(s.text)

                                    listaPeliculas.agregarFinal(Pelicula(titulo, director, anio, fecha, hora, imagen, precio))

                            listaCategorias.agregarUltimo(Categoria(nombre, listaPeliculas))

            # listaCategorias.recorrerCategorias()

            return listaCategorias, listaPeliculas

        except Exception as e:
            print('Error al cargar el archivo')

    
    def lecturaT(self,dato):
        try:
            tree = ET.parse(dato)  # Parsea el archivo XML y crea un objeto de árbol
            root = tree.getroot()  # Obtiene la etiqueta raíz del árbol
            
            listaTarjetas = ListaDobleEnlazada()
            
            # API Obtener los datos de la API
            response = requests.get('http://localhost:5000/getTarjeta')
            if response.status_code == 200:
                tarjetasAPI = response.json()
                for tarjetaAPI in tarjetasAPI['tarjeta']:
                    tipo = tarjetaAPI['tipo']
                    numero = tarjetaAPI['numero']
                    titular = tarjetaAPI['titular']
                    fecha_exp = tarjetaAPI['fecha_expiracion']
                    listaTarjetas.agregarUltimo(Tarjeta(tipo, numero, titular, fecha_exp))

            # Itera sobre los elementos hijos de la raíz (raiz=tarjetas)
            for elemento in root:
                tipo = ""
                numero = ""
                titular = ""
                fecha_exp = ""
                
                if elemento.tag == "tarjeta":
                    for sub in elemento: #sub son las sub etiquetas mas adentro de la etiqueta tarjeta
                        if sub.tag == "tipo":
                            tipo = sub.text
                        if sub.tag == "numero":
                            numero = sub.text
                            #print(numero)
                        if sub.tag == "titular":
                            titular= sub.text
                        if sub.tag == "fecha_expiracion":
                            fecha_exp = sub.text
                    listaTarjetas.agregarUltimo(Tarjeta(tipo,numero,titular,fecha_exp))
            
            return listaTarjetas
        except Exception as e:
            print('Error al cargar el archivo')
        
#dato = r"C:\Users\amaya\OneDrive\Documents\GitHub\IPC2_V1S12023_ProyectoF2_3_202000558\Fase1\xml prueba\ArchivoPruebaU.xml"
#lector = Lectura()
#lista = lector.lecturaU(dato)

