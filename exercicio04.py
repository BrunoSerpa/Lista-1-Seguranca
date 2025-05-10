# Faça  um  programa  que  conte  quantos  acessos  um  determinado  IP  fez  em  um  sistema.
from conteudoLog import main as conteudoLog
from os import name, path
from collections import defaultdict

def extrai_sid_usuario(descricao):
    """Extrai apenas o primeiro SID de usuário da descrição."""
    for parte in descricao:
        if parte.startswith("S-1-5-"):
            return parte.split()[0]
    return "desconhecido"

def main(maquina=None):
    if not maquina:
        maquina = name

    logs = []
    if maquina == "nt":
        logs.append(path.join(path.dirname(__file__), 'logs', 'Security.log'))

    registros = []
    for log in logs:
        registros.extend(conteudoLog(log))

    if not registros:
        print("Nenhum registro encontrado.")
        return

    contagem_usuarios = defaultdict(int)

    for (_, _, _), _, _, _, descricao in registros:
        sid = extrai_sid_usuario(descricao)
        contagem_usuarios[sid] += 1

    print("Contagem de ações por usuário (SID primário):\n")
    for sid, contagem in contagem_usuarios.items():
        print(f"Usuário (SID): {sid} — {contagem} {"ação" if contagem == 1 else "ações"}")

if __name__ == "__main__":
    main()
