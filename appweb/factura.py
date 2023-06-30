class Factura:
    def __init__(self, nombre, NIT, direccion, cine, boleto, nombre_cliente, nit_cliente, direccion_cliente, pelicula, fecha, hora, sala, num_boletos, numero_asiento, total):
        # Initialize the attributes
        self.nombre = nombre
        self.NIT = NIT
        self.direccion = direccion
        self.cine = cine
        self.boleto = boleto
        self.nombre_cliente = nombre_cliente
        self.nit_cliente = nit_cliente
        self.direccion_cliente = direccion_cliente
        self.pelicula = pelicula
        self.fecha = fecha
        self.hora = hora
        self.sala = sala
        self.num_boletos = num_boletos
        self.numero_asiento = numero_asiento
        self.total = total