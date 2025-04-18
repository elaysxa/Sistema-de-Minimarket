import sqlite3
import os

class DBConnection:
    """Clase para manejar la conexión a la base de datos SQLite"""

    def __init__(self, db_name="data/minimarket.db"):
        # Ruta de la base de datos (en el mismo directorio que el proyecto)
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_name)
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establece la conexión a la base de datos"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = (
                sqlite3.Row
            )  # Para acceder a las filas como diccionarios
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False

    def disconnect(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute_query(self, query, params=()):
        """Ejecuta una consulta SQL"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False

    def fetch_all(self, query, params=()):
        """Ejecuta una consulta y devuelve todos los resultados"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener datos: {e}")
            return []

    def fetch_one(self, query, params=()):
        """Ejecuta una consulta y devuelve un solo resultado"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener datos: {e}")
            return None

    def create_tables(self):
        """Crea las tablas necesarias si no existen"""
        try:
            # Tabla Clientes
            self.execute_query(
                """
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    edad TEXT,
                    telefono TEXT,
                    documento INTEGER
                )
            """
            )

            # Tabla Productos
            self.execute_query(
                """
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    cantidad INTEGER NOT NULL
                )
            """
            )

            # Tabla Facturas
            self.execute_query(
                """
                CREATE TABLE IF NOT EXISTS facturas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    total REAL NOT NULL,
                    fecha TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
            """
            )

            # Tabla Items de Factura (para la relación muchos a muchos)
            self.execute_query(
                """
                CREATE TABLE IF NOT EXISTS items_factura (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    factura_id INTEGER,
                    producto_nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    cantidad INTEGER NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (factura_id) REFERENCES facturas (id)
                )
            """
            )

            return True
        except sqlite3.Error as e:
            print(f"Error al crear las tablas: {e}")
            return False
