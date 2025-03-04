import os
import db
from utilidades import limpiar_pantalla, separador, pausar
#Menu de facturacion
def facturar():
    limpiar_pantalla()
    separador()
    print("         📠  FACTURACION ")
    separador()
    #Elegir un cliente
    clientes = db.read_clients()
    if not clientes:
        print(" ❌  No hay clientes registrados.")
        pausar()
        return
    print("📃 Lista de Clientes")
    separador()
    for cli in clientes:
        print(f"{cli['Id']:<6} {cli['Nombre']}")
    try:
        separador()
        cliente_id = int(input("Ingrese el ID del cliente: "))
    except ValueError:
        print("⚠️ Entrada no válida.")
        pausar()
        return
    if not any(cli["Id"] == cliente_id for cli in clientes):
        print("❌ Cliente no encontrado.")
        pausar()
        return

    producto = db.read_products()
    limpiar_pantalla()
    if not producto:
        print(' ❌ No hay productos disponibles')
        pausar()
        return
    separador()
    print(' 🧾 Productos disponibles')
    separador()
    print(f"{'NO':<4}{'NOMBRE':<15}{'PRECIO ':>15}")
    separador()

    for i, productos in enumerate(producto):
        print(f"{i+1:<4} {productos['Nombre']:<15}{productos['Precio']:>13,.0f}")
        
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
                print(' ⚠️ Producto invalido')
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
            print(' ⚠️ Entrada no valida.')
            pausar()
    if not items:
        print(' ⚠️ No se agregaron productos a la factura ')
        pausar()
        return
    limpiar_pantalla()
    separador()
    print("     🧾 FACTURA GENERADA  ")
    separador()
    print(f" {'Nombre':<15}{'Cantidad':>8}  {'Precio':<10} {'Subtotal':>8}")
    separador()
    for item in items:
        print(f"{item['Nombre']:<16}{item['Cantidad']:>8}  {item['Precio']:<10,.0f}{item['Subtotal']:>8,.0f}")
    separador()
    print(f"{'Total: ':>35}{total:,.0f}")
    separador()
    factura = {"Cliente": cliente_id, "Items": items, "Total": total}
    db.create_facturas(factura)
    db.guardar_datos()
    print('  ✅ FACTURA GENERADA CON EXITO  ')
    separador()
    pausar()

def listar_factura():
    limpiar_pantalla()
    separador()
    print('  📃 LISTA DE FACTURAS  ' )
    separador()
    print(f"{'ID':<4}{'CLIENTE':<18}{'TOTAL ':>10}")
    separador()
    facturas = db.read_facturas()
    clientes = db.read_clients()
    if not facturas:
        print(" ❌ No hay facturas registradas.")
    else:
        for i, fac in enumerate(facturas):
            cliente_nombre = next(
                (cli["Nombre"] for cli in clientes if cli["Id"] == fac["Cliente"]),
                "Desconocido",
            )
            print(f"{i+1:<4} {cliente_nombre:<18} {fac['Total']:>10,.2F}")
    separador()
    pausar()

def eliminar_factura():
    limpiar_pantalla()
    separador()
    print(' 🗑️ ELIMINAR FACTURA')
    separador()
    listar_factura()
    op = int(input('Ingrese el numero de la factura a eliminar: '))
    factura = db.delete_facturas(op-1)
    db.guardar_datos()
    separador()
    print(f" ✅ La factura de {factura['Cliente']} ha sido eliminado")
    separador()
    pausar()

