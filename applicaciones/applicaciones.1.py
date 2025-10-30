from datetime import datetime, timedelta #libreria para usar el timepo actual
import uuid # para crear id unicos
# variables de Datos
libros = [] # Una Lista. Guarda todos los libros como diccionarios.
prestamos = [] # Lista que Guarda todos los préstamos (activos e históricos) como diccionarios.
def agregar_libro(titulo,autor,tipo,copias=1):
    id_libro = str(uuid.uuid4())
    libros.append( {# append sirve papra meter una sola cosa a una lista, pero puede ser otra lista o un dic
        # un diccionario va entre llaves y son pares de valores, ej nobre:Alex
        "id": id_libro,
        "titulo":titulo,
        "autor":autor,
        "clasificacion":tipo,
        "copias":copias
    })
    return id_libro

print("Se creo correctaente la entrada del libbro ",agregar_libro("La Counidad del anillo","Tolkien","Fantasia"))













"""

Estructuras de datos:
- libros: lista de diccionarios con la información de cada libro
    {"id": int, "titulo": str, "autor": str, "copias": int}
- prestamos: lista de diccionarios con cada préstamo activo/histórico
    {"book_id": int, "usuario": str, "vence": datetime, "devuelto": bool}
"""