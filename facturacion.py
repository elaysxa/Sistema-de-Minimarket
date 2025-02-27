import os
import db
from utilidades import limpiar_pantalla, separador, pausar
#Menu de facturacion
def facturar():
    limpiar_pantalla()
    separador()
    print("Facturacion")
    separador()
    #Elegir un cliente
    clientes = db.read_clients()
    if not clientes:
        print("No hay clientes registrados.")
        pausar()
        return
    print("Lista de Clientes")
    for cli in clientes:
        print(f"{cli['Id']} - {cli['Nombre']}")
    try:
        cliente_id = int(input("Ingrese el ID del cliente: "))
    except ValueError:
        print("Entrada no válida.")
        pausar()
        return
    if not any(cli["Id"] == cliente_id for cli in clientes):
        print("Cliente no encontrado.")
        pausar()
        return

    producto = db.read_products()
    limpiar_pantalla()
    if not producto:
        print('No hay productos disponibles')
        pausar()
        return
    separador()
    print('Productos disponibles')
    separador()

    for i, prod in enumerate(producto):
        print(f"{i + 1}. {prod['Nombre']} - Precio: {prod['Precio']}")
        
    items = []
    total = 0.0
    while True:
        separador()
        op = input('Seleccione producto por numero o escriba "fin" para terminar: ')
        if op.lower() == 'fin':
            break
        try:
            indice =int (op)-1
            if indice < 0 or indice >= len(producto):
                print('Producto invalido')
                pausar()
                continue
            cantidad = int(input('Cantidad: '))
            precio = producto[indice]['Precio']
            subtotal = precio * cantidad
            items.append(
                {
                    'Nombre': producto[indice]['Nombre'],
                    'Precio': precio,
                    'Cantidad': cantidad,
                    'Subtotal': subtotal
                }
            )
            total += subtotal
        except ValueError:
            print('Entrada no valida.')
            pausar()
    if not items:
        print('No se agregaron productos a la factura ')
        pausar()
        return
    limpiar_pantalla()
    separador()
    print(" Factura generada: ")
    separador()
    for item in items:
        print(f"{item['Nombre']} x {item['Cantidad']} = {item['Subtotal']}")
    print(f"Total: {total}")
    separador()
    factura = {"Cliente": cliente_id, "Items": items, "Total": total}
    db.create_facturas(factura)
    db.guardar_datos()
    separador()
    print('  FACTURA GENERADA CON EXITO  ')
    separador()
    pausar()

def listar_factura():
    limpiar_pantalla()
    separador()
    print('  LISTA DE FACTURAS  ' )
    separador()
   
    facturas = db.read_facturas()
    clientes = db.read_clients()
    if not facturas:
        print("No hay facturas registradas.")
    else:
        for i, fac in enumerate(facturas):
            cliente_nombre = next(
                (cli["Nombre"] for cli in clientes if cli["Id"] == fac["Cliente"]),
                "Desconocido",
            )
            print(f"{i+1}. Cliente: {cliente_nombre} - Total: {fac['Total']}")
    pausar()


def eliminar_factura():
    limpiar_pantalla()
    separador()
    print('ELIMINAR FACTURA')
    separador()
    listar_factura()
    op = int(input('Ingrese el numero de la factura a eliminar: '))
    factura = db.delete_facturas(op-1)
    db.guardar_datos()
    separador()
    print(f"La factura de {factura['Cliente']} ha sido eliminado")
    separador()
    pausar()

def modificar_factura():
    limpiar_pantalla()
    separador()
    print('MODIFICAR FACTURA')
    separador()
    listar_factura()
    op = int(input('Ingrese el numero de la factura a modificar: '))
    factura = db.read_facturas()[op-1]
    separador()
    print(f"Factura seleccionada: {factura['Cliente']}")
    separador()
    print('Producto -  Cantidad - Precio')
    separador()
    for i, item in enumerate(factura['Items']):
        print(f"{i+1}. {item['Nombre']}   {item['Cantidad']} x {item['Precio']} = {item['Subtotal']}")
    
    separador()
    item_op = int(input('Ingrese el numero del producto a modificar: '))
    item = factura['Items'][item_op-1]
    separador()
    nueva_cantidad = int(input(f"Ingrese la nueva cantidad para {item['Nombre']}: "))
    item['Cantidad'] = nueva_cantidad
    item['Subtotal'] = item['Precio'] * nueva_cantidad
    
    factura['Total'] = sum(item['Subtotal'] for item in factura['Items'])
    
    db.update_facturas(op-1, factura)
    db.guardar_datos()
    
    print('Factura modificada con exito')
    pausar()
    
def imprimir_menu():
    os.system("cls")
    separador()
    print ("Menú de facturacion")
    separador()
    print("1. Facturar")
    print("2. Eliminar factura")
    print("3. Modificar factura")
    print("4. Listar factura")
    print("5. Salir")
    separador()
    op = int(input("Ingrese la opcion deseada: "))
    return op

def factura():

    os.system("cls")
    while True:

        op = imprimir_menu()

        match op:
            case 1:
                facturar()
            case 2:
                eliminar_factura()
            case 3:
                modificar_factura()
            case 4:
                listar_factura()
            case 5:
                print('Salir')
                break

               