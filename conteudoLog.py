from re import match, compile

from escolherLog import main as escolherLog

cabecalho = compile(
    r'^(\d{4}-\d{2}-\d{2})\s+'          # Data
    r'(\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+' # Horário
    r'(.*?)'                            # Título
    r'\[(\d+)\]'                        # IP
    r'(.*?)$'                           # Descrição
)

def primeiraLinha(linhaLog):
    dados = cabecalho.search(linhaLog)
    if not dados:
        return None
    data, horario, titulo, ip, descricao = dados.groups()
    ano, mes, dia = data.split('-')
    hora = horario.split('.')[0]  # Remove milissegundos
    
    descricao = descricao.strip()
    if descricao.startswith(':'):
        descricao = [descricao[1:].strip()]
    else:
        descricao = [descricao]

    return [(ano, mes, dia), hora, titulo.strip(), ip.strip(), descricao]

def main(log=None):
    if not log:
        log = escolherLog()

    registros = []
    with open(log, 'r', encoding='utf8') as arquivo:
        registro = None

        linhas = arquivo.readlines()
        for linha in linhas:
            if cabecalho.search(linha):
                if registro:
                    registros.append(registro)
                registro = primeiraLinha(linha)

                continue
            elif match(r'\d{*}',linha.strip()) or linha.strip() == "" :
                continue

            if registro and isinstance(registro[4], list):
                registro[4].append(linha.strip())
    return registros

if __name__ == "__main__":
    registros = main()
    if not registros:
        print("Nenhum registro encontrado")
    else:
        for posicao, ((ano, mes, dia), hora, titulo, ip, descricao) in enumerate(registros, start=1):
            print(f"{posicao}º Registro - {titulo} | IP: {ip} (Data: {dia}/{mes}/{ano} | Hora: {hora}):")
            textoDescricao = ""
            for desc in descricao:
                textoDescricao += f'{desc}; '
            print(f'Descrições: {textoDescricao[0:-1]}')