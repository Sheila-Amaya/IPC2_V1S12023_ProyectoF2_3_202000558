from Estructuras.NodoDEC import *
from pelicula import *
class CicularDobleEnlazada:

    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.length = 0
        
    def estaVacia(self):
        return self.primero == None
    
    def agregarFinal(self, dato):
        nuevo_nodo = Nodo(dato)  # Creamos un nuevo nodo con el dato 
        
        if self.estaVacia(): # Si la lista está vacía, el nuevo nodo se convierte en el primer y único elemento
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
            nuevo_nodo.siguiente = nuevo_nodo  # El nuevo nodo se enlaza consigo mismo
            nuevo_nodo.anterior = nuevo_nodo  # El nuevo nodo se enlaza consigo mismo
        else: # Si la lista no está vacía, se actualizan los enlaces de los nodos existentes
            nuevo_nodo.siguiente = self.primero  # El siguiente del nuevo nodo es el primer nodo actual
            nuevo_nodo.anterior = self.ultimo  # El anterior del nuevo nodo es el último nodo actual
            self.primero.anterior = nuevo_nodo  # El anterior del primer nodo actual se actualiza al nuevo nodo
            self.ultimo.siguiente = nuevo_nodo  # El siguiente del último nodo actual se actualiza al nuevo nodo
            self.ultimo = nuevo_nodo  # Actualizamos el puntero del último nodo a ser el nuevo nodo
        self.length += 1

    def recorrerInicio(self):
        temp = self.primero
        while temp:
            print(temp.dato)  # Imprime el dato del nodo actual
            aux = aux.siguiente  # Avanza al siguiente nodo asignándolo a la variable 'aux'
            if aux == self.primero:  # Si se ha vuelto al primer nodo, se ha recorrido toda la lista
                break
            
    def buscar(self, dato):
        if self.estavacia():
            return False
        
        nodo_actual = self.primero
        while nodo_actual:
            if nodo_actual.dato == dato:  # Si se encuentra el dato buscado
                return True
            else:
                nodo_actual = nodo_actual.siguiente
                if nodo_actual == self.primero:  # Si se ha recorrido toda la lista sin encontrar el dato
                    return False

    def eliminar(self, dato):
        if self.estaVacia():
            return

        nodo_actual = self.primero
        while nodo_actual:
            if nodo_actual.dato == dato:
                if nodo_actual == self.primero:
                    self.primero = nodo_actual.siguiente
                    self.primero.anterior = self.ultimo
                    self.ultimo.siguiente = self.primero
                elif nodo_actual == self.ultimo:
                    self.ultimo = nodo_actual.anterior
                    self.ultimo.siguiente = self.primero
                    self.primero.anterior = self.ultimo
                else:
                    nodo_actual.anterior.siguiente = nodo_actual.siguiente
                    nodo_actual.siguiente.anterior = nodo_actual.anterior
                self.length -= 1
                return

            nodo_actual = nodo_actual.siguiente
            if nodo_actual == self.primero:
                return

    def recorrerPeliculas(self):
        pelicula_actual = self.primero
        while pelicula_actual:
            print()
            print("\t\tTítulo:", pelicula_actual.dato.titulo)
            print("\t\tDirector:", pelicula_actual.dato.director)
            print("\t\tAño:", pelicula_actual.dato.anio)
            print("\t\tFecha:", pelicula_actual.dato.fecha)
            print("\t\tHora:", pelicula_actual.dato.hora)
            print("\t\timagen:", pelicula_actual.dato.imagen)
            print("\t\tPrecio (Q):", pelicula_actual.dato.precio)
            print()
            pelicula_actual = pelicula_actual.siguiente
            if pelicula_actual == self.primero:
                break
            
    def modificarPeliculas(self):
        opcion = 's'
        while opcion.lower() == 's':
            titulo_buscar = input("\n\tIngrese el nombre de la pelicula a modificar: ")
            
            pelicula_actual = self.primero
            while pelicula_actual:
                if pelicula_actual.dato.titulo == titulo_buscar:  # Si se encuentra la película buscada
                    print("\n\tDatos actuales de la película:")
                    print("\tTítulo:", pelicula_actual.dato.titulo)
                    print("\tDirector:", pelicula_actual.dato.director)
                    print("\tAño:", pelicula_actual.dato.anio)
                    print("\tFecha:", pelicula_actual.dato.fecha)
                    print("\tHora:", pelicula_actual.dato.hora)
                    print("\t\timagen:", pelicula_actual.dato.imagen)
                    print("\tPrecio (Q):", pelicula_actual.dato.precio)
                    print()

                    nuevo_titulo = input("\tIngrese el nuevo título: ")
                    nuevo_director = input("\tIngrese el nuevo director: ")
                    nuevo_anio = input("\tIngrese el nuevo año: ")
                    nueva_fecha = input("\tIngrese la nueva fecha: ")
                    nueva_hora = input("\tIngrese la nueva hora: ")
                    nuevo_precio = input("\tIngrese el nuevo precio (Q): ")

                    pelicula_actual.dato.titulo = nuevo_titulo
                    pelicula_actual.dato.director = nuevo_director
                    pelicula_actual.dato.anio = nuevo_anio
                    pelicula_actual.dato.fecha = nueva_fecha
                    pelicula_actual.dato.hora = nueva_hora
                    pelicula_actual.dato.precio = nuevo_precio

                    print("\tLos datos de la película se han modificado.")
                    return

                pelicula_actual = pelicula_actual.siguiente
                if pelicula_actual == self.primero:  # Si se ha recorrido toda la lista sin encontrar la película
                    break

            print("\tLa película no se encontró en la lista.")
            
    def verSoloPeliculas(self):
        pelicula_actual = self.primero
        while pelicula_actual:
            print("\t\tTítulo:", pelicula_actual.dato.titulo)
            pelicula_actual = pelicula_actual.siguiente
            if pelicula_actual == self.primero:
                break
        return pelicula_actual.dato.titulo 
    
    def fav(self):
        pelicula_actual = self.primero
        peliculas = []
        while pelicula_actual:
            peliculas.append((pelicula_actual.dato.titulo, pelicula_actual.dato.imagen))
            pelicula_actual = pelicula_actual.siguiente
            if pelicula_actual == self.primero:
                break
        return peliculas
            
    def buscarPeliculaPorNombre(self, nombre):
        if self.estaVacia():
            print("\tNo hay películas en la lista.")
            return None

        pelicula_actual = self.primero
        while True:
            if pelicula_actual.dato.titulo.lower() == nombre.lower():
                return pelicula_actual.dato

            pelicula_actual = pelicula_actual.siguiente
            if pelicula_actual == self.primero:
                break

        print("\tLa película no se encontró en la lista.")
        return None
        
    def buscarPeliculaParaBoleto(self, nombre):
        if self.estaVacia():
            print("\tNo hay películas en la lista.")
            return None

        pelicula_actual = self.primero
        while True:
            if pelicula_actual.dato.titulo.lower() == nombre.lower():
                print("\n\tPelícula encontrada:\n")
                print("\t\tTítulo:", pelicula_actual.dato.titulo)
                print("\t\tFecha función:", pelicula_actual.dato.fecha)
                print("\t\tHora de la funcion:", pelicula_actual.dato.hora)
                print("\t\tPrecio (Q):", pelicula_actual.dato.precio)
                print()
                return pelicula_actual.dato #retorna el nodo con la informacion

            pelicula_actual = pelicula_actual.siguiente
            if pelicula_actual == self.primero:
                break

        print("\tLa película no se encontró en la lista.")
        return None

    def buscarPeli(self, nombre):
        if self.estaVacia():
            print("\tNo hay películas en la lista.")
            return None

        pelicula_actual = self.primero
        while True:
            if pelicula_actual.dato.titulo.lower() == nombre.lower():
                return pelicula_actual.dato

            pelicula_actual = pelicula_actual.siguiente
            if pelicula_actual == self.primero:
                break

        return None
    
    def __iter__(self):
        nodo_actual = self.primero  # Inicializar el nodo actual como el primer nodo
        while nodo_actual is not None:  # Mientras haya nodos en la lista
            yield nodo_actual.dato  # Devolver el dato del nodo actual
            nodo_actual = nodo_actual.siguiente  # Avanzar al siguiente nodo
            if nodo_actual == self.primero:  # Si se ha vuelto al primer nodo, se ha recorrido toda la lista
                break
            
    def get_length(self):
        return self.length