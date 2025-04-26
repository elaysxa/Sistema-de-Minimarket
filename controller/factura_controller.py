from math import e
from models.factura import Factura, ItemFactura
from models.cliente import Cliente
from models.producto import Producto
from controller.producto_controller import ProductoController


class FacturaController:
    """Controlador para la entidad Factura"""

    @staticmethod
    def crear_factura(cliente_id, items_data):
        """
        Crea una nueva factura

        Args:
            cliente_id: ID del cliente
            items_data: Lista de diccionarios con los datos de los items (producto_id, cantidad)

        Returns:
            (Boolean, String): Tupla con el resultado de la operación y un mensaje
        """
        try:
            # Validar cliente
            cliente_id = int(cliente_id)
            cliente = Cliente.get_by_id(cliente_id)
            if not cliente:
                return False, f"Cliente con ID {cliente_id} no encontrado"

            # Validar que haya items
            if not items_data or len(items_data) == 0:
                return False, "La factura debe tener al menos un producto"

            # Crear los items y verificar stock
            items_factura = []
            total_factura = 0

            for item_data in items_data:
                producto_id = int(item_data["producto_id"])
                cantidad = int(item_data["cantidad"])

                # Verificar que haya suficiente stock
                stock_suficiente, mensaje = (
                    ProductoController.verificar_stock_disponible(producto_id, cantidad)
                )
                if not stock_suficiente:
                    return False, mensaje

                # Obtener el producto
                producto = Producto.get_by_id(producto_id)
                subtotal = producto.precio * cantidad

                # Crear el item
                item = ItemFactura(
                    producto_nombre=producto.nombre,
                    producto_id=producto_id,
                    precio=producto.precio,
                    cantidad=cantidad,
                    subtotal=subtotal,
                )
                items_factura.append(item)
                total_factura += subtotal

                # Actualizar el stock del producto
                nuevo_stock = producto.cantidad - cantidad
                ProductoController.actualizar_stock(producto_id, nuevo_stock)

            # Crear la factura
            factura = Factura(
                cliente_id=cliente_id, total=total_factura, items=items_factura
            )

            # Guardar en la base de datos
            if Factura.create(factura):
                return (
                    True,
                    f"Factura creada correctamente. Total: ${total_factura:.2f}",
                )
            else:
                return False, "Error al guardar la factura en la base de datos"

        except ValueError as e:
            return False, f"Error en los datos: {str(e)}"
        except Exception as e:
            return False, f"Error al crear la factura: {str(e)}"

    @staticmethod
    def obtener_todas_facturas():
        """Obtiene todas las facturas de la base de datos"""
        return Factura.get_all()

    @staticmethod
    def obtener_factura_por_id(factura_id):
        """Obtiene una factura por su ID"""
        try:
            factura_id = int(factura_id)
            return Factura.get_by_id(factura_id)
        except ValueError:
            return None
    @staticmethod
    def obtener_items_por_factura_id(factura_id):
        """Devuelve los ítems de una factura dado su ID"""
        try:
            factura = Factura.get_by_id(int(factura_id))
            return factura.items if factura else []
        except Exception:
            return []


    @staticmethod
    def eliminar_factura(factura_id):
        """Elimina una factura por su ID"""
        try:
            factura_id = int(factura_id)
            factura = Factura.delete(factura_id)
            if factura:
                return True, f"Factura #{factura.id} eliminada correctamente"
            else:
                return (
                    False,
                    f"Factura con ID {factura_id} no encontrada o error al eliminar",
                )
        except ValueError:
            return False, "El ID de la factura debe ser un número"

    @staticmethod
    def obtener_facturas_por_cliente(cliente_id):
        """Obtiene las facturas de un cliente específico"""
        try:
            cliente_id = int(cliente_id)
            todas_facturas = Factura.get_all()
            facturas_cliente = [f for f in todas_facturas if f.cliente_id == cliente_id]
            return facturas_cliente
        except ValueError:
            return []
        except Exception as e:
            return f"Error al obtener las facturas del cliente: {str(e)}"
    
    @staticmethod
    def modificar_factura(factura_id, cliente_id, items_data):
        """
        Modifica una factura existente

        Args:
            factura_id: ID de la factura a modificar
            cliente_id: ID del nuevo cliente
            items_data: Lista de diccionarios con los datos de los items (producto_id, cantidad)

        Returns:
            (Boolean, String): Tupla con el resultado de la operación y un mensaje
        """
        try:
            # Validar cliente
            cliente_id = int(cliente_id)
            cliente = Cliente.get_by_id(cliente_id)
            if not cliente:
                return False, f"Cliente con ID {cliente_id} no encontrado"

            # Validar que haya items
            if not items_data or len(items_data) == 0:
                return False, "La factura debe tener al menos un producto"

            # Obtener la factura existente
            factura = Factura.get_by_id(factura_id)
            if not factura:
                return False, f"Factura con ID {factura_id} no encontrada"

            # Crear los nuevos items y verificar stock
            items_factura = []
            total_factura = 0

            for item_data in items_data:
                producto_id = int(item_data["producto_id"])
                cantidad = int(item_data["cantidad"])

                # Verificar que haya suficiente stock
                stock_suficiente, mensaje = (
                    ProductoController.verificar_stock_disponible(producto_id, cantidad)
                )
                if not stock_suficiente:
                    return False, mensaje

                # Obtener el producto
                producto = Producto.get_by_id(producto_id)
                subtotal = producto.precio * cantidad

                # Crear el item
                item = ItemFactura(
                    producto_nombre=producto.nombre,
                    producto_id=producto.id,
                    precio=producto.precio,
                    cantidad=cantidad,
                    subtotal=subtotal,
                )
                items_factura.append(item)
                total_factura += subtotal

                # Actualizar el stock del producto
                nuevo_stock = producto.cantidad - cantidad
                ProductoController.actualizar_stock(producto_id, nuevo_stock)

            # Modificar la factura
            factura.cliente_id = cliente_id
            factura.items = items_factura
            factura.total = total_factura

            # Guardar en la base de datos
            if Factura.update(factura):
                return (
                    True,
                    f"Factura modificada correctamente. Total: ${total_factura  :.2f}",
                )    
        except ValueError as e:
            return False, f"Error en los datos: {str(e)}"   