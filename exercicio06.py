# Faça  um  programa  que  leia  um  arquivo  de  log  e  informe:  Data  que  a  máquina ligou, hora que a máquina desligou e tempo que ela ficou ligada em um determinado dia.
from conteudoLog import main as conteudoLog
from os import name, path
from datetime import datetime, timedelta

def parse_data_e_hora(ano, mes, dia, hora):
    try:
        return datetime.strptime(f"{ano}-{mes}-{dia} {hora}", "%Y-%m-%d %H:%M:%S")
    except:
        return None

def main(maquina=None):
    if not maquina:
        maquina = name

    logs = []
    if maquina == "nt":
        logs.append(path.join(path.dirname(__file__), 'logs', 'System.log'))

    registros = []
    for log in logs:
        registros.extend(conteudoLog(log))

    eventos = []
    for (ano, mes, dia), hora, titulo, ip, _ in registros:
        datahora = parse_data_e_hora(ano, mes, dia, hora)
        if not datahora:
            continue

        if "Kernel-General" in titulo and "1" in ip:
            eventos.append(("ligou", datahora))
        elif "Power-Troubleshooter" in titulo and "1" in ip:
            eventos.append(("acordou", datahora))
        elif "Kernel-Power" in titulo and ip in ("107", "42"):
            eventos.append(("desligou", datahora))

    eventos.sort(key=lambda x: x[1])

    ligado = None
    sessoes = []

    for tipo, datahora in eventos:
        if tipo in ("ligou", "acordou"):
            if not ligado:
                ligado = datahora
        elif tipo == "desligou":
            if ligado:
                sessoes.append((ligado, datahora))
                ligado = None

    if not sessoes:
        print("Nenhum ciclo de energia completo encontrado.")
        return

    same_day = {}
    cross_day = []
    for ligou, desligou in sessoes:
        duracao = desligou - ligou
        if ligou.date() == desligou.date():
            key = ligou.date()
            same_day.setdefault(key, []).append((ligou, desligou, duracao))
        else:
            cross_day.append((ligou, desligou, duracao))

    # Para sessões de mesmo dia: agrupa por data, lista os intervalos e faz a soma dos tempos
    for day in sorted(same_day.keys()):
        sessions = same_day[day]
        # Ordena pelas horas de início (caso não estejam ordenados)
        sessions.sort(key=lambda tup: tup[0])
        intervals = []
        total_seconds = 0  # soma em segundos
        for ligou, desligou, duracao in sessions:
            intervals.append(f"as {ligou.strftime('%H:%M:%S')} às {desligou.strftime('%H:%M:%S')}")
            total_seconds += duracao.total_seconds()

        # Converte a soma dos segundos para um objeto timedelta e formata (descartando frações de segundo)
        total_dur = timedelta(seconds=int(total_seconds))
        day_str = day.strftime('%d/%m/%Y')
        print(f"No dia {day_str} o dispositivo estava ligado ou acordado:\nD" + ";\nD".join(intervals) + f".\nTotalizando {str(total_dur).split('.')[0]}.")

    # Sessões que atravessam dias são exibidas individualmente
    for ligou, desligou, duracao in cross_day:
        dur_str = str(duracao).split('.')[0]
        print(f"No dia {ligou.strftime('%d/%m/%Y')} o dispositivo estava ligado às {ligou.strftime('%H:%M:%S')} e se desligou/suspendeu no dia {desligou.strftime('%d/%m/%Y')} às {desligou.strftime('%H:%M:%S')}, totalizando {dur_str}.")

if __name__ == "__main__":
    main()