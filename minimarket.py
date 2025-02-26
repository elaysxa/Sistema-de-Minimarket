import os
lista_productos =[]

while True:
    
    os.system("cls")
    print("Esperanza minimarket")
    print("1. Productos")
    print("2. Clientes")
    print("3. Facturar")
    print("4. Datos del minimarket")
    print("5. Salir")
    
    print("Seleccione una opcion")
    op = int(input("Opcion: "))
    
    match op: 
        case 1:
            print('Productos')
        case 2:
            print('Clientes')
        case 3:
           print('Facturar')
        case 4:
            print("Datos del minimarket")
            input("Presione para continuar")
        case 5:
            print("Salir")
            print("Gracias por usar el minimarket")
            break