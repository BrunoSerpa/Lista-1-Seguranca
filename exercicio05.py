# Faça  um  programa  que  registre  eventos  de  auditoria,  como  quando  um  usuário acessa  ou  altera  um  recurso.  Cada  evento  deve  ser  salvo  em  um  arquivo  com informações como: data, hora, nome do usuário, ação realizada, etc.
from conteudoLog import main as conteudoLog
from os import name
from os import path

def extraiUsuario(descricao, maquina):
    if maquina == 'posix':
        return
    for parte in descricao:
        if "MicrosoftAccount:user=" in parte:
            return parte.split("=", 1)[1].split()[0]
    return "desconhecido"

def main(maquina=None):
    if not maquina:
        maquina = name

    logs = []
    if maquina == "nt":
        logs.append(path.join(path.dirname(__file__), 'logs', 'Security.log'))
    elif maquina == "posix":
        # Linux (comum: auditoria via journald ou histórico de comandos)
        # logs.append("/var/log/auth.log")  # Debian/Ubuntu
        # logs.append("/var/log/audit/audit.log")  # RedHat/CentOS/Fedora com auditd
        # logs.append(Path.home() / ".bash_history")  # Histórico do bash
        # logs.append(Path.home() / ".zsh_history")   # Histórico do zsh
        pass

    registros = []
    for log in logs:
        registros.extend(conteudoLog(log))

    if not registros:
        print("Nenhum registro encontrado.")
        return

    mensagens = []
    for (ano, mes, dia), hora, titulo, ip, descricao in registros:
        usuario = extraiUsuario(descricao, maquina)
        inicio='Um' if usuario=='desconhecido' else 'O'
        mensagens.append(
            f'{inicio} usuário {usuario} realizou ações na auditoria de "{titulo}", IP: {ip} no dia {dia}/{mes}/{ano} às {hora}.'
        )

    if not mensagens:
        print("Nenhum evento de auditoria encontrado.")
    else:
        for mensagem in mensagens:
            print(mensagem)

if __name__ == "__main__":
    main()
