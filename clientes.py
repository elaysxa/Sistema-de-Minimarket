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

def obtener_nuevo_id():
    clientes = db.read_clients()
    if not clientes:
        return 1
    return max(cliente.get("Id", 0) for cliente in clientes) + 1
   
def agregar_cliente():
    limpiar_pantalla()
    separador()
    print("AGREGAR CLIENTE")
    separador()
    #Ingresar datos del cliente
    nombre = input("Ingrese el nombre del cliente: ")
    telefono = int(input("Ingrese el telefono del cliente: "))
    edad = int(input("Ingrese la edad del cliente: "))
    id = obtener_nuevo_id()
    #Crear cliente
    cliente = {
          "Id": id,
          "Nombre": nombre,  
          "Telefono": telefono,
          "Edad": edad,
          "Documento":id
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
    print("Lista de clientes")
    separador()
    print("ID - NOMBRE - EDAD - TELEFONO")
    clientes = db.read_clients()
    if not clientes:
        print("No hay clientes registrados")
    else:
        for cliente in clientes:
            print(
                f"{cliente['Id']} - {cliente['Nombre']} - {cliente['Edad']} - {cliente['Telefono']}"
                )
    separador()
    pausar()


def buscar_indice_por_id(cli_id):
    clientes = db.read_clients()
    for index, cliente in enumerate(clientes):
        if cliente.get("Id") == cli_id:
            return index
    return None

def eliminar_cliente():
    listar_clientes()
    try:
        cli_id = int(input("Ingrese el ID del cliente a eliminar: "))
        indice = buscar_indice_por_id(cli_id)
        if indice is None:
            print("Cliente no encontrado.")
        else:
            cliente = db.delete_clients(indice)
            print(f"El cliente {cliente['Nombre']} ha sido eliminado")
    except ValueError:
        print("Entrada no válida.")
    pausar()

def modificar_cliente():
    listar_clientes()
    try:
        cli_id = int(input("Ingrese el ID del cliente a modificar: "))
        indice = buscar_indice_por_id(cli_id)
        if indice is None:
            print("Cliente no encontrado.")
            pausar()
            return
        cliente = db.read_clients()[indice]
    except ValueError:
        print("Entrada no válida")
        pausar()
        return

    nombre = input(f"Nombre del cliente ({cliente['Nombre']}): ")
    if nombre != "":
        cliente["Nombre"] = nombre
    edad = input(f"Edad del cliente ({cliente['Edad']}): ")
    if edad != "":
        cliente["Edad"] = edad
    telefono = input(f"Telefono del cliente ({cliente['Telefono']}): ")
    if telefono != "":
        cliente["Telefono"] = telefono
    db.update_clients(indice, cliente)
    print("Cliente modificado con éxito")
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