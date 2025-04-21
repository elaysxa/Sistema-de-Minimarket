import tkinter as tk
from tkinter import ttk, messagebox
from controller.factura_controller import FacturaController
from controller.cliente_controller import ClienteController
from controller.producto_controller import ProductoController

class FacturaUI:
    def __init__(self, root):
        self.root = root
        self.productos_disponibles = []
        self.items_factura = []
        self.total_var = tk.StringVar(value="Total: $0.00")
        self.setup_ui()

        self.marco_botones = ttk.Frame(self.root)
        self.marco_botones.pack(pady=10)

        ttk.Button(self.marco_botones, text="Crear Factura", command=self.mostrar_formulario_crear).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.marco_botones, text="Listar Facturas", command=self.listar_facturas).pack(side=tk.LEFT, padx=10)

        self.marco_formulario = ttk.Frame(self.root)
        self.marco_formulario.pack(fill='both', expand=False)

    def setup_ui(self):
        self.style = ttk.Style()
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
            padding=2)

        self.style.configure("Treeview",
            background="white",
            foreground="black",
            rowheight=28,
            fieldbackground="white",
            font=("Poppins", 10))

        self.style.map("Treeview",
            background=[("selected", "#b3ecff")],
            foreground=[("selected", "black")])

    def mostrar_formulario_crear(self):
        for widget in self.marco_formulario.winfo_children():
            widget.destroy()

        self.items_factura = []
        self.total_var.set("Total: $0.00")

        ttk.Label(self.marco_formulario, text="Cliente:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cliente_combobox = ttk.Combobox(self.marco_formulario, width=40, state="readonly")
        clientes = ClienteController.obtener_todos_clientes()
        self.clientes_dict = {f"{c.nombre} (ID: {c.id})": c.id for c in clientes}
        self.cliente_combobox['values'] = list(self.clientes_dict.keys())
        self.cliente_combobox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        marco_tablas = ttk.Frame(self.marco_formulario)
        marco_tablas.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        ttk.Label(marco_tablas, text="Productos disponibles").grid(row=0, column=0)
        self.tabla_productos = ttk.Treeview(marco_tablas, columns=("nombre", "precio"), show="headings", height=12)
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("precio", text="Precio")
        self.tabla_productos.column("nombre", width=200)
        self.tabla_productos.column("precio", width=80)
        self.tabla_productos.grid(row=1, column=0, padx=(0,2))
        self.tabla_productos.bind("<Double-1>", self.agregar_producto)

        ttk.Label(marco_tablas, text="Items en factura").grid(row=0, column=1)
        self.tabla_items = ttk.Treeview(marco_tablas, columns=("nombre", "precio", "cantidad", "subtotal"), show="headings", height=12)
        self.tabla_items.heading("nombre", text="Nombre")
        self.tabla_items.heading("precio", text="Precio")
        self.tabla_items.heading("cantidad", text="Cantidad")
        self.tabla_items.heading("subtotal", text="Subtotal")
        for col in ("nombre", "precio", "cantidad", "subtotal"):
            self.tabla_items.column(col, width=140)
        self.tabla_items.grid(row=1, column=1, padx=10)

        ttk.Button(marco_tablas, text="Eliminar item", command=self.eliminar_item).grid(row=2, column=1, pady=10)


        contenedor_acciones = ttk.Frame(self.marco_formulario)
        contenedor_acciones.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10)
        contenedor_acciones.columnconfigure(0, weight=1)  

        # Botón a la izquierda
        ttk.Button(marco_tablas, text="Guardar Factura", command=self.guardar_factura).grid(row=2, column=0,pady=10)

