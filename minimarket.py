import tkinter as tk
from tkinter import ttk, messagebox
from views.factura_view import FacturaUI
from views.product_view import ProductosUI
from views.client_view import ClientesUI

class MinimarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Esperanza Minimarket - Sistema de Gestión")
        self.root.geometry("1000x900")
        self.root.resizable(True, True)

        # ===== Tema =====
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TButton", font=("Poppins", 11), padding=8)
        self.style.configure("TLabel", font=("Poppins", 11))
        self.style.configure("Header.TLabel", font=("Poppins", 16, "bold"), background="#2c3e50", foreground="white")

        #Topbar
        self.topbar = tk.Frame(self.root, height=50, bg="#2c3e50")
        self.topbar.pack(side="top", fill="x")

        self.title_label = ttk.Label(self.topbar, text="Inicio", style="Header.TLabel", anchor="center")
        self.title_label.place(x=100, y=10)
        #  Contenedor principal 
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.main_frame, bg="#2c3e50", width=350)
        self.sidebar.pack(side="left", fill="y")

        self.create_sidebar_buttons()

        #  Área de contenido dinámico 
        self.content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Mostrar vista de inicio
        self.mostrar_vista_inicio()

    def create_sidebar_buttons(self):
        opciones = [
            ("Inicio", self.mostrar_vista_inicio),
            ("Productos", self.open_productos),
            ("Clientes", self.open_clientes),
            ("Facturas", self.open_facturas),
            ("Info", self.show_info),
            ("Salir", self.exit_app),
        ]

        for texto, comando in opciones:
            btn = tk.Button(
                self.sidebar, text=texto, command=comando,
                bg="#34495e", fg="white", relief="flat", bd=0 , width=15,
                font=("Poppins", 11), activebackground="#16a085", activeforeground="white"
            )
            btn.pack(fill="x", pady=3, padx=10, ipady=15)

    def actualizar_titulo(self, texto):
        self.title_label.config(text=texto)

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_vista_inicio(self):
        self.actualizar_titulo("Inicio")
        self.limpiar_contenido()
        lbl = ttk.Label(self.content_frame, text="Bienvenido a Esperanza Minimarket", font=("Poppins", 14))
        lbl.pack(pady=20)

    def open_productos(self):
        self.actualizar_titulo("Gestión de Productos")
        self.limpiar_contenido()
        ProductosUI(self.content_frame)  # Asegúrate de que ProductosUI puede usar un frame contenedor

    def open_clientes(self):
        self.actualizar_titulo("Gestión de Clientes")
        self.limpiar_contenido()
        ClientesUI(self.content_frame)  # Igual que arriba

    def open_facturas(self):
        self.actualizar_titulo("Gestión de Facturas")
        self.limpiar_contenido()
        FacturaUI(self.content_frame)

    def show_info(self):
        self.actualizar_titulo("Información")
        self.limpiar_contenido()
        info = """
ESPERANZA MINIMARKET
---------------------
Sistema de Gestión

Desarrollado como proyecto educativo
UTESA - Programación II
2025
"""
        lbl = ttk.Label(self.content_frame, text=info, font=("Poppins", 25), justify="left")
        lbl.pack(pady=20, padx=20)

    def exit_app(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinimarketApp(root)
    root.mainloop()
