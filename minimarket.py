from utilidades import separador, limpiar_pantalla, pausar
import os
from productos import producto
from clientes import cliente
from facturacion import factura
lista_productos =[]

while True:
    
    os.system("cls")
    separador()
    print("  🛒 ESPERANZA MINIMARKET    ")
    separador()
    print("1.🏷️   Productos")
    print("2.👤  Clientes")
    print("3.📠  Facturar")
    print("4.📃  Datos del minimarket")
    print("5.🔙  Salir")
    separador()
    op = int(input("Opcion: "))
    
    match op: 
        case 1:
            producto()
        case 2:
            cliente()
        case 3:
           factura()
        case 4:
            print("Datos del minimarket")
            input("Presione para continuar")
        case 5:
            print("Salir")
            print("Gracias por usar el minimarket")
            break