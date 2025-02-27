import os
import db
from utilidades import limpiar_pantalla, separador, pausar

def imprimir_menu():
    limpiar_pantalla()
    separador()
    print ("  MENU DE CLIENTES")
    separador()
    print("1. Listar clientes")
    print("2. Agregar clientes")
    print("3. Modificar clientes")
    print("4. Eliminar clientes")
    print("5.Salir")
    separador()
    opcion = int(input("Ingrese la opcion deseada: "))
    return opcion

def agregar_cliente():
    limpiar_pantalla()
    separador()
    print("AGREGAR CLIENTE")
    separador()
    #Ingresar datos del cliente
    nombre = input("Ingrese el nombre del cliente: ")
    telefono = int(input("Ingrese el telefono del cliente: "))
    edad = int(input("Ingrese la edad del cliente: "))
    #Crear cliente
    cliente = {
          "Nombre": nombre,  
          "Telefono": telefono,
          "Edad": edad
          }
    
    db.create_clients(cliente)
    db.guardar_datos()
    separador()
    print("  CLIENTE AGREGADO CON EXITO")
    separador()
    pausar()

def listar_clientes():  
    limpiar_pantalla()
    separador()
    print("LISTA DE CLIENTES") 
    separador()
    print("   NOMBRE - TELEFONO - EDAD")
    if len(db.read_clients()) == 0:
        print("No hay clientes registrados")
    else:
        for i, cliente in enumerate(db.read_clients()):
            print(f"{i+1}. {cliente['Nombre']} - {cliente['Telefono']} - {cliente['Edad']}")
    separador()
    pausar()

def eliminar_cliente():
    limpiar_pantalla()
    separador()
    print("ELIMINAR CLIENTE")
    separador()
    listar_clientes()
    if len(db.read_clients()) == 0:
        print("No hay clientes registrados")
    else:
        indice = int(input("Ingrese el numero del cliente a eliminar: "))
        clientes = db.delete_clients(indice-1)
        db.guardar_datos()
        print(f"El cliente {clientes['Nombre']} ha sido eliminado")
        print("Cliente eliminado con exito")
    pausar()

def modificar_cliente():
    limpiar_pantalla()
    separador()
    print(" MODIFICAR CLIENTE   ")
    separador()
    listar_clientes()
    op = int(input("Ingrese el numero del cliente a modificar: "))
    indice = op-1
    cliente = db.read_clients()[indice]
    nombre = input(f"Ingrese el nuevo nombre del cliente ({cliente['Nombre']}): ")
    if nombre != "":
        cliente['Nombre'] = nombre
    telefono = input(f"Ingrese el nuevo telefono del cliente ({cliente['Telefono']}): ")
    if telefono != "":
        cliente['Telefono'] = telefono
    edad = input(f"Ingrese la nueva edad del cliente ({cliente['Edad']}): ")
    if edad.strip():
        cliente['Edad'] =int(edad)
    
    db.update_clients(indice, cliente)
    db.guardar_datos()
    separador()
    print(" CLIENTE MODIFICADO CON EXITO ")
    separador()
    pausar()

def cliente():
    os.system("cls")
    while True:
        op = imprimir_menu()
        match op:
            case 1:
                listar_clientes()
            case 2:
                agregar_cliente()
            case 3:
                modificar_cliente()
            case 4:
                eliminar_cliente()
            case 5:
                print("Salir")
                break