# Faça  um  programa  que  registre  eventos  de  auditoria,  como  quando  um  usuário acessa  ou  altera  um  recurso.  Cada  evento  deve  ser  salvo  em  um  arquivo  com informações como: data, hora, nome do usuário, ação realizada, etc.
from os import name

from conteudoLog import main as conteudoLog

def extraiUsuario(descricoes):
    if name == "nt":
        for descricao in descricoes:
            if "MicrosoftAccount:user=" in descricao:
                return descricao.split("=", 1)[1].split()[0]
        return "desconhecido"
    return descricoes[0]
def main():
    logs = []
    if name == "nt":
        from os import path        
        logs.append(path.join(path.dirname(__file__), 'logs', 'Security.log')) #logs/Security.log
    elif name == "posix":
        from pathlib import Path
        logs.append(Path.home() / ".bash_history")  # Histórico do bash
        logs.append(Path.home() / ".zsh_history")   # Histórico do zsh

    registros = []
    for log in logs:
        registros.extend(conteudoLog(log))

    if not registros:
        print("Nenhum registro encontrado.")
        return

    mensagens = []
    for (ano, mes, dia), hora, titulo, ip, descricao in registros:
        usuario = extraiUsuario(descricao)
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