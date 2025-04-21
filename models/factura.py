from .db_connection import DBConnection


class ItemFactura:
    """Modelo para los items de una factura"""

    def __init__(
        self,
        id=None,
        factura_id=None,
        producto_nombre="",
        producto_id=None,
        precio=0.0,
        cantidad=0,
        subtotal=0.0,
    ):
        self.id = id
        self.factura_id = factura_id
        self.producto_nombre = producto_nombre
        self.producto_id = producto_id
        self.precio = precio
        self.cantidad = cantidad
        self.subtotal = subtotal

    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "factura_id": self.factura_id,
            "nombre": self.producto_nombre,
            "producto_id": self.producto_id,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "subtotal": self.subtotal,
        }


class Factura:
    """Modelo para la entidad Factura"""

    def __init__(self, id=None, cliente_id=None, total=0.0, fecha=None, items=None):
        self.id = id
        self.cliente_id = cliente_id
        self.total = total
        self.fecha = fecha
        self.items = items if items is not None else []

    @staticmethod
    def create(factura):
        """Crea una nueva factura en la base de datos"""
        db = DBConnection()
        if db.connect():
            # Insertar la factura
            query_factura = """
                INSERT INTO facturas (cliente_id, total)
                VALUES (?, ?)
            """
            result = db.execute_query(
                query_factura, (factura.cliente_id, factura.total)
            )

            if result:
                factura.id = db.cursor.lastrowid

                # Insertar los items de la factura
                query_item = """
                    INSERT INTO items_factura (factura_id, producto_nombre, producto_id, precio, cantidad, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """

                for item in factura.items:
                    item.factura_id = factura.id
                    db.execute_query(
                        query_item,
                        (
                            item.factura_id,
                            item.producto_nombre,
                            item.producto_id,
                            item.precio,
                            item.cantidad,
                            item.subtotal,
                        ),
                    )

            db.disconnect()
            return result
        return False

    @staticmethod
    def get_all():
        """Obtiene todas las facturas de la base de datos"""
        db = DBConnection()
        facturas = []
        if db.connect():
            # Obtener las facturas
            rows_facturas = db.fetch_all("SELECT * FROM facturas")

            for row_factura in rows_facturas:
                # Obtener los items de la factura
                factura_id = row_factura["id"]
                query_items = "SELECT * FROM items_factura WHERE factura_id = ?"
                rows_items = db.fetch_all(query_items, (factura_id,))

                items = []
                for row_item in rows_items:
                    item = ItemFactura(
                        id=row_item["id"],
                        factura_id=row_item["factura_id"],
                        producto_id=row_item["producto_id"],
                        producto_nombre=row_item["producto_nombre"],
                        precio=row_item["precio"],
                        cantidad=row_item["cantidad"],
                        subtotal=row_item["subtotal"],
                    )
                    items.append(item)

                # Crear la factura con sus items
                factura = Factura(
                    id=row_factura["id"],
                    cliente_id=row_factura["cliente_id"],
                    total=row_factura["total"],
                    fecha=row_factura["fecha"],
                    items=items,
                )
                facturas.append(factura)

            db.disconnect()
        return facturas

    @staticmethod
    def get_by_id(factura_id):
        """Obtiene una factura por su id"""
        db = DBConnection()
        factura = None
        if db.connect():
            # Obtener la factura
            row_factura = db.fetch_one(
                "SELECT * FROM facturas WHERE id = ?", (factura_id,)
            )

            if row_factura:
                # Obtener los items de la factura
                query_items = "SELECT * FROM items_factura WHERE factura_id = ?"
                rows_items = db.fetch_all(query_items, (factura_id,))

                items = []
                for row_item in rows_items:
                    item = ItemFactura(
                        id=row_item["id"],
                        factura_id=row_item["factura_id"],
                        producto_id=row_item["producto_id"],
                        producto_nombre=row_item["producto_nombre"],
                        precio=row_item["precio"],
                        cantidad=row_item["cantidad"],
                        subtotal=row_item["subtotal"],
                    )
                    items.append(item)

                # Crear la factura con sus items
                factura = Factura(
                    id=row_factura["id"],
                    cliente_id=row_factura["cliente_id"],
                    total=row_factura["total"],
                    fecha=row_factura["fecha"],
                    items=items,
                )

            db.disconnect()
        return factura

    @staticmethod
    def update(factura):
        """Actualiza una factura en la base de datos"""
        db = DBConnection()
        if db.connect():
            # Actualizar la factura
            query_factura = """
                UPDATE facturas
                SET cliente_id = ?, total = ?
                WHERE id = ?
            """
            result = db.execute_query(
                query_factura, (factura.cliente_id, factura.total, factura.id)
            )

            if result:
                # Eliminar los items anteriores
                db.execute_query(
                    "DELETE FROM items_factura WHERE factura_id = ?", (factura.id,)
                )

                # Insertar los nuevos items
                query_item = """
                    INSERT INTO items_factura (factura_id, producto_nombre, producto_id, precio, cantidad, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """

                for item in factura.items:
                    item.factura_id = factura.id
                    db.execute_query(
                        query_item,
                        (
                            item.factura_id,
                            item.producto_nombre,
                            item.producto_id,
                            item.precio,
                            item.cantidad,
                            item.subtotal,
                        ),
                    )

            db.disconnect()
            return result
        return False

    @staticmethod
    def delete(factura_id):
        """Elimina una factura de la base de datos"""
        db = DBConnection()
        if db.connect():
            # Primero obtenemos la factura para devolverla
            factura = Factura.get_by_id(factura_id)

            if factura:
                # Eliminar los items asociados
                db.execute_query(
                    "DELETE FROM items_factura WHERE factura_id = ?", (factura_id,)
                )

                # Eliminar la factura
                result = db.execute_query(
                    "DELETE FROM facturas WHERE id = ?", (factura_id,)
                )

                db.disconnect()
                if result:
                    return factura
        return None

    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "total": self.total,
            "fecha": self.fecha,
            "items": [item.to_dict() for item in self.items],
        }
