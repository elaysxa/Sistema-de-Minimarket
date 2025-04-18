# Este archivo permite que Python reconozca la carpeta como un paquete

from .db_connection import DBConnection
from .cliente import Cliente
from .producto import Producto
from .factura import Factura, ItemFactura


# Inicializar la base de datos al importar el paquete
def init_db():
    db = DBConnection()
    if db.connect():
        db.create_tables()
        db.disconnect()
        return True
    return False


# Inicializar la base de datos
init_db()
