from utilidades import separador, limpiar_pantalla, pausar
import os
import db

def imprimir_menu():
    os.system("cls")
    separador()
    print ("MENU DE PRODUCTOS")
    separador()
    print("1. Listar productos")
    print("2. Agregar productos")
    print("3. Modificar producto")
    print("4. Eliminar producto")
    print("5. Salir")
    separador()
    opcion = int(input("Ingrese la opcion deseada: "))
    return opcion

def agregar_producto():
    limpiar_pantalla()
    separador()
    print("AGREGAR PRODUCTO")
    separador()
    #Ingresar datos del producto
    nombre = input("Ingrese el nombre del producto: ")
    precio = float(input("Ingrese el precio del producto: "))
    cantidad = int(input("Ingrese la cantidad del producto: "))
    #Crear producto
    producto = {
          "Nombre": nombre, 
          "Precio": precio, 
          "Cantidad": cantidad
          }
    db.create_products(producto)
    db.guardar_datos()
    separador()
    print("  PRODUCTO AGREGADO CON EXITO     ")
    separador()
    pausar()

def listar_productos():
    limpiar_pantalla()
    separador()
    print("LISTA DE PRODUCTOS") 
    separador()
    print("   NOMBRE - PRECIO - CANTIDAD")
    if len(db.read_products()) == 0:
        print("No hay productos registrados")
    else:
        for i, producto in enumerate(db.read_products()):
            print(f"{i+1}. {producto['Nombre']} - {producto['Precio']} - {producto['Cantidad']}")
    separador()
    pausar()

def eliminar_producto():
    limpiar_pantalla()
    separador()
    print("ELIMINAR PRODUCTO")
    separador()
    listar_productos()
    separador()
    op = int(input("Ingrese el numero del producto a eliminar: "))
    producto = db.delete_products(op-1)
    db.guardar_datos()
    print(f"El producto {producto['Nombre']} ha sido eliminado")
    pausar() 

def modificar_producto():
    limpiar_pantalla()
    separador()
    print(" MODIFICAR PRODUCTO  ")
    separador()
    listar_productos()
    separador()
    op = int(input("Ingrese el numero del producto a modificar: "))
    indice = op-1
    producto = db.read_products()[indice]
    nombre = input(f"Ingrese el nuevo nombre del producto ({producto['Nombre']}): ")    
    if nombre != "":
        producto['Nombre'] = nombre
    precio = input(f"Ingrese el nuevo precio del producto ({producto['Precio']}): ")
    if precio.strip():
        producto['Precio'] = float(precio)
    cantidad = input(f"Ingrese la nueva cantidad del producto ({producto['Cantidad']}): ")
    if cantidad.strip():
        producto['Cantidad'] = int(cantidad)

    db.update_products(indice, producto)
    db.guardar_datos()
    separador()
    print("  PRODUCTO MODIFICADO CON EXITO")  
    separador() 
    pausar()

def producto():

    os.system("cls")
    while True:
        op = imprimir_menu()
        match op:
            case 1:
                listar_productos()
            case 2:
                agregar_producto()
            case 3:
                modificar_producto()
            case 4:
               eliminar_producto()
            case 5:
                print("Salir")
                break