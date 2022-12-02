lista = list(range(1, 100))
resposta = 1
while resposta != 's':
    resposta = int(input())
    if resposta < 7:
        print(lista[0:10])
    else:
        index = lista.index(resposta)
        print(lista[index - 5:index + 5])
