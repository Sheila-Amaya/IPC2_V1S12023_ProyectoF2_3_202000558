class Usuario:
    def __init__(self,rol,nombre,apellido,telefono,correo,contrasena):
        self.rol = rol
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.contrasena = contrasena
        self.peliculas_Favoritas = []
        self.historial_Boletos = []
        self.tarjeta = None
