def filtro_duas_listas(lista1, lista2):
    return [x for x in lista1 if x in lista2]

lista1 = [1, 2, 3, 4, 5, 6]
lista2 = [4, 5, 6, 7, 8, 9]

resultado = filtro_duas_listas(lista1, lista2)
print(resultado)
