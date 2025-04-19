from models.producto import Producto


class ProductoController:
    """Controlador para la entidad Producto"""

    @staticmethod
    def crear_producto(nombre, precio, cantidad):
        """Crea un nuevo producto con los datos proporcionados"""
        try:
            precio = float(precio)
            cantidad = int(cantidad)

            # Validar datos
            if not nombre.strip():
                return False, "El nombre del producto no puede estar vacío"
            if precio <= 0:
                return False, "El precio debe ser mayor que cero"
            if cantidad < 0:
                return False, "La cantidad no puede ser negativa"

            # Crear el objeto producto
            nuevo_producto = Producto(nombre=nombre, precio=precio, cantidad=cantidad)

            # Guardar en la base de datos
            if Producto.create(nuevo_producto):
                return True, f"Producto '{nombre}' creado correctamente"
            else:
                return False, "Error al guardar el producto en la base de datos"
        except ValueError:
            return False, "Los valores de precio y cantidad deben ser numéricos"

    @staticmethod
    def obtener_todos_productos():
        """Obtiene todos los productos de la base de datos"""
        return Producto.get_all()

    @staticmethod
    def obtener_producto_por_id(producto_id):
        """Obtiene un producto por su ID"""
        try:
            producto_id = int(producto_id)
            return Producto.get_by_id(producto_id)
        except ValueError:
            return None

    @staticmethod
    def actualizar_producto(producto_id, nombre=None, precio=None, cantidad=None):
        """Actualiza los datos de un producto existente"""
        # Obtener el producto actual
        producto = ProductoController.obtener_producto_por_id(producto_id)
        if not producto:
            return False, f"Producto con ID {producto_id} no encontrado"

        # Actualizar solo los campos proporcionados
        if nombre is not None and nombre.strip():
            producto.nombre = nombre

        try:
            if precio is not None:
                if precio == "":
                    pass  # Mantener el precio actual
                else:
                    precio_float = float(precio)
                    if precio_float <= 0:
                        return False, "El precio debe ser mayor que cero"
                    producto.precio = precio_float

            if cantidad is not None:
                if cantidad == "":
                    pass  # Mantener la cantidad actual
                else:
                    cantidad_int = int(cantidad)
                    if cantidad_int < 0:
                        return False, "La cantidad no puede ser negativa"
                    producto.cantidad = cantidad_int

            # Guardar los cambios
            if Producto.update(producto):
                return True, f"Producto '{producto.nombre}' actualizado correctamente"
            else:
                return False, "Error al actualizar el producto en la base de datos"
        except ValueError:
            return False, "Los valores de precio y cantidad deben ser numéricos"

    @staticmethod
    def eliminar_producto(producto_id):
        """Elimina un producto por su ID"""
        try:
            producto_id = int(producto_id)
            producto = Producto.delete(producto_id)
            if producto:
                return True, f"Producto '{producto.nombre}' eliminado correctamente"
            else:
                return (
                    False,
                    f"Producto con ID {producto_id} no encontrado o error al eliminar",
                )
        except ValueError:
            return False, "El ID del producto debe ser un número"

    @staticmethod
    def buscar_productos_por_nombre(nombre):
        """Busca productos que contengan el texto proporcionado en su nombre"""
        productos = Producto.get_all()
        return [p for p in productos if nombre.lower() in p.nombre.lower()]

    @staticmethod
    def verificar_stock_disponible(producto_id, cantidad_requerida):
        """Verifica si hay suficiente stock para un producto"""
        producto = ProductoController.obtener_producto_por_id(producto_id)
        if not producto:
            return False, "Producto no encontrado"

        if producto.cantidad >= cantidad_requerida:
            return True, f"Stock disponible: {producto.cantidad}"
        else:
            return (
                False,
                f"Stock insuficiente. Disponible: {producto.cantidad}, Requerido: {cantidad_requerida}",
            )

    @staticmethod
    def actualizar_stock(producto_id, cantidad_nueva):
        """Actualiza el stock de un producto después de una venta o reposición"""
        producto = ProductoController.obtener_producto_por_id(producto_id)
        if not producto:
            return False, "Producto no encontrado"

        try:
            cantidad_nueva = int(cantidad_nueva)
            if cantidad_nueva < 0:
                return False, "La cantidad no puede ser negativa"

            producto.cantidad = cantidad_nueva
            if Producto.update(producto):
                return (
                    True,
                    f"Stock del producto '{producto.nombre}' actualizado a {cantidad_nueva}",
                )
            else:
                return False, "Error al actualizar el stock"
        except ValueError:
            return False, "La cantidad debe ser un número entero"
    
    @staticmethod
    def contar_productos():
        """Cuenta el número total de productos en la base de datos"""
        return Producto.count()
