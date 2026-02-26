
# guarda nombre en un archivo 
def guardar_nombres(ruta="nombres.txt",cantidad=5):
    with open(ruta,"w",encoding="utf-8") as f: # funcion open abre el archivo o lo crea si no existe
        # open usa 3 cosas 1 el nombre del archivo, 2 que va a ahcer leer R o esciribir W
        # 3 el encoding que tipo de letras guarda utf8 letras latinas
        for i in range(1,cantidad+1): # for para pedir cada elemento
            nombre = input("Dame un nombre ") # 
            f.write(nombre + "\n")
    print(" SE TERMINARON DE GUARDAR LOS NOMBRES ")

guardar_nombres()