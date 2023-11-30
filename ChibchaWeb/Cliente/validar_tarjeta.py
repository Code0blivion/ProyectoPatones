def validar_tarjeta(numero): #algoritmo de luh para validar numeros de tarjetas de credito
    numero = numero[::-1]  # Invertir el número
    total = 0
    for i in range(len(numero)):
        digito = int(numero[i])

        # Duplicar cada segundo dígito
        if i % 2 == 1:
            digito *= 2

        # Si el número es mayor que 9, restar 9
        if digito > 9:
            digito -= 9

        total += digito

    # El número de tarjeta es válido si es divisible por 10
    return total % 10 == 0 and not str(numero).count('0') == 16 #devuelve un booleano