def CodificaDNI(dni):
    if len(dni) != 8 or not dni.isdigit():
        return "Error: El DNI debe tener exactamente 8 dígitos"
    bloque = int(dni) % 23
    
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"

    letra_bloque = letras[bloque]
    
    return dni + letra_bloque

def CompruebaDNI(dni_codificado):
    if len(dni_codificado) != 9:
        return "Error: El código de bloque debe tener 9 caracteres"

    dni_numero = dni_codificado[:-1]
    dni_letra = dni_codificado[-1]

    if not dni_numero.isdigit() or len(dni_numero) != 8:
        return "Error: El número de DNI en el código de bloque no es válido"

    dni_codificado_calculado = CodificaDNI(dni_numero)

    if dni_codificado_calculado == dni_codificado:
        return "DNI es válido"
    else:
        return "DNI no es válido"



# Ejemplos de uso:
#Ejemplo 1:
dni_codificado_valido = "12345678Z"
resultado_valido = CompruebaDNI(dni_codificado_valido)
print("El DNI es ", dni_codificado_valido, " y el resultado es: ", resultado_valido)

#Ejemplo 2:
dni_codificado_no_valido = "49275390Z"
resultado_no_valido = CompruebaDNI(dni_codificado_no_valido)
print("El DNI es ", dni_codificado_no_valido, " y el resultado es: ", resultado_no_valido)

def CodificaTarjeta(numero_tarjeta):
    if len(numero_tarjeta) != 15 or not numero_tarjeta.isdigit():
        return "Error: El número de tarjeta debe tener exactamente 15 dígitos"

    digitos = list(map(int, numero_tarjeta))

    # Paso 1: Multiplicar por dos los dígitos en posiciones impares
    for i in range(0, 16, 2):
        digitos[i] *= 2

        # Paso 2: Si el resultado excede 10, sumar sus dígitos y sustituir
        if digitos[i] > 9:
            digitos[i] = digitos[i] // 10 + digitos[i] % 10

    # Paso 3: Sumar el resultado a todos los dígitos en posiciones pares
    suma_total = sum(digitos)

    # Paso 4: Calcular el módulo 10 del resultado
    modulo_10 = suma_total % 10

    # Paso 5: Calcular x=10-M
    x = (10 - modulo_10) % 10
    
    numero_tarjeta = list(map(int, numero_tarjeta))

    numero_tarjeta.append(x)

    codigo_bloque = ''.join(map(str, numero_tarjeta))

    return codigo_bloque


def CompruebaTarjeta(codigo_bloque):
    if len(codigo_bloque) != 16 :
        return "Error: El código de bloque debe tener exactamente 16 dígitos"

    codigo_bloque_calculado = CodificaTarjeta(codigo_bloque[:-1])

    if codigo_bloque_calculado == codigo_bloque:
        return "La tarjeta es válida"
    else:
        return "La tarjeta no es válida"


# Ejemplo de uso
#Ejemplo 1:
numero_tarjeta_valida = "545762389823411"
codigo_bloque_valido = CodificaTarjeta(numero_tarjeta_valida)
print("El numero de tarjeta es ", numero_tarjeta_valida, " y el resultado es: ", codigo_bloque_valido)

#Ejemplo 2:
numero_tarjeta_no_valida ="5457623898234113"
codigo_bloque_no_valido = CompruebaTarjeta(numero_tarjeta_no_valida)
print("El numero de tarjeta es ", numero_tarjeta_no_valida, " y el resultado es: ", codigo_bloque_no_valido)