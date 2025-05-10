from datetime import datetime

from buscaLogs import main as buscaLogs
from conteudoLog import main as conteudoLog

# Tempo de retenção: 6 meses (aproximadamente 6 x 30 dias em segundos)
tempoRetencao = 6 * 30 * 24 * 60 * 60  
hoje = datetime.now().replace(microsecond=0)

def verifica_conformidade_registros(registros):
    earliest_date = hoje

    for ((ano, mes, dia), hora, _, _, _) in registros:
        try:
            log_dt = datetime.strptime(f"{ano}-{mes}-{dia} {hora}", "%Y-%m-%d %H:%M:%S")
            if log_dt < earliest_date:
                earliest_date = log_dt
        except Exception:
            continue


    retencao_ok = False
    if earliest_date:
        print(f'Registro mais antigo em {earliest_date}')
        retencao_ok = (hoje - earliest_date).total_seconds() >= tempoRetencao

    return retencao_ok

def main(logs):
    if not logs:
        print("Nenhum log encontrado.")
        return

    registros = []
    for log in logs:
        registros.extend(conteudoLog(log))
    
    if not registros:
        print("Nenhum registro encontrado.")
        return

    print("Verificando conformidade dos logs segundo o Marco Civil da Internet (Lei nº 12.965/2014)...")
    retencao_ok = verifica_conformidade_registros(registros)
    if retencao_ok:
        print("- Retenção de logs: Em comformidade (logs retidos por pelo menos 6 meses)")
    else:
        print("- Retenção de logs: Não está em conformidade (logs retidos por menos de 6 meses)")

if __name__ == "__main__":
    main(buscaLogs())
