import json

db = {
    "Clientes": [],
    "Producto": [],
    "Facturas": []
}

#CRUD for clients
def create_products(product):
    db['Producto'].append(product)

def read_products():
    return db["Producto"]

def update_products(index, product):
    db["Producto"][index] = product

def delete_products(index):
    return db["Producto"].pop(index)

# Guardar datos en un archivo json
def guardar_datos():
    with open("data/db.json", "w") as archivo:
        json.dump(db, archivo, indent=4)

def cargar_datos():
    global db
    try:
        with open("data/db.json") as archivo:
            db = json.load(archivo)
    except FileNotFoundError:
        # Crear un archivo vacío si no existe
        guardar_datos()

cargar_datos()