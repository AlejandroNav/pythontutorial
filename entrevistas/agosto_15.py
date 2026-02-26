password_real = "gatito123"

while True:
    intento = input("Introduce la contraseña: ")
    
    if intento == password_real:
        print("¡Contraseña correcta!")
        break
    else:
        coincidencias = 0
        pista=''
        for i in range(min(len(intento), len(password_real))):
            if intento[i] == password_real[i]:
                coincidencias += 1
                pista += intento[i]
            else:
                pista += '*'
        print(f"Contraseña incorrecta. Coincidencias: {coincidencias}. Pista: {pista}")  1q
        