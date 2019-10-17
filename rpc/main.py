import sys
from campo_minado_servidor import server
from campo_minado_client import client

print("Você quer executar:")
print("1 para servidor")
print("2 para cliente")
opcao = input("Opção:")

try:
    if int(opcao) == 1:
        print("Servidor ativado:\n")
        server()
    elif int(opcao) == 2:
        print("Cliente ativado:\n")
        client()

except : # pega todas possíveis
    for val in sys.exc_info():
        print(val)

input()
