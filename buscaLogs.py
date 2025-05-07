from os import name, path, walk
from pyuac import isUserAdmin, runAsAdmin

from transformarLogs import main as transformaLogs
from tentarNovamente import main as tentarNovamente

def verificaSistema():
    sistema = name
    if sistema == 'nt':
        if isUserAdmin():
            transformaLogs()
        else:
            print('O sistema é Windows')
            if tentarNovamente('Deseja converter os logs atuais do Windows'):
                runAsAdmin()
        return path.abspath(path.join(path.dirname(__file__), "logs"))
    elif sistema == 'posix':
        print('O sistema é Linux')
        return '/var/log/'
    else:
        print('Sistema não identificado')
        return None

def verificaDiretorio(diretorio):
    if not path.exists(diretorio):
        print(f'O diretório {diretorio} não existe')
        return []

    if not path.isdir(diretorio):
        print(f'O caminho {diretorio} não é um diretório')
        return []

    logs = [
        path.join(root, file)
        for root, _, files in walk(diretorio)
        for file in files
        if file.lower().endswith('.log')
    ]

    if not logs:
        print(f'⚠️ Nenhum arquivo .log encontrado em {diretorio}')

    return logs

def main():
    dir_logs = verificaSistema()
    if dir_logs is None:
        return []
    return verificaDiretorio(dir_logs)

if __name__ == "__main__":
    logs = main()
    for i, log in enumerate(logs, start=1):
        print(f'{i}º log: {path.basename(log)}')