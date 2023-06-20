class Boleto:
    def __init__(self, nombre, cine, numero_boleto, pelicula, fecha_funcion, hora_funcion, num_boletos,sala_encontrada, numero_asiento, monto_pagado, cancelado=False):
        self.nombre = nombre
        self.cine = cine
        self.numero_boleto = numero_boleto
        self.pelicula = pelicula
        self.fecha_funcion = fecha_funcion
        self.hora_funcion = hora_funcion
        self.num_boletos = num_boletos
        self.sala_encontrada = sala_encontrada
        self.numero_asiento = numero_asiento
        self.monto_pagado = monto_pagado
        self.cancelado = cancelado
