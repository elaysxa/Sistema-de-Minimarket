import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font
from controller.cliente_controller import ClienteController
from controller.factura_controller import FacturaController
from controller.producto_controller import ProductoController
from models.cliente import Cliente
from models.factura import Factura


class FacturaUI:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.crear_factura()

    def setup_ui(self):

        self.style = ttk.Style()
        self.style.configure("TCombobox",  font=("Poppins", 11))
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Poppins", 11), padding=5)
        self.style.configure("TLabel", font=("Poppins", 11))
        self.style.configure("Header.TLabel", font=("Poppins", 14, "bold"), background="#2c3e50")
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

        self.sidebar = ttk.Frame(self.root, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.btn_add = ttk.Button(self.sidebar, text="Crear Factura", command=self.crear_factura)
        self.btn_add.pack(fill=tk.X, padx=10, pady=5)

        self.btn_delete = ttk.Button(self.sidebar, text="Eliminar Factura", command=self.eliminar_factura)
        self.btn_delete.pack(fill=tk.X, padx=10, pady=5)

        self.btn_refresh = ttk.Button(self.sidebar, text="Modificar Factura", command=self.modificar_factura)
        self.btn_refresh.pack(fill=tk.X, padx=10, pady=5)

        self.btn_listar = ttk.Button(self.sidebar, text="Listar Facturas", command=self.mostrar_listado_facturas)
        self.btn_listar.pack(fill=tk.X, padx=10, pady=5)

        self.search_label = ttk.Label(self.sidebar, text="Buscar por cliente:")
        self.search_label.pack(anchor="w", padx=10, pady=(20, 0))

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.sidebar, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=10, pady=5)

        self.btn_search = ttk.Button(self.sidebar, text="Buscar", command=self.buscar_facturas)
        self.btn_search.pack(fill=tk.X, padx=10)

        self.topbar = ttk.Frame(self.root, height=50)
        self.topbar.pack(side="top", fill="x")
        self.topbar_label = ttk.Label(self.topbar, text="Listado de Facturas", font=("Arial", 13, "bold"))
        self.topbar_label.pack(side="left", padx=20, pady=10)

        self.content = ttk.Frame(self.root)
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tree_columns = ("id", "cliente", "fecha", "total")
        self.tree = ttk.Treeview(self.content, columns=self.tree_columns, show="headings")

        for col in self.tree_columns:
            self.tree.heading(col, text=col.capitalize())

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("cliente", width=200)
        self.tree.column("fecha", width=120, anchor="center")
        self.tree.column("total", width=100, anchor="e")

        self.tree.pack(fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

    def mostrar_listado_facturas(self):
        self.limpiar_contenido()
        self.topbar_label.config(text="Listado de Facturas")

        self.tree = ttk.Treeview(self.content, columns=("id", "cliente", "fecha", "total"), show="headings")
        for col in ("id", "cliente", "fecha", "total"):
            self.tree.heading(col, text=col.capitalize())

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("cliente", width=200)
        self.tree.column("fecha", width=120, anchor="center")
        self.tree.column("total", width=100, anchor="e")

        self.tree.pack(fill="both", expand=True)

        facturas = FacturaController.obtener_todas_facturas()
        for factura in facturas:
            cliente = Cliente.get_by_id(factura.cliente_id)
            cliente_nombre = cliente.nombre if cliente else "Desconocido"
            fecha = factura.fecha if factura.fecha else "N/A"
            self.tree.insert("", "end", values=(factura.id, cliente_nombre, fecha, f"${factura.total:.2f}"))

    def modificar_factura(self):
        factura_id = self.get_factura_id_seleccionada()
        
        if factura_id is None:
            return

        factura = Factura.get_by_id(factura_id)
        if not factura:
            messagebox.showerror("Error", "Factura no encontrada.")
            return

        self.limpiar_contenido()
        self.topbar_label.config(text=f"Modificar Factura #{factura.id}")

        clientes = Cliente.get_all()
        productos = ProductoController.obtener_todos_productos()
        items_factura = FacturaController.obtener_items_por_factura_id(factura.id)
       

        ttk.Label(self.content, text="Cliente:").pack(anchor="w", padx=10, pady=5)

        cliente_var = tk.StringVar()
        cliente_cb = ttk.Combobox(self.content, textvariable=cliente_var, state="readonly")

        # Obtener todos los clientes
        clientes = Cliente.get_all()
        valores_clientes = [f"{c.id} - {c.nombre}" for c in clientes]

        cliente_cb = ttk.Combobox(self.content, state="readonly")
        cliente_cb["values"] = valores_clientes
        cliente_cb.pack(fill="x", padx=10)

        cliente_id = factura.cliente_id
        cliente_actual = ClienteController.obtener_cliente_por_id(cliente_id)

        if cliente_actual:
            cliente_str = f"{cliente_actual.id} - {cliente_actual.nombre}"
            cliente_cb.set(cliente_str)
        
        ttk.Label(self.content, text="Productos disponibles:").pack(anchor="w", padx=10, pady=10)
        producto_tree = ttk.Treeview(self.content, columns=("id", "nombre", "precio", "stock"), show="headings", height=6)
        for col in ("id", "nombre", "precio", "stock"):
            producto_tree.heading(col, text=col.capitalize())
        producto_tree.pack(fill="x", padx=10)
        for p in productos:
            producto_tree.insert("", "end", values=(p.id, p.nombre, f"${p.precio:.2f}", p.cantidad))

        ttk.Label(self.content, text="Cantidad:").pack(anchor="w", padx=10, pady=5)
        cantidad_var = tk.StringVar()
        ttk.Entry(self.content, textvariable=cantidad_var).pack(fill="x", padx=10)

        ttk.Label(self.content, text="Productos agregados:").pack(anchor="w", padx=10, pady=(10, 0))
        items_tree = ttk.Treeview(self.content, columns=("producto_id", "nombre", "cantidad", "subtotal"), show="headings", height=5)
        for col in ("producto_id", "nombre", "cantidad", "subtotal"):
            items_tree.heading(col, text=col.capitalize())
        items_tree.pack(fill="x", padx=10, pady=5)

        items = []
        total_var = tk.StringVar(value="Total $0.00")

        # Cargar ítems actuales
        for item in items_factura:
            if item.producto_id is None:
                continue
            producto = ProductoController.obtener_producto_por_id(item.producto_id)
            if producto:
                subtotal = producto.precio * item.cantidad
                items.append({"producto_id": producto.id, "cantidad": item.cantidad})
                items_tree.insert("", "end", values=(producto.id, producto.nombre, item.cantidad, f"${subtotal:.2f}"))
        total = sum(ProductoController.obtener_producto_por_id(i["producto_id"]).precio * i["cantidad"] for i in items)
        total_var.set(f"Total: ${total:.2f}")

        def agregar_item():
            selected = producto_tree.selection()
            if not selected:
                messagebox.showwarning("Atención", "Seleccione un producto.")
                return
            producto_id = int(producto_tree.item(selected[0])["values"][0])
            producto = next((p for p in productos if p.id == producto_id), None)
            if not producto:
                messagebox.showerror("Error", "Producto no válido.")
                return
            try:
                cantidad = int(cantidad_var.get())
                if cantidad <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida.")
                return
            if cantidad > producto.cantidad:
                messagebox.showerror("Error", "Stock insuficiente.")
                return
            subtotal = producto.precio * cantidad
            items.append({"producto_id": producto.id, "cantidad": cantidad})
            items_tree.insert("", "end", values=(producto.id, producto.nombre, cantidad, f"${subtotal:.2f}"))
            total = sum(ProductoController.obtener_producto_por_id(i["producto_id"]).precio * i["cantidad"] for i in items)
            total_var.set(f"Total: ${total:.2f}")

        def eliminar_item():
            seleccion = items_tree.selection()
            if not seleccion:
                messagebox.showwarning("Atención", "Seleccione un producto a eliminar.")
                return
            indice = items_tree.index(seleccion[0])
            items.pop(indice)
            items_tree.delete(seleccion[0])
            total = sum(ProductoController.obtener_producto_por_id(i["producto_id"]).precio * i["cantidad"] for i in items)
            total_var.set(f"Total: ${total:.2f}")

        def guardar_cambios():
            if not cliente_cb.get():
                messagebox.showerror("Error", "Seleccione un cliente.")
                return
            if not items:
                messagebox.showerror("Error", "Agregue al menos un producto.")
                return
            cliente_id = int(cliente_cb.get().split(" - ")[0])
            exito, mensaje = FacturaController.modificar_factura(factura.id, cliente_id, items)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.mostrar_listado_facturas()
            else:
                messagebox.showerror("Error", mensaje)

        
        def modificar_cantidad():
            seleccion = items_tree.selection()
            if not seleccion:
                messagebox.showwarning("Atención", "Seleccione un producto para modificar la cantidad.")
                return

            item_index = items_tree.index(seleccion[0])
            producto_id = items[item_index]["producto_id"]
            producto = ProductoController.obtener_producto_por_id(producto_id)

            if not producto:
                messagebox.showerror("Error", "Producto no encontrado.")
                return

            nueva_cantidad_str = simpledialog.askstring("Modificar cantidad", f"Ingrese nueva cantidad para {producto.nombre}:")
            if nueva_cantidad_str is None:
                return  # Cancelado

            try:
                nueva_cantidad = int(nueva_cantidad_str)
                if nueva_cantidad <= 0:
                    raise ValueError
                if nueva_cantidad > producto.cantidad:
                    messagebox.showerror("Error", "Stock insuficiente.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida.")
                return

            # Actualizar en lista interna
            items[item_index]["cantidad"] = nueva_cantidad

            # Actualizar en treeview
            subtotal = producto.precio * nueva_cantidad
            items_tree.item(seleccion[0], values=(producto.id, producto.nombre, nueva_cantidad, f"${subtotal:.2f}"))

            # Recalcular total
            total = sum(ProductoController.obtener_producto_por_id(i["producto_id"]).precio * i["cantidad"] for i in items)
            total_var.set(f"Total: ${total:.2f}")
        
        boton_total_frame = ttk.Frame(self.content)
        boton_total_frame.pack(pady=10)
        ttk.Button(boton_total_frame, text="Agregar Producto", command=agregar_item).pack(side="left", padx=5)
        ttk.Button(boton_total_frame, text="Eliminar Producto", command=eliminar_item).pack(side="left", padx=5)
        ttk.Button(boton_total_frame, text="Guardar Cambios", command=guardar_cambios).pack(side="left", padx=5)
        ttk.Button(boton_total_frame, text="Modificar Cantidad", command=modificar_cantidad).pack(side="left", padx=5)
        ttk.Label(self.content, textvariable=total_var, font=("Poppins", 11, "bold")).pack(pady=5)

    def load_facturas(self):
        self.tree.delete(*self.tree.get_children())
        facturas = FacturaController.obtener_todas_facturas()
        for factura in facturas:
            cliente = Cliente.get_by_id(factura.cliente_id)
            cliente_nombre = cliente.nombre if cliente else "Desconocido"
            fecha = factura.fecha if factura.fecha else "N/A"
            self.tree.insert("", "end", values=(factura.id, cliente_nombre, fecha, f"${factura.total:.2f}"))

    def buscar_facturas(self):
        texto = self.search_var.get().strip().lower()
        if not texto:
            self.load_facturas()
            return
        clientes = Cliente.get_all()
        clientes_filtrados = [c for c in clientes if texto in c.nombre.lower()]
        ids_clientes = [c.id for c in clientes_filtrados]
        facturas = FacturaController.obtener_todas_facturas()
        facturas_filtradas = [f for f in facturas if f.cliente_id in ids_clientes]
        self.tree.delete(*self.tree.get_children())
        for factura in facturas_filtradas:
            cliente = Cliente.get_by_id(factura.cliente_id)
            cliente_nombre = cliente.nombre if cliente else "Desconocido"
            fecha = factura.fecha if factura.fecha else "N/A"
            self.tree.insert("", "end", values=(factura.id, cliente_nombre, fecha, f"${factura.total:.2f}"))

    def get_factura_id_seleccionada(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Seleccione una factura de la lista.")
            return None
        return self.tree.item(seleccion[0])["values"][0]

    def eliminar_factura(self):
        factura_id = self.get_factura_id_seleccionada()
        if factura_id is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar factura con ID {factura_id}?"):
            return
        exito, mensaje = FacturaController.eliminar_factura(factura_id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.load_facturas()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_contenido(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def crear_factura(self):
        self.limpiar_contenido()
        self.topbar_label.config(text="Crear Factura")

        clientes = Cliente.get_all()
        productos = ProductoController.obtener_todos_productos()

        ttk.Label(self.content, text="Cliente:").pack(anchor="w", padx=10, pady=5)
        cliente_var = tk.StringVar()
        cliente_cb = ttk.Combobox(self.content, textvariable=cliente_var, state="readonly", font="Poppins")
        cliente_cb["values"] = [f"{c.id} - {c.nombre}" for c in clientes]
        cliente_cb.pack(fill="x", padx=10)

        ttk.Label(self.content, text="Productos disponibles:").pack(anchor="w", padx=10, pady=10)
        producto_tree = ttk.Treeview(self.content, columns=("id", "nombre", "precio", "stock"), show="headings", height=6)
        for col in ("id", "nombre", "precio", "stock"):
            producto_tree.heading(col, text=col.capitalize())
        producto_tree.pack(fill="x", padx=10)
        for p in productos:
            producto_tree.insert("", "end", values=(p.id, p.nombre, f"${p.precio:.2f}", p.cantidad))

        ttk.Label(self.content, text="Cantidad:").pack(anchor="w", padx=10, pady=5)
        cantidad_var = tk.StringVar()
        ttk.Entry(self.content, textvariable=cantidad_var).pack(fill="x", padx=10)

        ttk.Label(self.content, text="Productos agregados:").pack(anchor="w", padx=10, pady=(10, 0))
        items_tree = ttk.Treeview(self.content, columns=("producto_id", "nombre", "cantidad", "subtotal"), show="headings", height=5)
        for col in ("producto_id", "nombre", "cantidad", "subtotal"):
            items_tree.heading(col, text=col.capitalize())
        items_tree.pack(fill="x", padx=10, pady=5)

        items = []
        total_var = tk.StringVar(value="Total: $0.00")

        def agregar_item():
            selected = producto_tree.selection()
            if not selected:
                messagebox.showwarning("Atención", "Seleccione un producto.")
                return
            producto_id = int(producto_tree.item(selected[0])["values"][0])
            producto = next((p for p in productos if p.id == producto_id), None)
            if not producto:
                messagebox.showerror("Error", "Producto no válido.")
                return
            try:
                cantidad = int(cantidad_var.get())
                if cantidad <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida.")
                return
            if cantidad > producto.cantidad:
                messagebox.showerror("Error", "Stock insuficiente.")
                return
            subtotal = producto.precio * cantidad
            items.append({"producto_id": producto.id, "cantidad": cantidad})
            items_tree.insert("", "end", values=(producto.id, producto.nombre, cantidad, f"${subtotal:.2f}"))
            total = sum(ProductoController.obtener_producto_por_id(i["producto_id"]).precio * i["cantidad"] for i in items)
            total_var.set(f"Total: ${total:.2f}")

        def eliminar_item():
            seleccion = items_tree.selection()
            if not seleccion:
                messagebox.showwarning("Atención", "Seleccione un producto a eliminar.")
                return
            indice = items_tree.index(seleccion[0])
            items.pop(indice)
            items_tree.delete(seleccion[0])
            total = sum(ProductoController.obtener_producto_por_id(i["producto_id"]).precio * i["cantidad"] for i in items)
            total_var.set(f"Total: ${total:.2f}")

        def guardar_factura():
            if not cliente_cb.get():
                messagebox.showerror("Error", "Seleccione un cliente.")
                return
            if not items:
                messagebox.showerror("Error", "Agregue al menos un producto.")
                return
            cliente_id = int(cliente_cb.get().split(" - ")[0])
            exito, mensaje = FacturaController.crear_factura(cliente_id, items)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.crear_factura()
            else:
                messagebox.showerror("Error", mensaje)
        def modificar_cantidad():
            seleccion = items_tree.selection()
            if not seleccion:
                messagebox.showwarning("Atención", "Seleccione un producto para modificar la cantidad.")
                return

            item_index = items_tree.index(seleccion[0])
            producto_id = items[item_index]["producto_id"]
            producto = ProductoController.obtener_producto_por_id(producto_id)

            if not producto:
                messagebox.showerror("Error", "Producto no encontrado.")
                return

            nueva_cantidad_str = simpledialog.askinteger("Modificar cantidad", f"Ingrese nueva cantidad para {producto.nombre}:")
            if nueva_cantidad_str is None:
                return  # Cancelado

            try:
                nueva_cantidad = int(nueva_cantidad_str)
                if nueva_cantidad <= 0:
                    raise ValueError
                if nueva_cantidad > producto.cantidad:
                    messagebox.showerror("Error", "Stock insuficiente.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida.")
                return

            # Actualizar en lista interna
            items[item_index]["cantidad"] = nueva_cantidad

            # Actualizar en treeview
            subtotal = producto.precio * nueva_cantidad
            items_tree.item(seleccion[0], values=(producto.id, producto.nombre, nueva_cantidad, f"${subtotal:.2f}"))

            # Recalcular total
            total = sum(ProductoController.obtener_producto_por_id(i["producto_id"]).precio * i["cantidad"] for i in items)
            total_var.set(f"Total: ${total:.2f}")

        boton_total_frame = ttk.Frame(self.content)
        boton_total_frame.pack(pady=10)

        ttk.Button(boton_total_frame, text="Agregar Producto", command=agregar_item).pack(side="left", padx=5)
        ttk.Button(boton_total_frame, text="Eliminar Producto", command=eliminar_item).pack(side="left", padx=5)
        ttk.Button(boton_total_frame, text="Guardar Factura", command=guardar_factura).pack(side="left", padx=5)
        ttk.Button(boton_total_frame, text="Modificar Cantidad", command=modificar_cantidad).pack(side="left", padx=5)

        ttk.Label(boton_total_frame, textvariable=total_var, font=("Poppins", 12, "bold")).pack(side="left", padx=10)
