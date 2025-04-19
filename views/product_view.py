import tkinter as tk
from tkinter import ttk, messagebox
from controller.producto_controller import ProductoController


class ProductosUI:
    def __init__(self, parent):
        # Asigna el contenedor recibido a main_frame
        self.main_frame = ttk.Frame(parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.setup_ui()
        self.load_products()

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
            self.button_frame, text="Agregar Producto", command=self.show_add_form
        )
        self.btn_add.pack(fill=tk.X, pady=5)

        self.btn_edit = ttk.Button(
            self.button_frame, text="Modificar Producto", command=self.show_edit_form
        )
        self.btn_edit.pack(fill=tk.X, pady=5)

        self.btn_delete = ttk.Button(
            self.button_frame, text="Eliminar Producto", command=self.delete_product
        )
        self.btn_delete.pack(fill=tk.X, pady=5)

        self.btn_refresh = ttk.Button(
            self.button_frame, text="Actualizar Lista", command=self.load_products
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
            self.search_frame, text="Buscar", command=self.search_products
        )
        self.btn_search.pack(fill=tk.X)

        # Frame para la tabla de productos
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.grid(row=1, column=1, sticky="nsew")

        # Crear Treeview para la lista de productos
        self.tree_columns = ("id", "nombre", "precio", "cantidad")
        self.tree = ttk.Treeview(
            self.table_frame, columns=self.tree_columns, show="headings"
        )
         #Encabezados
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading",
            background="#white",
            foreground="black",
            font=("Poppins", 11, "bold"))
        
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
        self.tree.heading("precio", text="Precio")
        self.tree.heading("cantidad", text="Stock")

        # Definir anchos de columna
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=250)
        self.tree.column("precio", width=100, anchor="center")
        self.tree.column("cantidad", width=100, anchor="center")

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetar Treeview y scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Configurar grid para que la tabla ocupe más espacio
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def load_products(self):
        """Cargar la lista de productos en el Treeview"""
        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener productos y agregarlos al Treeview
        productos = ProductoController.obtener_todos_productos()
        for producto in productos:
            self.tree.insert(
                "",
                "end",
                values=(
                    producto.id,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.cantidad,
                ),
            )

    def search_products(self):
        """Buscar productos por nombre"""
        search_text = self.search_var.get().strip()
        if not search_text:
            self.load_products()
            return

        # Buscar productos
        productos = ProductoController.buscar_productos_por_nombre(search_text)

        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Mostrar resultados
        for producto in productos:
            self.tree.insert(
                "",
                "end",
                values=(
                    producto.id,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.cantidad,
                ),
            )

    def get_selected_product_id(self):
        """Obtener el ID del producto seleccionado en el Treeview"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Selección", "Seleccione un producto de la lista.")
            return None

        return self.tree.item(selected_items[0])["values"][0]

    def show_add_form(self):
        """Mostrar formulario para agregar un producto"""
        self.add_window = tk.Toplevel(self.main_frame.winfo_toplevel())
        self.add_window.title("Agregar Nuevo Producto")
        self.add_window.geometry("400x300")
        self.add_window.configure(bg="#f0f0f0")
        self.add_window.resizable(False, False)

        # Form frame
        form_frame = ttk.Frame(self.add_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Labels y entradas de texto
        ttk.Label(form_frame, text="Nombre del Producto:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        nombre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=nombre_var, width=30).grid(
            row=0, column=1, pady=5
        )

        ttk.Label(form_frame, text="Precio:").grid(row=1, column=0, sticky="w", pady=5)
        precio_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=precio_var, width=30).grid(
            row=1, column=1, pady=5
        )

        ttk.Label(form_frame, text="Cantidad en Stock:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        cantidad_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=cantidad_var, width=30).grid(
            row=2, column=1, pady=5
        )

        # Frame para botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        # Botones
        ttk.Button(
            button_frame,
            text="Guardar",
            command=lambda: self.save_product(
                nombre_var.get(), precio_var.get(), cantidad_var.get()
            ),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.add_window.destroy).pack(
            side=tk.LEFT, padx=5
        )

    def save_product(self, nombre, precio, cantidad):
        """Guardar un nuevo producto"""
        if not nombre.strip():
            messagebox.showerror(
                "Error", "El nombre del producto no puede estar vacío."
            )
            return

        exito, mensaje = ProductoController.crear_producto(nombre, precio, cantidad)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.add_window.destroy()
            self.load_products()
        else:
            messagebox.showerror("Error", mensaje)

    def show_edit_form(self):
        """Mostrar formulario para editar un producto seleccionado"""
        producto_id = self.get_selected_product_id()
        if producto_id is None:
            return

        # Obtener datos del producto
        producto = ProductoController.obtener_producto_por_id(producto_id)
        if not producto:
            messagebox.showerror(
                "Error", f"No se encontró el producto con ID {producto_id}"
            )
            return

        # Crear ventana para editar
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title(f"Editar Producto: {producto.nombre}")
        self.edit_window.geometry("400x300")
        self.edit_window.configure(bg="#f0f0f0")
        self.edit_window.resizable(False, False)

        # Form frame
        form_frame = ttk.Frame(self.edit_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Labels y entradas de texto con valores actuales
        ttk.Label(form_frame, text="Nombre del Producto:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        nombre_var = tk.StringVar(value=producto.nombre)
        ttk.Entry(form_frame, textvariable=nombre_var, width=30).grid(
            row=0, column=1, pady=5
        )

        ttk.Label(form_frame, text="Precio:").grid(row=1, column=0, sticky="w", pady=5)
        precio_var = tk.StringVar(value=str(producto.precio))
        ttk.Entry(form_frame, textvariable=precio_var, width=30).grid(
            row=1, column=1, pady=5
        )

        ttk.Label(form_frame, text="Cantidad en Stock:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        cantidad_var = tk.StringVar(value=str(producto.cantidad))
        ttk.Entry(form_frame, textvariable=cantidad_var, width=30).grid(
            row=2, column=1, pady=5
        )

        # Frame para botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        # Botones
        ttk.Button(
            button_frame,
            text="Guardar",
            command=lambda: self.update_product(
                producto_id, nombre_var.get(), precio_var.get(), cantidad_var.get()
            ),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Cancelar", command=self.edit_window.destroy
        ).pack(side=tk.LEFT, padx=5)

    def update_product(self, producto_id, nombre, precio, cantidad):
        """Actualizar un producto existente"""
        exito, mensaje = ProductoController.actualizar_producto(
            producto_id, nombre, precio, cantidad
        )
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.edit_window.destroy()
            self.load_products()
        else:
            messagebox.showerror("Error", mensaje)

    def delete_product(self):
        """Eliminar un producto seleccionado"""
        producto_id = self.get_selected_product_id()
        if producto_id is None:
            return

        # Confirmar eliminación
        if not messagebox.askyesno(
            "Confirmar", f"¿Está seguro de eliminar el producto con ID {producto_id}?"
        ):
            return

        # Eliminar producto
        exito, mensaje = ProductoController.eliminar_producto(producto_id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.load_products()
        else:
            messagebox.showerror("Error", mensaje)
