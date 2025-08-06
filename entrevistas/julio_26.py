# Crear un menú con convertidor de unidades
# Usar múltiples funciones dentro de una función menú principal y operaciones matemáticas

def km_milla(km):
    return km * 0.621371

def milla_km(millas):
    return millas * 1.60934

def cel_far(celsius):
    return (celsius * 9/5) + 32  # Puedes completar esta parte

def far_cel(faren):
    return (faren - 32) * 5/9  # Puedes completar esta parte

def kilo_libra(kilos):
    return kilos * 2.20462  # Puedes completar esta parte

def libra_kilo(libra):
    return libra / 2.20462  # Puedes completar esta parte

while True: 
    print("\n--- Conversor de Unidades ---")
    print("1. Distancia (km a millas)")
    print("2. Distancia (millas a km)")
    print("3. Temperatura (°C a °F)")
    print("4. Temperatura (°F a °C)")
    print("5. Peso (lb a kg)")
    print("6. Peso (kg a lb)")
    print("7. Salir")
    
    opcion_usuario = input("Selecciona una opción: ")

    if opcion_usuario == "1":
        kilometros = float(input("Dame kilómetros: "))
        resultado = km_milla(kilometros)
        print("En millas son:", round(resultado, 2))

    elif opcion_usuario == "2":
        millas = float(input("Dame millas: "))
        resultado = milla_km(millas)
        print("En kilómetros son:", round(resultado, 2))

    elif opcion_usuario == "7":
        print("Adiós")
        break

    else:
        print("Opción no válida o aún no implementada.")
