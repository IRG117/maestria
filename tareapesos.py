def combinaciones_monedas(monto, monedas):
    if monto == 0:
        return [[]]
    combinaciones = []
    for i, moneda in enumerate(monedas):
        if moneda <= monto:
            resto = monto - moneda
            for comb in combinaciones_monedas(resto,monedas[i:]):
                combinaciones.append([moneda] + comb)
    return combinaciones


def imprime_combinaciones(combinaciones):
    for i, comb in enumerate(combinaciones):
        print(f"Combinación {i+1}:")
        dicc = {}
        for moneda in comb:
            dicc[moneda] = dicc.get(moneda, 0) + 1
        for moneda, cantidad in dicc.items():
            print(f"{cantidad} monedas de {moneda} pesos")
        print()


monedas = [50, 20, 10, 5, 1]  # Monedas disponibles
monto = int(input("Ingrese el monto: "))

combinaciones = combinaciones_monedas(monto, monedas)
print(combinaciones)
imprime_combinaciones(combinaciones)