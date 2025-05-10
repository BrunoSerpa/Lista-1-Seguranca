# Faça um programa que leia arquivos de log e filtre apenas os logs de erro (logs de tipo "erro"). O programa deve retornar os logs de erro em um formato fácil de analisar.
from re import fullmatch, IGNORECASE, search

from conteudoLog import main as conteudoLog

def ajustaDescricao(descricoes):
    if len(descricoes)<=1:
        return descricoes[0]
    
    mensagem = ""
    for descricao in descricoes:
        texto = descricao.strip()
        
        # Ignora linhas vazias e que são só números, IPs ou timestamps
        if not texto or fullmatch(r'^\d+$|^\d{1,3}(\.\d{1,3}){3}$|^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?$', texto):
            continue

        mensagem += f'{descricao}. '
    return mensagem

def contemErro(descricoes):
    for descricao in descricoes:
        if search(r'erro', descricao, IGNORECASE):
            return True
    return False

def main(registro = None):
    if not registro:
        registros = conteudoLog()

    if not registros:
        print("Nenhum registro encontrado.")
        return
    
    mensagens = []
    for posicao, ((ano, mes, dia), hora, titulo, ip, descricao) in enumerate(registros, start=1):
        if not contemErro(descricao):
            continue
        mensagens.append(f"{posicao}º Registro - {titulo} | IP: {ip} (Data: {dia}/{mes}/{ano} | Hora: {hora}):")
        mensagens.append(f'Descrição: {ajustaDescricao(descricao)}')

    if not mensagens:
        print("Nenhum registro de erro encontrado.")
        return

    print("Logs de erro encontrados:")
    for mensagem in mensagens:
        print(mensagem)

if __name__ == "__main__":
    main()