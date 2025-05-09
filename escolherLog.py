from os import path
from buscaLogs import main as buscaLogs

def main(logs):
    if not logs:
        logs = buscaLogs()
    print("Logs encontrados:")
    for i, log_file in enumerate(logs, start=1):
        print(f"{i}º - {path.basename(log_file)}")
    
    while True:
        try:
            escolha = int(input("Escolha o número do log que desejado: "))
            if escolha < 1 or escolha > len(logs):
                print("Número inválido. Tente novamente.")
            return logs[escolha - 1]
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

if __name__ == "__main__":
    log_escolhido = main()
    if log_escolhido:
        print(f"Você escolheu o log: {log_escolhido}")