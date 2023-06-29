from Estructuras.NodoS import *

class EnlazadaSimple:
    
    def __init__(self):
        self.primero = None
        self.ultimo = None
    
    def estaVacia(self): #Si la lista esta vacia
        return self.primero == None #si no he agregado nada
    
    def agregarUltimo(self,dato):
        if self.estaVacia():
            self.primero = self.ultimo = Nodo(dato)
        else:
            temp = self.ultimo #guarda el dato en una variable temporal
            self.ultimo = temp.siguiente = Nodo(dato)

    def recorrer(self):
        temp = self.primero
        while temp != None:
            print("\n\tRol: "+temp.dato.rol)
            print("\tNombre: "+temp.dato.nombre)
            print("\tApellido: "+temp.dato.apellido)
            print("\tCorreo: "+temp.dato.correo)
            print("\tContraseña: "+temp.dato.contrasena+"\n")
            temp = temp.siguiente
            
    def eliminarUltimo(self):
        temp = self.primero
        while temp.siguiente != self.ultimo:
            temp = temp.siguiente
        temp.siguiente = None
        self.ultimo = temp
        
    def buscarPN(self, nombre):
        #
        temp = self.primero
        while temp:
            if temp.dato.nombre == nombre:
                #print("El nombre {} ha sido encontrado.".format(nombre))
                return temp.dato  # Devuelve el nodo si se encuentra el nombre
            temp = temp.siguiente
        #print("El nombre {} no ha sido encontrado.".format(nombre))
        return None  # Devuelve None si no se encuentra el nombre
        
    def buscarPorCorreo(self, correo):
        #
        temp = self.primero
        while temp:
            if temp.dato.correo == correo:
                #print("El correo {} ha sido encontrado.".format(correo))
                return temp.dato  # Devuelve el nodo si se encuentra el correo
            temp = temp.siguiente
        #print("El correo {} no ha sido encontrado.".format(correo))
        return None  # Devuelve None si no se encuentra el correo

    def buscarUsuario(self, nombre):
        #
        temp = self.primero
        while temp:
            if temp.dato.nombre == nombre:
                #print("El correo {} ha sido encontrado.".format(correo))
                return temp.dato  # Devuelve el nodo si se encuentra el correo
            temp = temp.siguiente
        #print("El correo {} no ha sido encontrado.".format(correo))
        return None  # Devuelve None si no se encuentra el correo
    
    def buscarPorNombreUsuario(self, nombre,contrasenia):
        #
        temp = self.primero
        while temp:
            if temp.dato.nombre == nombre and temp.dato.contrasenia == contrasenia:
                #print("El correo {} ha sido encontrado.".format(correo))
                return temp.dato  # Devuelve el nodo si se encuentra el correo
            temp = temp.siguiente
        #print("El correo {} no ha sido encontrado.".format(correo))
        return None  # Devuelve None si no se encuentra el correo
    
    def buscarPorRol(self, rol):
        #
        temp = self.primero
        while temp:
            if temp.dato.correo == rol:
                return temp.dato  # Devuelve el nodo si se encuentra el correo
            temp = temp.siguiente
        return None  # Devuelve None si no se encuentra el correo

    
    def modificarPorCorreo(self, correo):
        
        temp = self.primero

        # Recorrer la lista mientras haya nodos disponibles
        while temp:
            if temp.dato.correo == correo:
                print()
                nuevoNombre = input("\tIngrese el nuevo nombre: ")
                nuevoApellido = input("\tIngrese el nuevo apellido: ")
                nuevoTelefono = input("\tIngrese el nuevo teléfono: ")
                nuevoCorreo = input("\tIngrese el nuevo correo: ")
                nuevaContrasena = input("\tIngrese la nueva contraseña: ")

                # Modificar los datos del usuario
                temp.dato.nombre = nuevoNombre
                temp.dato.apellido = nuevoApellido
                temp.dato.telefono = nuevoTelefono
                temp.dato.correo = nuevoCorreo
                temp.dato.contrasena = nuevaContrasena

                print("\tLos datos del correo {} han sido modificados.\n".format(correo))
                return True

            # Avanzar al siguiente nodo
            temp = temp.siguiente

        # Si el correo no se encuentra en la lista
        print("El correo {} no ha sido encontrado.".format(correo))
        return False

    def eliminarPorCorreo(self, correo):
        temp = self.primero
        previo = None
        
        while temp:
            if temp.dato.correo == correo:
                if previo:
                    previo.siguiente = temp.siguiente
                    if temp == self.ultimo:
                        self.ultimo = previo
                else:
                    self.primero = temp.siguiente
                    if temp == self.ultimo:
                        self.ultimo = None
                print("La información correspondiente al correo {} ha sido eliminada del sistema.".format(correo))
                return
            previo = temp
            temp = temp.siguiente
        
        print("No se encontró ninguna información correspondiente al correo {} en el sistema.".format(correo))
        
    def recorrerSalas(self): #Lista almacenada dentro de una LD
        temp = self.primero
        while temp != None:
            print("\n\t\tNumero: "+temp.dato.num)
            print("\t\tAsientos: "+temp.dato.asientos+"\n")
            temp = temp.siguiente
            
    def modificarSalas(self):
        opcion = 's'
        while opcion.lower() == 's':
            nombre_sala = input("\n\tIngrese el numero de la sala a modificar: ")
            temp = self.primero
            while temp is not None:
                if temp.dato.num == nombre_sala:
                    print("\n\tDatos actuales de la sala:")
                    print("\tNúmero: " + temp.dato.num)
                    print("\tAsientos: " + temp.dato.asientos+"\n")

                    print("\n\tIngrese los nuevos datos de la sala:")
                    nuevo_numero = input("\tNuevo número: ")
                    nuevo_asientos = input("\tNuevo número de asientos: ")

                    temp.dato.num = nuevo_numero
                    temp.dato.asientos = nuevo_asientos

                    break

                temp = temp.siguiente

            if temp is None:
                print("\tNo se encontró la sala en la lista")

            opcion = input("\t¿Desea modificar otra sala? (s/n): ")

    def recorrerCategorias(self):
        temp = self.primero
        while temp:
            print("\n\tNombre de la categoría:", temp.dato.nombre)
            print("\tPeliculas:")
            temp.dato.pelicula.recorrerPeliculas()  # Llama al método recorrerPeliculas de la lista doblemente circular enlazada
            temp = temp.siguiente
            if temp == self.primero:
                break

    def mostrarPeliculas(self):
        temp = self.primero
        contador = 1
        while temp:
            print("\n\tCategoría:", temp.dato.nombre)
            pelicula_actual = temp.dato.pelicula.primero
            while pelicula_actual: #Recorrido de la DEC
                print("\t\t",contador,". Título:", pelicula_actual.dato.titulo)
                pelicula_actual = pelicula_actual.siguiente
                if pelicula_actual == temp.dato.pelicula.primero:
                    break
                contador += 1
            temp = temp.siguiente
            if temp == self.primero:
                break

    def buscarPorCategoria(self, categoria):
        #
        temp = self.primero
        while temp:
            if temp.dato.nombre == categoria:
                return temp.dato  # Devuelve el nodo si se encuentra la categoria
            temp = temp.siguiente
        return None  # Devuelve None si no se encuentra la categoria

    def buscarCategoria(self, categoria):
        if self.estaVacia():
            print("La lista está vacía")
        else:
            temp = self.primero
            while temp is not None:
                if temp.dato.nombre == categoria:  # se busca el elemento a través de su atributo
                    # Mostrar los datos actuales 
                    print("\n\tDatos actuales de la categoria:")
                    print("\tNombre categoria: " + temp.dato.nombre)
                    print("\tPeliculas:")
                    temp.dato.pelicula.recorrerPeliculas()  
                    
                    # Solicitar los nuevos datos de la categoria
                    print("\tIngrese los nuevos de la categoria:")
                    nuevo_nombre = input("\tNombre: ")
                    
                    # Modificar los datos del cine
                    temp.dato.nombre = nuevo_nombre
                    # Modificar las salas del cine
                    opcion = input("\nDesea modificar las peliculas de la categoria? (s/n): ")
                    if opcion.lower() == "s":
                        temp.dato.pelicula.modificarPeliculas()
                        
                    print("\n\tElemento modificado")
                    return
                temp = temp.siguiente
            print("\n\tNo se encontró el elemento en la lista")

    def eliminarPorCategoria(self, categoria):
        temp = self.primero
        previo = None
        
        while temp:
            if temp.dato.nombre == categoria:
                if previo:
                    previo.siguiente = temp.siguiente
                    if temp == self.ultimo:
                        self.ultimo = previo
                else:
                    self.primero = temp.siguiente
                    if temp == self.ultimo:
                        self.ultimo = None
                print("\tLa información correspondiente a la categoria {} ha sido eliminada del sistema.".format(categoria))
                return
            previo = temp
            temp = temp.siguiente
        
        print("\tNo se encontró ninguna información correspondiente a la categoria {} en el sistema.".format(categoria))
        
            
    def buscarUnaCategoria(self, categoria):
        if self.estaVacia():
            print("La lista está vacía")
        else:
            temp = self.primero
            while temp is not None:
                if temp.dato.nombre == categoria:
                    return temp.dato  # Devuelve el objeto Categoria encontrado
                temp = temp.siguiente
        return None  # Retorna None si la categoría no se encuentra en la lista
                
    def buscarPorSala(self, sala):
        temp = self.primero
        while temp:
            if temp.dato.num == sala:
                return temp.dato  # Devuelve el nodo si se encuentra la categoria
            temp = temp.siguiente
        return None  # Devuelve None si no se encuentra la categoria

    def mostrarUsuario(self):
        temp = self.primero
        while temp is not None:
            print("\n\tRol: " + temp.dato.rol)
            print("\tNombre: " + temp.dato.nombre)
            print("\tApellido: " + temp.dato.apellido)
            print("\tCorreo: " + temp.dato.correo)
            print("\tContraseña: " + temp.dato.contrasena + "\n")
            
            # Verificar si la lista de películas favoritas no está vacía
            if temp.dato.peliculas_Favoritas:
                print("\tPeliculas Favoritas:")
                for pelicula in temp.dato.peliculas_Favoritas:
                    print("\t- " + pelicula)
            else:
                pass
                #print("\tPeliculas Favoritas: No hay películas favoritas registradas.")
            
            # Verificar si la lista de historial de boletos no está vacía
            if temp.dato.historial_Boletos:
                print("\n\tHistorial de Boletos:")
                for boleto in temp.dato.historial_Boletos:
                    print("\t- Nombre:: " + boleto.nombre)
                    print("\t- Cine: " + boleto.cine)
                    print("\t- Número de boleto: " + boleto.numero_boleto)
                    print("\t- Número de sala: " + boleto.sala_encontrada)
                    print("\t- Película: " + boleto.pelicula)
                    print("\t- Fecha función: " + boleto.fecha_funcion)
                    print("\t- Hora función: " + boleto.hora_funcion)
                    print("\t- Número de boletos: " + boleto.num_boletos)
                    print("\t- Número de asiento: " + boleto.numero_asiento)
                    print("\t- Monto pagado: " + boleto.monto_pagado)
                    estado = "Cancelado" 
                    estado = "Cancelado" if boleto.cancelado else "Activo"
                    print("\tEstado: " + estado)

            else:
                pass
                #print("\tHistorial de Boletos: No hay boletos registrados en el historial.")
            
            temp = temp.siguiente
            
    def __iter__(self):
        current = self.primero  # Establece el nodo actual como el primero de la lista
        while current is not None:  # Itera mientras el nodo actual no sea None (hay elementos en la lista)
            yield current.dato  # Devuelve el dato del nodo actual
            current = current.siguiente  # Mueve al siguiente nodo de la lista

    def get_length(self):
        current = self.primero
        count = 0
        while current:
            count += 1
            current = current.siguiente
        return count