from .db_connection import DBConnection


class Cliente:
    """Modelo para la entidad Cliente"""

    def __init__(self, id=None, nombre="", edad="", telefono="", documento=None):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.telefono = telefono
        self.documento = documento if documento is not None else id

    @staticmethod
    def create(cliente):
        """Crea un nuevo cliente en la base de datos"""
        db = DBConnection()
        if db.connect():
            query = """
                INSERT INTO clientes (nombre, edad, telefono, documento)
                VALUES (?, ?, ?, ?)
            """
            result = db.execute_query(
                query,
                (cliente.nombre, cliente.edad, cliente.telefono, cliente.documento),
            )
            if result:
                # Obtener el id generado
                cliente.id = db.cursor.lastrowid
            db.disconnect()
            return result
        return False

    @staticmethod
    def get_all():
        """Obtiene todos los clientes de la base de datos"""
        db = DBConnection()
        clientes = []
        if db.connect():
            rows = db.fetch_all("SELECT * FROM clientes")
            for row in rows:
                cliente = Cliente(
                    id=row["id"],
                    nombre=row["nombre"],
                    edad=row["edad"],
                    telefono=row["telefono"],
                    documento=row["documento"],
                )
                clientes.append(cliente)
            db.disconnect()
        return clientes

    @staticmethod
    def get_by_id(cliente_id):
        """Obtiene un cliente por su id"""
        db = DBConnection()
        cliente = None
        if db.connect():
            row = db.fetch_one("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
            if row:
                cliente = Cliente(
                    id=row["id"],
                    nombre=row["nombre"],
                    edad=row["edad"],
                    telefono=row["telefono"],
                    documento=row["documento"],
                )
            db.disconnect()
        return cliente

    @staticmethod
    def update(cliente):
        """Actualiza un cliente en la base de datos"""
        db = DBConnection()
        if db.connect():
            query = """
                UPDATE clientes
                SET nombre = ?, edad = ?, telefono = ?, documento = ?
                WHERE id = ?
            """
            result = db.execute_query(
                query,
                (
                    cliente.nombre,
                    cliente.edad,
                    cliente.telefono,
                    cliente.documento,
                    cliente.id,
                ),
            )
            db.disconnect()
            return result
        return False

    @staticmethod
    def delete(cliente_id):
        """Elimina un cliente de la base de datos"""
        db = DBConnection()
        if db.connect():
            # Primero obtenemos el cliente para devolverlo
            cliente = Cliente.get_by_id(cliente_id)
            if cliente:
                # Luego lo eliminamos
                result = db.execute_query(
                    "DELETE FROM clientes WHERE id = ?", (cliente_id,)
                )
                db.disconnect()
                if result:
                    return cliente
        return None

    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edad": self.edad,
            "telefono": self.telefono,
            "documento": self.documento,
        }
