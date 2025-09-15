#recibe cadena si es contra 3 intenntos
contra= "gatito123"
def login(password):
    if password == contra:
        return "Bienvenido"
    else:
        return "Estas bien tonoto"
    
intentos=0
while intentos < 3:
    usuario_dice = input(("Dame tu contrasena"))
    resultado = login(usuario_dice)
    if resultado == "Bienvenido":
        print(resultado)
        break
    else:
        print(resultado)
        intentos = intentos+1

if intentos == 3:
    print("Has agotado tus intentos. Acceso bloqueado.")