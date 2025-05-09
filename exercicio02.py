# Faça um programa que leia arquivos de log e filtre apenas os logs de erro (logs de tipo "erro"). O programa deve retornar os logs de erro em um formato fácil de analisar.
from buscaLogs import main as buscaLogs
from escolherLog import main as escolherLog
from conteudoLog import main as conteudoLog
from re import fullmatch, IGNORECASE, search

def ajustaDescricao(descricoes):
    mensagem = []
    grupo = [] 
    for descricao in descricoes:
        texto = descricao.strip()
        if not texto:
            continue
        # Ignora linhas que são só números, IPs ou timestamps
        if fullmatch(r'[\d\.:]+', texto):
            if grupo:
                mensagem.append(" ".join(grupo))
                grupo = []
            continue
        grupo.append(texto)
    if grupo:
        mensagem.append(" ".join(grupo))
    return mensagem

def contemErro(listaDescricao):
    for item in listaDescricao:
        if search(r'erro', item, IGNORECASE):
            return True
    return False

def main(logs):
    if not logs:
        print('Nenhum log encontrado.')
        return

    registros = conteudoLog(escolherLog(logs))
    if not registros:
        print("Nenhum registro encontrado.")
    else:
        mensagens = []
        for posicao, ((ano, mes, dia), hora, titulo, ip, descricao) in enumerate(registros, start=1):
            if not contemErro(descricao):
                continue
            mensagens.append(f"{posicao}º Registro - {titulo} | IP: {ip} (Data: {dia}/{mes}/{ano} | Hora: {hora}):")
            textoErro = ''
            for erro in ajustaDescricao(descricao):
                textoErro += f'{erro}. '
            mensagens.append(f'Descrição: {textoErro}')
        if not mensagens:
            print("Nenhum registro de erro encontrado.")
            return
        print("Logs de erro encontrados:")
        for mensagem in mensagens:
            print(mensagem)

if __name__ == "__main__":
    main(buscaLogs())