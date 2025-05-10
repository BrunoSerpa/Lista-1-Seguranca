# Faça  um  programa  que  retorne  os  últimos  30  comandos  executados  por  um usuário no sistema.
from os import name
from datetime import datetime

from conteudoLog import main as conteudoLog

def extrairComandos(descricoes):
    if name == "nt":
        for descricao in descricoes:
            if "CommandLine=" in descricao:
                comando = descricao.split("=", 1)[1].strip()
                if comando:
                    return comando

        for descricao in descricoes:
            if "HostApplication=" in descricao:
                comando = descricao.split("=", 1)[1].strip()
                if comando:
                    return comando
    return descricoes[0]

def geraTimestamp(registro):
    try:
        ((ano, mes, dia), hora, _, _, _) = registro
        ts = datetime.strptime(f"{ano}-{mes}-{dia} {hora}", "%Y-%m-%d %H:%M:%S")
        return ts
    except Exception:
        return datetime.min

def main():
    logs = []
    if name == "nt":
        from os import path
        logs.append(path.join(path.dirname(__file__), 'logs', 'Windows PowerShell.log')) #logs/Windows PowerShell.log

    elif name == "posix":
        from pathlib import Path
        logs.append(Path.home() / ".bash_history")
        logs.append(Path.home() / ".zsh_history")

    registros = []
    for log in logs:
        registros.extend(conteudoLog(log))

    if not registros:
        print("Nenhum registro encontrado.")
        return

    registros.sort(key=geraTimestamp, reverse=True)
    mensagens = []
    for posicao, ((ano, mes, dia), hora, titulo, ip, descricao) in enumerate(registros, start=0):
        textoComando = extrairComandos(descricao)
        if not textoComando:
            continue

        numeroRegistro = len(registros) - posicao
        mensagens.append(f"{numeroRegistro}º Registro - {titulo} | IP: {ip} (Data: {dia}/{mes}/{ano} | Hora: {hora}):")
        mensagens.append(f'Comando: {textoComando}')

        if len(mensagens) == 60:
            break

    if not mensagens:
        print("Nenhum comando encontrado.")

    print("Comandos encontrados:")
    for mensagem in mensagens:
        print(mensagem)

if __name__ == "__main__":
    main()