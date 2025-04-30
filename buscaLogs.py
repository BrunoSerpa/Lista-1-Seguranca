from os import name, path, walk

def verificaSistema():
    sistema = name
    if sistema == 'nt':
        print('O sistema é Windows')
        return r'C:\Windows\Logs', sistema
    elif sistema == 'posix':
        print('O sistema é Linux')
        return '/var/log/', sistema
    else:
        print('Sistema não identificado')
        return None, None

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
    dir_logs, sistema = verificaSistema()
    if dir_logs is None:
        return [], None
    return verificaDiretorio(dir_logs), sistema

if __name__ == "__main__":
    logs = main()
    for i, log in enumerate(logs, start=1):
        print(f'{i}º log: {path.basename(log)}')