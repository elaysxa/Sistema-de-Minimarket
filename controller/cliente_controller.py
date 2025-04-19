from models.cliente import Cliente


class ClienteController:
    """Controlador para la entidad Cliente"""

    @staticmethod
    def crear_cliente(nombre, edad, telefono, documento=None):
        """Crea un nuevo cliente con los datos proporcionados"""
        try:
            # Validar datos
            if not nombre.strip():
                return False, "El nombre del cliente no puede estar vacío"

            # Si se proporciona documento, validar que sea numérico
            if documento and not documento.isdigit():
                return False, "El documento debe ser un número"
            elif documento:
                documento = int(documento)

            # Crear el objeto cliente
            nuevo_cliente = Cliente(
                nombre=nombre, edad=edad, telefono=telefono, documento=documento
            )

            # Guardar en la base de datos
            if Cliente.create(nuevo_cliente):
                return True, f"Cliente '{nombre}' creado correctamente"
            else:
                return False, "Error al guardar el cliente en la base de datos"
        except Exception as e:
            return False, f"Error al crear el cliente: {str(e)}"

    @staticmethod
    def obtener_todos_clientes():
        """Obtiene todos los clientes de la base de datos"""
        return Cliente.get_all()

    @staticmethod
    def obtener_cliente_por_id(cliente_id):
        """Obtiene un cliente por su ID"""
        try:
            cliente_id = int(cliente_id)
            return Cliente.get_by_id(cliente_id)
        except ValueError:
            return None

    @staticmethod
    def actualizar_cliente(
        cliente_id, nombre=None, edad=None, telefono=None, documento=None
    ):
        """Actualiza los datos de un cliente existente"""
        # Obtener el cliente actual
        cliente = ClienteController.obtener_cliente_por_id(cliente_id)
        if not cliente:
            return False, f"Cliente con ID {cliente_id} no encontrado"

        # Actualizar solo los campos proporcionados
        if nombre is not None and nombre.strip():
            cliente.nombre = nombre

        if edad is not None:
            if edad == "":
                pass  # Mantener la edad actual
            else:
                cliente.edad = edad

        if telefono is not None:
            if telefono == "":
                pass  # Mantener el teléfono actual
            else:
                cliente.telefono = telefono

        try:
            if documento is not None:
                if documento == "":
                    pass  # Mantener el documento actual
                else:
                    documento_int = int(documento)
                    cliente.documento = documento_int

            # Guardar los cambios
            if Cliente.update(cliente):
                return True, f"Cliente '{cliente.nombre}' actualizado correctamente"
            else:
                return False, "Error al actualizar el cliente en la base de datos"
        except ValueError:
            return False, "El documento debe ser un número"

    @staticmethod
    def eliminar_cliente(cliente_id):
        """Elimina un cliente por su ID"""
        try:
            cliente_id = int(cliente_id)
            cliente = Cliente.delete(cliente_id)
            if cliente:
                return True, f"Cliente '{cliente.nombre}' eliminado correctamente"
            else:
                return (
                    False,
                    f"Cliente con ID {cliente_id} no encontrado o error al eliminar",
                )
        except ValueError:
            return False, "El ID del cliente debe ser un número"

    @staticmethod
    def buscar_clientes_por_nombre(nombre):
        """Busca clientes que contengan el texto proporcionado en su nombre"""
        clientes = Cliente.get_all()
        return [c for c in clientes if nombre.lower() in c.nombre.lower()]
    
    @staticmethod
    def contar_clientes():
        """Cuenta el número total de clientes en la base de datos"""
        return Cliente.count_all()
