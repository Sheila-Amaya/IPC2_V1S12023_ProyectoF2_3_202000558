from Estructuras.NodoDE import *

class ListaDobleEnlazada:

    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
        
    def estaVacia(self):
        return self.primero is None
    
    def agregarUltimo(self, dato):
        if self.estaVacia():
            self.primero = self.ultimo = Nodo(dato)
        else:
            nuevo_nodo = Nodo(dato)
            nuevo_nodo.anterior = self.ultimo
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        self.size += 1
        
    def recorrerInicio(self):
        temp = self.primero
        while temp is not None:
            print("\n\tNombre cine: "+temp.dato.nombre)
            print("\tSalas: ")
            temp.dato.sala.recorrerSalas() #LISTA SIMPLE
            temp = temp.siguiente
            
    def recorrerFinal(self):
        temp = self.ultimo
        while temp is not None:
            temp = temp.anterior
            
    def size(self):
        return self.size
    
    def eliminar(self):
        if self.estaVacia():
            print("La lista está vacía")
        elif self.primero.siguiente is None:
            self.primero = self.ultimo = None
            self.size = 0
        else:
            self.primero = self.primero.siguiente
            self.primero.anterior = None
            self.size -= 1
            

    def eliminarPorCine(self, nombre):
        if self.estaVacia():
            print("La lista está vacía")
        else:
            temp = self.primero
            while temp is not None:
                if temp.dato.nombre == nombre: # se busca el elemento a travez de su atributo
                    if temp.anterior is None: # si el elemento a eliminar es el primero de la lista
                        self.primero = temp.siguiente
                        if self.primero is not None:
                            self.primero.anterior = None
                        else:
                            self.ultimo = None
                    else: # El elemento a eliminar está en el medio o al final de la lista
                        temp.anterior.siguiente = temp.siguiente
                        if temp.siguiente is not None:
                            temp.siguiente.anterior = temp.anterior
                        else:
                            self.ultimo = temp.anterior
                    self.size -= 1
                    print("\n\tElemento eliminado\n")
                    return
                temp = temp.siguiente
            print("\n\tNo se encontró el elemento en la lista\n")
            

    def modificarPorCine(self, nombre):
        if self.estaVacia():
            print("La lista está vacía")
        else:
            temp = self.primero
            while temp is not None:
                if temp.dato.nombre == nombre:  # se busca el elemento a través de su atributo
                    # Mostrar los datos actuales del cine
                    print("\n\tDatos actuales del cine:")
                    print("\tNombre cine: " + temp.dato.nombre)
                    print("\tSalas:")
                    temp.dato.sala.recorrerSalas()  # Recorrer y mostrar las salas del cine

                    # Solicitar los nuevos datos del cine
                    print("\tIngrese los nuevos datos del cine:")
                    nuevo_nombre = input("\tNombre: ")

                    # Modificar los datos del cine
                    temp.dato.nombre = nuevo_nombre

                    # Modificar las salas del cine
                    opcion = input("\nDesea modificar las salas del cine? (s/n): ")
                    if opcion.lower() == "s":
                        temp.dato.sala.modificarSalas()

                    print("\n\tElemento modificado")
                    return
                temp = temp.siguiente
            print("\n\tNo se encontró el elemento en la lista")
            

    def buscarPorNombre(self, nombre):
        if self.estaVacia():
            print("La lista está vacía")
        else:
            temp = self.primero
            while temp is not None:
                if temp.dato.nombre == nombre:
                    print("\n\tCine encontrado:")
                    print("\tNombre cine:", temp.dato.nombre)
                    print("\tSalas:")
                    temp.dato.sala.recorrerSalas()
                    return
                temp = temp.siguiente
            print("\n\tNo se encontró el cine con el nombre especificado")
            

    def buscarCine(self, cine):
        temp = self.primero
        while temp:
            if temp.dato.nombre == cine:
                return temp.dato  # Devuelve el nodo si se encuentra el cine
            temp = temp.siguiente
        return None  # Devuelve None si no se encuentra el correo