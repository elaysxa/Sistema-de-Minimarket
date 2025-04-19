import tkinter as tk
from tkinter import ttk, messagebox
from controller.cliente_controller import ClienteController

class ClientesUI:
    def __init__(self, parent):
        # Asigna el contenedor recibido a main_frame
        self.main_frame = ttk.Frame(parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.setup_ui()
        self.load_clients()

    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Configuración de estilos
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Poppins", 11), padding=5)
        self.style.configure("TLabel", font=("Poppins", 11))
        self.style.configure("Header.TLabel", font=("Poppins", 14, "bold"), background="#2c3e50")

       
        
        # Frame para los botones principales
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, sticky="nw", padx=(0, 20))

        # Botones de acción
        self.btn_add = ttk.Button(
            self.button_frame, text="Agregar Cliente", command=self.show_add_form
        )
        self.btn_add.pack(fill=tk.X, pady=5)

        self.btn_edit = ttk.Button(
            self.button_frame, text="Modificar Cliente", command=self.show_edit_form
        )
        self.btn_edit.pack(fill=tk.X, pady=5)

        self.btn_delete = ttk.Button(
            self.button_frame, text="Eliminar Cliente", command=self.delete_client
        )
        self.btn_delete.pack(fill=tk.X, pady=5)

        self.btn_refresh = ttk.Button(
            self.button_frame, text="Actualizar Lista", command=self.load_clients
        )
        self.btn_refresh.pack(fill=tk.X, pady=5)

        # Frame para la búsqueda
        self.search_frame = ttk.Frame(self.button_frame)
        self.search_frame.pack(fill=tk.X, pady=15)

        self.search_label = ttk.Label(self.search_frame, text="Buscar por nombre:")
        self.search_label.pack(anchor="w")

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, pady=5)

        self.btn_search = ttk.Button(
            self.search_frame, text="Buscar", command=self.search_clients
        )
        self.btn_search.pack(fill=tk.X)

        # Frame para la tabla de clientes
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.grid(row=1, column=1, sticky="nsew")

        # Crear el Treeview para la lista de clientes
        self.tree_columns = ("id", "nombre", "edad", "telefono", "documento")
        self.tree = ttk.Treeview(
            self.table_frame, columns=self.tree_columns, show="headings"
        )
        #Encabezados
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading",
            background="white",
            bordercolor="#b3b3cc",
            borderwidth=1,
            relief="flat",
            foreground="black",
            font=("Poppins", 11, "bold"),
            padding=6)
        
        #Filas
        self.style.configure("Treeview",
            background="white",
            foreground="black",
            rowheight=28,
            fieldbackground="white",
            font=("Poppins", 10))
        
        self.style.map("Treeview",
            background=[("selected", "#b3ecff")],
            foreground=[("selected", "black")])

        # Definir encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("edad", text="Edad")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("documento", text="Documento")

        # Definir anchos de columna
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=200)
        self.tree.column("edad", width=80, anchor="center")
        self.tree.column("telefono", width=120, anchor="center")
        self.tree.column("documento", width=120)

        # Scrollbar para el Treeview
        self.scrollbar = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetar el Treeview y el scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Configurar grid para que la tabla ocupe más espacio
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def load_clients(self):
        """Cargar la lista de clientes en el Treeview"""
        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener clientes y agregarlos al Treeview
        clientes = ClienteController.obtener_todos_clientes()
        for cliente in clientes:
            self.tree.insert(
                "",
                "end",
                values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.edad,
                    cliente.telefono,
                    cliente.documento if cliente.documento else "-"
                ),
            )

    def search_clients(self):
        """Buscar clientes por nombre"""
        search_text = self.search_var.get().strip()
        if not search_text:
            self.load_clients()
            return

        # Buscar clientes
        clientes = ClienteController.buscar_clientes_por_nombre(search_text)

        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Mostrar resultados
        for cliente in clientes:
            self.tree.insert(
                "",
                "end",
                values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.edad,
                    cliente.telefono,
                    cliente.documento if cliente.documento else "-"
                ),
            )

    def get_selected_client_id(self):
        """Obtener el ID del cliente seleccionado en el Treeview"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Selección", "Seleccione un cliente de la lista.")
            return None
        return self.tree.item(selected_items[0])["values"][0]

    def show_add_form(self):
        """Mostrar formulario para agregar un cliente"""
        # Se utiliza self.main_frame.winfo_toplevel() para obtener la ventana raíz
        self.add_window = tk.Toplevel(self.main_frame.winfo_toplevel())
        self.add_window.title("Agregar Nuevo Cliente")
        self.add_window.geometry("400x300")
        self.add_window.configure(bg="#f0f0f0")
        self.add_window.resizable(False, False)

        # Frame del formulario
        form_frame = ttk.Frame(self.add_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Labels y campos de entrada
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        nombre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=nombre_var, width=30).grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Edad:").grid(row=1, column=0, sticky="w", pady=5)
        edad_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=edad_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=5)
        telefono_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=telefono_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Documento (opcional):").grid(row=3, column=0, sticky="w", pady=5)
        documento_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=documento_var, width=30).grid(row=3, column=1, pady=5)

        # Frame para los botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(
            button_frame,
            text="Guardar",
            command=lambda: self.save_client(
                nombre_var.get(),
                edad_var.get(),
                telefono_var.get(),
                documento_var.get(),
            )
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.add_window.destroy).pack(side=tk.LEFT, padx=5)

    def save_client(self, nombre, edad, telefono, documento):
        """Guardar un nuevo cliente"""
        if not nombre.strip():
            messagebox.showerror("Error", "El nombre del cliente no puede estar vacío.")
            return

        if not documento.strip():
            documento = None

        exito, mensaje = ClienteController.crear_cliente(nombre, edad, telefono, documento)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.add_window.destroy()
            self.load_clients()
        else:
            messagebox.showerror("Error", mensaje)

    def show_edit_form(self):
        """Mostrar formulario para editar un cliente seleccionado"""
        cliente_id = self.get_selected_client_id()
        if cliente_id is None:
            return

        # Obtener datos del cliente
        cliente = ClienteController.obtener_cliente_por_id(cliente_id)
        if not cliente:
            messagebox.showerror("Error", f"No se encontró el cliente con ID {cliente_id}")
            return

        self.edit_window = tk.Toplevel(self.main_frame.winfo_toplevel())
        self.edit_window.title(f"Editar Cliente: {cliente.nombre}")
        self.edit_window.geometry("400x300")
        self.edit_window.configure(bg="#f0f0f0")
        self.edit_window.resizable(False, False)

        # Frame del formulario
        form_frame = ttk.Frame(self.edit_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Labels y entradas con valores actuales
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        nombre_var = tk.StringVar(value=cliente.nombre)
        ttk.Entry(form_frame, textvariable=nombre_var, width=30).grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Edad:").grid(row=1, column=0, sticky="w", pady=5)
        edad_var = tk.StringVar(value=str(cliente.edad))
        ttk.Entry(form_frame, textvariable=edad_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=5)
        telefono_var = tk.StringVar(value=cliente.telefono)
        ttk.Entry(form_frame, textvariable=telefono_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Documento:").grid(row=3, column=0, sticky="w", pady=5)
        documento_var = tk.StringVar(value=str(cliente.documento) if cliente.documento else "")
        ttk.Entry(form_frame, textvariable=documento_var, width=30).grid(row=3, column=1, pady=5)

        # Frame para botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(
            button_frame,
            text="Guardar",
            command=lambda: self.update_client(
                cliente_id,
                nombre_var.get(),
                edad_var.get(),
                telefono_var.get(),
                documento_var.get(),
            )
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.edit_window.destroy).pack(side=tk.LEFT, padx=5)

    def update_client(self, cliente_id, nombre, edad, telefono, documento):
        """Actualizar un cliente existente"""
        if not documento.strip():
            documento = None

        exito, mensaje = ClienteController.actualizar_cliente(cliente_id, nombre, edad, telefono, documento)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.edit_window.destroy()
            self.load_clients()
        else:
            messagebox.showerror("Error", mensaje)

    def delete_client(self):
        """Eliminar un cliente seleccionado"""
        cliente_id = self.get_selected_client_id()
        if cliente_id is None:
            return

        if not messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el cliente con ID {cliente_id}?"):
            return

        exito, mensaje = ClienteController.eliminar_cliente(cliente_id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.load_clients()
        else:
            messagebox.showerror("Error", mensaje)

