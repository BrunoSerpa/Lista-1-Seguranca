# Faça um programa que leia arquivos de log e filtre apenas os logs de erro (logs de tipo "erro"). O programa deve retornar os logs de erro em um formato fácil de analisar.
from buscaLogs import main as buscaLogs
from escolherLog import main as escolherLog
from re import fullmatch, search, IGNORECASE, match, compile

def extrai_mensagem_adicional(bloco, header_index):
    mensagem = []
    grupo = []
    for linha in bloco[header_index+1:]:
        texto = linha.strip()
        if not texto:
            continue
        if fullmatch(r'[\d\.:]+', texto):
            if grupo:
                mensagem.append(" ".join(grupo))
                grupo = []
            continue
        grupo.append(texto)
    if grupo:
        mensagem.append(" ".join(grupo))
    return mensagem

def processa_bloco(bloco, registros):
    bloco_completo = ''.join(bloco)
    if not search(r'erro', bloco_completo, IGNORECASE):
        return

    header_line = None
    header_index = None
    for i, linha in enumerate(bloco):
        if match(r'^\d{4}-\d{2}-\d{2}\s', linha):
            header_line = linha
            header_index = i
            break
    if not header_line:
        return

    header_regex = compile(
        r'^(\d{4}-\d{2}-\d{2})\s+'
        r'(\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+'
        r'(.*?)'
        r'\[(\d+)\]'
    )
    match = header_regex.search(header_line)
    if not match:
        return
    data, horario, titulo, ip = match.groups()
    ano, mes, dia = data.split('-')
    hora, _ = horario.split('.')
    data_formatada = f"{dia}/{mes}/{ano}"

    mensagem_linhas = extrai_mensagem_adicional(bloco, header_index)
    mensagem_str = "\n".join(mensagem_linhas)
    registros.append((data_formatada, hora, titulo.strip(), ip, mensagem_str))

def processa_log(log):
    registros = []
    try:
        with open(log, 'r', encoding='utf8') as arquivo:
            linhas = arquivo.readlines()

        bloco = []
        for linha in linhas:
            if match(r'^\d{4}-\d{2}-\d{2}\s', linha) and bloco:
                processa_bloco(bloco, registros)
                bloco = []
            bloco.append(linha)
        if bloco:
            processa_bloco(bloco, registros)
    except Exception as e:
        print(f"Erro ao ler o arquivo {log}: {e}")
    return registros

def main(logs=buscaLogs()):
    if not logs:
        print('Nenhum log encontrado.')
        return

    log_escolhido = escolherLog(logs=logs)
    print(f"Processando o log: {log_escolhido}")
    registros = processa_log(log_escolhido)

    if not registros:
        print("Nenhum registro de erro encontrado.")
    else:
        print("Logs de erro encontrados:")
        for i, (data_formatada, hora, titulo, ip, mensagem_str) in enumerate(registros, start=1):
            print(f"{i}º Registro: {titulo} | IP: {ip} (Data: {data_formatada} | Hora: {hora}):")
            if mensagem_str:
                print(mensagem_str)
            print("-" * 40)

if __name__ == "__main__":
    main()