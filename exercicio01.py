# Faça  um  programa  que  leia  um  arquivo  de  log  e  retorne  os  registros  de  acesso (por exemplo, com data, hora e endereço IP)
from conteudoLog import main as conteudoLog

def main():
    registros = conteudoLog()

    if not registros:
        print("Nenhum registro de acesso encontrado.")
        return
    
    print("Registros de acesso encontrados:")
    for posicao, ((ano, mes, dia), hora, _, ip, _) in enumerate(registros, start=1):
        print(f"{posicao}º Registro (Data: {dia}/{mes}/{ano}, Hora: {hora}, IP: {ip})")

if __name__ == "__main__":
    main()