def modificar_factura():
    listar_factura()
    try:
        index_factura = int(input("Ingrese el número de la factura a editar: ")) - 1
        factura_actual = db.read_facturas()[index_factura]
    except (ValueError, IndexError):
        print("Opción inválida.")
        pausar()
        return
    limpiar_pantalla()
    separador()
    print("🔁   MODIFICAR FACTURA ")
    separador()
    nuevo_cliente = input(f"Nombre del cliente ({factura_actual['Cliente']}): ")
    if nuevo_cliente != "":
        factura_actual["Cliente"] = nuevo_cliente

    # Iniciar con los items actuales
    items = factura_actual.get("Items", [])
    while True:
        
        limpiar_pantalla()
        separador()
        print("FACTURA ACTUAL  ")
        separador()
        print(f" {'NO':<4} {'Nombre':<15}{'Cantidad':>8}  {'Precio':<10} {'Subtotal':>8}")
        separador()
        if items:
            for idx, item in enumerate(items):
                print(f"{idx+1:<4}{item['Nombre']:<16}{item['Cantidad']:>8}  {item['Precio']:<10,.0f}{item['Subtotal']:>8,.0f}")
            separador()
            print(f"{'Total: ':>35}{sum(item['Subtotal'] for item in items):,.0f}")
        else:
            print(" ❌ No hay items en la factura.")
        separador()
        print("Opciones:")
        separador()
        print("1. Modificar un item existente")
        print("2. Eliminar un item existente")
        print("3. Agregar nuevo item")
        print("4. Terminar edición")
        separador()
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            continue

        if opcion == 1:
            try:
                num = int(input("Número del item a modificar: ")) - 1
                if num < 0 or num >= len(items):
                    print(" ⚠️ Índice inválido.")
                    pausar()
                else:
                    nueva_cantidad = input(
                        f"Cantidad actual ({items[num]['Cantidad']}): "
                    )
                    if nueva_cantidad != "":
                        nueva_cantidad = int(nueva_cantidad)
                        items[num]["Cantidad"] = nueva_cantidad
                        items[num]["Subtotal"] = nueva_cantidad * items[num]["Precio"]
                        print('✅ Item modificado ')
            except ValueError:
                print(" ⚠️ Entrada no válida.")
                pausar()
        elif opcion == 2:
            try:
                num = int(input("Número del item a eliminar: ")) - 1
                if num < 0 or num >= len(items):
                    print(" ⚠️ Índice inválido.")
                    pausar()
                else:
                    eliminado = items.pop(num)
                    print(f" 🗑️ Se eliminó el item: {eliminado['Nombre']}")
                    pausar()
            except ValueError:
                print(" ❌ Entrada no válida.")
                pausar()
        elif opcion == 3:
            total = factura_actual['Total']
            productos = db.read_products()
            if not productos:
                print("No hay productos disponibles.")
                pausar()
            else:
                separador()
                print(' 🧾 Productos disponibles')
                separador()
                print(f"{'NO':<4}{'NOMBRE':<15}{'PRECIO ':>15}")
                separador()

                for i, prod in enumerate(productos):
                    print(f"{i+1:<4} {prod['Nombre']:<15}{prod['Precio']:>13,.0f}")
                separador()
                try:
                    op_prod = int(input("Seleccione producto por número: ")) - 1
                    if op_prod < 0 or op_prod >= len(productos):
                        print(" ❌ Producto inválido.")
                        pausar()
                        continue
                    cantidad = int(input("Cantidad: "))
                    precio = productos[op_prod]["Precio"]
                    subtotal = precio * cantidad
                    items.append(
                        {
                            "Nombre": productos[op_prod]["Nombre"],
                            "Precio": precio,
                            "Cantidad": cantidad,
                            "Subtotal": subtotal
                        }         
                        )
                    
                except ValueError:
                    print(" ⚠️ Entrada no válida.")
                    pausar()
        elif opcion == 4:
            break

    total = sum(item["Subtotal"] for item in items)
    factura_actual["Items"] = items
    factura_actual["Total"] = total
    db.update_facturas(index_factura, factura_actual)
    db.guardar_datos()
    separador()
    print(" ✅ Factura editada con éxito.")
    separador()
    pausar()
    
def imprimir_menu():
    os.system("cls")
    separador()
    print (" 📠 Menú de facturacion")
    separador()
    print("1.🧾  Facturar")
    print("2.🗑️   Eliminar factura")
    print("3.🔁  Modificar factura")
    print("4.🧾  Listar factura")
    print("5.🔙  Salir")
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

               