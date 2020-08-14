#Imports necesarios para la generación del shell y la interpretación de comandos
import click
from click_shell import shell
'''
Clase para guardar la información de cada cliente
'''
class Cliente:
    Nombre = ""
    Direccion = ""
    Telefono = ""
    def __init__(self,name,add,phone):
        self.Nombre = name
        self.Direccion = add
        self.Telefono = phone

ListaClientes = {}          #Diccionario para guardar los datos de los clientes

'''
Función para imprimir todos los datos de un cliente,
recibe como parámetro el id a imprimir
'''
def imprimir(id):
    print("Valores del id "+str(id)+":")
    print("Nombre: "+ListaClientes[id].Nombre)
    print("Dirección: "+ListaClientes[id].Direccion)
    print("Telefono: "+ListaClientes[id].Telefono)

#Definición del punto de entrada e inicio del shell
@shell(prompt='my-client-app > ', intro='Starting client app...')
def cli():
    pass
#Comando para crear clientes, debe recibir todos los datos y se valida el tamaño del teléfono
@cli.command()
@click.option('--id',       default = 0,    help='Identificador del cliente')
@click.option('--nombre',   default = "",   help='Nombre del cliente')
@click.option('--direccion',default = "",   help='Dirección del cliente')
@click.option('--telefono', default = "",   help='Telefono del cliente')
def create(id,nombre,direccion,telefono):
    if id == 0 or nombre == "" or direccion == "" or telefono == "":
        print("Please specify a value for all the client values, use 'help create' for more info")
    else:
        if not(len(telefono) == 10):
            print("Please use ten digits for the phone")
        else:
            if id in ListaClientes.keys():
                print("Allready exist, try with the 'update' command")
            else:
                ListaClientes[id] = Cliente(nombre, direccion ,telefono)
                print("Client created...")
        
#Comando para mostrar clientes, debe recibir un id válido, o ningúno para mostrar todos los que hay
@cli.command()
@click.argument('id', default=0)
def show(id):
    if len(ListaClientes) == 0:
        print("There are no clients yet")
    else:
        if id not in ListaClientes.keys():
            if id == 0:
                for client in ListaClientes.keys():
                    imprimir(client)
                    print("")
            else:
                print("The client does not exist, try the 'create' command")
        else:
            imprimir(id)

#Comando para actualizar valores, debe recibir un id válido, y los valores que se desean cambiar
@cli.command()
@click.argument('id', default=0)
@click.option('--nombre', default = "", help='Nombre nuevo del cliente')
@click.option('--direccion',default = "", help='Dirección nueva del cliente')
@click.option('--telefono', default="", help='Telefono nuevo del cliente')
def update(id,nombre,direccion,telefono):
    if id not in ListaClientes.keys():
        print("The client does not exist, try the 'create' command")
    else:
        if id == 0 and nombre == "" and direccion == "" and telefono == "":
            print("Please insert a value to change")
        else:
            if(nombre == ""):
                nombre = ListaClientes[id].Nombre
            if(direccion == ""):
                direccion = ListaClientes[id].Direccion
            if(telefono == ""):
                telefono = ListaClientes[id].Telefono
            ListaClientes[id] = Cliente(nombre, direccion ,telefono)
            print("The values have changed...")
        
#Comando para borrar un cliente, debe recibir un id válido
@cli.command()
@click.argument('id', default=0)
def delete(id):
    if id not in ListaClientes.keys():
        print("The client does not exist, try the 'create' command")
    else:
        del ListaClientes[id]
        print("client deleted...")

#Comando para guardar los datos actuales en un archivo, se puede ingresar el nombre del archivo
@cli.command()
@click.option('--arch', default = "clientInfo.txt", help='Nombre del archivo')
def save(arch):
    file = open(str(arch), "w")
    for id in ListaClientes.keys():
        file.write(str(id)+","+ListaClientes[id].Nombre+","+ListaClientes[id].Direccion+","+ListaClientes[id].Telefono+"\n")
    print("Data saved to file...")

#Comando para obtener datos de un archivo, se puede ingresar el nombre del archivo
@cli.command()
@click.option('--arch', default = "clientInfo.txt", help='Nombre del archivo')
def load(arch):
    ListaClientes.clear()
    file = open(str(arch), "r")
    for line in file:
        values = line.split(",")
        ListaClientes[int(values[0])] = Cliente(values[1],values[2],values[3][:-1])
    print("Data loaded from file...")

#Start Point
if __name__ == '__main__':
    cli()