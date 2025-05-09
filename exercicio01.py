# Faça  um  programa  que  leia  um  arquivo  de  log  e  retorne  os  registros  de  acesso (por exemplo, com data, hora e endereço IP)
from buscaLogs import main as buscaLogs
from escolherLog import main as escolherLog
from re import search

def processa_log(log):
    registros = []
    try:
        with open(log, 'r', encoding='utf8') as arquivo:
            for linha in arquivo:
                if linha.strip():
                    data = search(r'\d{4}-\d{2}-\d{2}', linha)
                    hora = search(r'\d{2}:\d{2}:\d{2}', linha)
                    ip = search(r'\[(\d+)\]', linha)
                    if data and hora and ip:
                        registros.append((data.group(), hora.group(), ip.group()))
    except Exception as e:
        print(f"Erro ao ler o arquivo {log}: {e}")
    return registros

def main(logs = buscaLogs()):
    if not logs:
        print('Nenhum log encontrado.')
        return
    logEscolhido = escolherLog(logs=logs)
    print(f"Processando o log: {logEscolhido}")
    registros = processa_log(logEscolhido)
    if not registros:
        print("Nenhum registro de acesso encontrado.")
    else:
        print("Registros de acesso encontrados:")
        for posicao, (data, hora, ip) in enumerate(registros, start=1):
            ano, mes, dia = data.split('-')
            print(f"{posicao}º Registro (Data: {dia}/{mes}/{data[0:4]}, Hora: {hora}, IP: {ip[1:-1]})")

if __name__ == "__main__":
    main()