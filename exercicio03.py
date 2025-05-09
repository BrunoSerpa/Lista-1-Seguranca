# Faça  um  programa  que  retorne  os  últimos  30  comandos  executados  por  um usuário no sistema.
from conteudoLog import main as conteudoLog
from os import name

def extrair_comandos(descricoes, maquina):
    if maquina == "posix":
        return descricoes[0]
    for descricao in descricoes:
        if "CommandLine=" in descricao:
            comando = descricao.split("=", 1)[1].strip()
            if comando:
                return comando
        if "HostApplication=" in descricao:
            comando = descricao.split("=", 1)[1].strip()
            if comando and not comando.lower().endswith("powershell.exe"):
                return comando

    return None

def main(maquina = None):
    if not maquina:
        maquina = name
    logs = []
    if maquina == "nt":
        from os import path
        logs.append(path.join(path.dirname(__file__), 'logs', 'Windows PowerShell.log'))
    elif maquina == "posix":
        from pathlib import Path
        logs.append(Path.home() / ".bash_history")
        logs.append(Path.home() / ".zsh_history")

    registros = []
    for log in logs:
        registros = [*reversed(conteudoLog(log))]
    if not registros:
        print("Nenhum registro encontrado.")
        return
    mensagens = []
    for posicao, ((ano, mes, dia), hora, titulo, ip, descricao) in enumerate(registros, start=1):
        textoComando = extrair_comandos(descricao, maquina)
        if textoComando:
            mensagens.append(f"{len(registros) - posicao + 1}º Registro - {titulo} | IP: {ip} (Data: {dia}/{mes}/{ano} | Hora: {hora}):")
            mensagens.append(f'Comando: {textoComando}')
        if len(mensagens) == 60:
            break
    if not mensagens:
        print("Nenhum comando encontrado.")
    for mensagem in mensagens:
        print(mensagem)

if __name__ == "__main__":
    main()