# Faça  um  programa  que  conte  quantos  acessos  um  determinado  IP  fez  em  um  sistema.
from os import name
from collections import defaultdict

from conteudoLog import main as conteudoLog

def extraiTipoAcesso(descricoes):
    if name == "nt":
        for descricao in descricoes:
            if descricao.startswith("S-1-5-"):
                return descricao.split()[0]
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

    contagem = defaultdict(int)
    for (_, _, _), _, _, _, descricao in registros:
        sid = extraiTipoAcesso(descricao)
        contagem[sid] += 1

    mensagems = []
    if name == "nt":
        for sid, contagem in contagem.items():
            mensagems.append(f"Usuário (SID): {sid} — {contagem} aç{"ão" if contagem == 1 else "ões"}")
        if not mensagems:
            print("Nenhuma de ação de usuário encontrada.")
            return
        print("Contagem de ações por usuário (SID primário):")
    else:
        print("Contagem de acesso por IP:\n")
        for ip, contagem in contagem.items():
            mensagems.append(f"(IP): {ip} — {contagem} acesso{"" if contagem == 1 else "s"}")
        if not mensagems:
            print("Nenhum acesso por IP encontrado.")
            return
        print("Contagem de acesso por IP:")

    for mensagem in mensagems:
        print(mensagem)

if __name__ == "__main__":
    main()