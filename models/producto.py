from .db_connection import DBConnection


class Producto:
    """Modelo para la entidad Producto"""

    def __init__(self, id=None, nombre="", precio=0.0, cantidad=0):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    @staticmethod
    def create(producto):
        """Crea un nuevo producto en la base de datos"""
        db = DBConnection()
        if db.connect():
            query = """
                INSERT INTO productos (nombre, precio, cantidad)
                VALUES (?, ?, ?)
            """
            result = db.execute_query(
                query, (producto.nombre, producto.precio, producto.cantidad)
            )
            if result:
                # Obtener el id generado
                producto.id = db.cursor.lastrowid
            db.disconnect()
            return result
        return False

    @staticmethod
    def get_all():
        """Obtiene todos los productos de la base de datos"""
        db = DBConnection()
        productos = []
        if db.connect():
            rows = db.fetch_all("SELECT * FROM productos")
            for row in rows:
                producto = Producto(
                    id=row["id"],
                    nombre=row["nombre"],
                    precio=row["precio"],
                    cantidad=row["cantidad"],
                )
                productos.append(producto)
            db.disconnect()
        return productos

    @staticmethod
    def get_by_id(producto_id):
        """Obtiene un producto por su id"""
        db = DBConnection()
        producto = None
        if db.connect():
            row = db.fetch_one("SELECT * FROM productos WHERE id = ?", (producto_id,))
            if row:
                producto = Producto(
                    id=row["id"],
                    nombre=row["nombre"],
                    precio=row["precio"],
                    cantidad=row["cantidad"],
                )
            db.disconnect()
        return producto

    @staticmethod
    def update(producto):
        """Actualiza un producto en la base de datos"""
        db = DBConnection()
        if db.connect():
            query = """
                UPDATE productos
                SET nombre = ?, precio = ?, cantidad = ?
                WHERE id = ?
            """
            result = db.execute_query(
                query,
                (producto.nombre, producto.precio, producto.cantidad, producto.id),
            )
            db.disconnect()
            return result
        return False

    @staticmethod
    def delete(producto_id):
        """Elimina un producto de la base de datos"""
        db = DBConnection()
        if db.connect():
            # Primero obtenemos el producto para devolverlo
            producto = Producto.get_by_id(producto_id)
            if producto:
                # Luego lo eliminamos
                result = db.execute_query(
                    "DELETE FROM productos WHERE id = ?", (producto_id,)
                )
                db.disconnect()
                if result:
                    return producto
        return None

    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
        }