# Total a la derecha, ligeramente más arriba
        ttk.Label(marco_tablas, textvariable=self.total_var, style="TLabel").grid(row=2, column=1, sticky="e", padx=5)

        self.cargar_productos()

    def cargar_productos(self):
        self.productos_disponibles = ProductoController.obtener_todos_productos()
        for producto in self.productos_disponibles:
            self.tabla_productos.insert("", tk.END, iid=producto.id, values=(producto.nombre, f"${producto.precio:.2f}"))

    def agregar_producto(self, event):
        seleccionado = self.tabla_productos.selection()
        if not seleccionado:
            return
        producto_id = int(seleccionado[0])
        producto = next((p for p in self.productos_disponibles if p.id == producto_id), None)

        if producto:
            ventana = tk.Toplevel(self.root)
            ventana.title("Cantidad")
            ventana.geometry("350x300")

            ttk.Label(ventana, text=f"Cantidad de '{producto.nombre}':").pack(pady=5)
            entrada_cantidad = ttk.Entry(ventana)
            entrada_cantidad.pack(pady=5)

            def confirmar():
                try:
                    cantidad = int(entrada_cantidad.get())
                    if cantidad <= 0:
                        raise ValueError
                    subtotal = producto.precio * cantidad
                    self.items_factura.append({
                        "producto_id": producto.id,
                        "nombre": producto.nombre,
                        "precio": producto.precio,
                        "cantidad": cantidad,
                        "subtotal": subtotal
                    })
                    self.tabla_items.insert("", tk.END, values=(producto.nombre, f"${producto.precio:.2f}", cantidad, f"${subtotal:.2f}"))
                    self.actualizar_total()
                    ventana.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Cantidad inválida")

            ttk.Button(ventana, text="Agregar", command=confirmar).pack(pady=5)

    def eliminar_item(self):
        seleccionado = self.tabla_items.selection()
        if not seleccionado:
            return
        index = self.tabla_items.index(seleccionado[0])
        self.tabla_items.delete(seleccionado[0])
        del self.items_factura[index]
        self.actualizar_total()

    def actualizar_total(self):
        total = sum(item["subtotal"] for item in self.items_factura)
        self.total_var.set(f"Total: ${total:.2f}")

    def guardar_factura(self):
        cliente_nombre = self.cliente_combobox.get()
        if not cliente_nombre:
            messagebox.showerror("Error", "Seleccione un cliente")
            return

        cliente_id = self.clientes_dict[cliente_nombre]

        if not self.items_factura:
            messagebox.showerror("Error", "La factura no contiene productos")
            return

        resultado, mensaje = FacturaController.crear_factura(cliente_id, self.items_factura)
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.mostrar_formulario_crear()
        else:
            messagebox.showerror("Error", mensaje)

    def listar_facturas(self):
        for widget in self.marco_formulario.winfo_children():
            widget.destroy()

        ttk.Label(self.marco_formulario, text="Listado de Facturas").pack(pady=10)

        tabla = ttk.Treeview(self.marco_formulario, columns=("id", "cliente", "total"), show="headings", height=15)
        tabla.heading("id", text="ID")
        tabla.heading("cliente", text="Cliente ID")
        tabla.heading("total", text="Total")
        tabla.column("id", width=100, anchor="center")
        tabla.column("cliente", width=120, anchor="center")
        tabla.column("total", width=100, anchor="center")
        tabla.pack(padx=30, pady=10,  expand=True)
                # Botones de acción para facturas
        acciones_frame = ttk.Frame(self.marco_formulario)
        acciones_frame.pack(pady=10)

        ttk.Button(acciones_frame, text="Modificar Factura", command=lambda: self.modificar_factura(tabla)).pack(side=tk.LEFT, padx=10)
        ttk.Button(acciones_frame, text="Eliminar Factura", command=lambda: self.eliminar_factura(tabla)).pack(side=tk.LEFT, padx=10)

        for f in FacturaController.obtener_todas_facturas():
            tabla.insert("", tk.END, values=(f.id, f.cliente_id, f.total))
    
    def eliminar_factura(self, tabla):
        
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una factura para eliminar")
            return

        factura_id = tabla.item(seleccion[0])["values"][0]

        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar la factura ID {factura_id}?")
        if confirmar:
            exito = FacturaController.eliminar_factura(factura_id)
            if exito:
                messagebox.showinfo("Éxito", "Factura eliminada correctamente")
                self.listar_facturas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la factura")

    def modificar_factura(self, tabla):
        
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una factura para modificar")
            return

        factura_id = tabla.item(seleccion[0])["values"][0]
        factura = FacturaController.obtener_factura_por_id(factura_id)

        if not factura:
            messagebox.showerror("Error", "Factura no encontrada")
            return

        # Mostrar el formulario con los datos actuales
        self.mostrar_formulario_crear()

        # Preseleccionar cliente
        for nombre, id_ in self.clientes_dict.items():
            if id_ == factura.cliente_id:
                self.cliente_combobox.set(nombre)
                break

        # Llenar tabla de items
        for item in factura.items:
            self.items_factura.append({
                "producto_id": item.producto_id,
                "producto_nombre": item.producto_nombre,
                "precio": item.precio,
                "cantidad": item.cantidad,
                "subtotal": item.subtotal
            })
            self.tabla_items.insert("", tk.END, values=(
                item.producto_nombre,
                f"${item.precio:.2f}",
                item.cantidad,
                f"${item.subtotal:.2f}"
            ))

        # Actualizar total
        total = sum(i["subtotal"] for i in self.items_factura)
        self.total_var.set(f"Total: ${total:.2f}")
        
        # Botón para actualizar factura
        ttk.Button(self.marco_formulario, text="Actualizar Factura", command=lambda: self.actualizar_factura(factura_id)).grid(row=2, column=0)
    
    def actualizar_factura(self, factura_id):
        cliente_nombre = self.cliente_combobox.get()
        if not cliente_nombre:
            messagebox.showerror("Error", "Seleccione un cliente")
            return

        cliente_id = self.clientes_dict[cliente_nombre]
        
        if not self.items_factura:
            messagebox.showerror("Error", "La factura no contiene productos")
            return

        resultado, mensaje = FacturaController.modificar_factura(factura_id, cliente_id, self.items_factura)
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.listar_facturas()
        else:
            messagebox.showerror("Error", mensaje)

