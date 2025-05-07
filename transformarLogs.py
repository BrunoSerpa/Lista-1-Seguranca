from os import path, makedirs, listdir
from Evtx.Evtx import Evtx
from xml.etree.ElementTree import fromstring
from pyuac import isUserAdmin, runAsAdmin

def converteEvtxParaLogLinux(caminhoEvtx, caminhoLog):
    try:
        linhas = []
        with Evtx(caminhoEvtx) as log:
            for record in log.records():
                dadosXml = fromstring(record.xml())
                
                namespace = dadosXml.tag.split('}')[0][1:] if '}' in dadosXml.tag else ''
                ns = {'ns': namespace} if namespace else {}
    
                dataElemento = dadosXml.find(".//ns:TimeCreated", namespaces=ns)
                dataHora = dataElemento.attrib.get("SystemTime") if dataElemento is not None else None
    
                idElemento = dadosXml.find(".//ns:EventID", namespaces=ns)
                event_id = idElemento.text if idElemento is not None else None
    
                nomeElemento = dadosXml.find(".//ns:Provider", namespaces=ns)
                nome = nomeElemento.attrib.get("Name") if nomeElemento is not None else None
    
                mensagensElementos = dadosXml.findall(".//ns:EventData/ns:Data", namespaces=ns)
                mensagens = [dado.text for dado in mensagensElementos if dado.text]
                mensagem = " ".join(mensagens) if mensagens else None
                if mensagem:
                    mensagem = mensagem.replace("<string>", "").replace("</string>", "").strip()
    
                if not dataHora or not event_id or not nome or not mensagem:
                    continue
    
                textoLog = f"{dataHora} {nome}[{event_id}]: {mensagem}"
                linhas.append(textoLog)
    
        if not linhas:
            print(f"Nenhum registro válido encontrado em {caminhoEvtx}. Arquivo não será salvo.")
            return False
    
        with open(caminhoLog, "w", encoding="utf-8") as linhaLog:
            for linha in linhas:
                linhaLog.write(linha + "\n")
    
        print(f"Arquivo {caminhoEvtx} convertido para {caminhoLog}")
        return True
    except Exception as e:
        print(f"Erro ao converter {caminhoEvtx}: {e}")
        return False

def main():
    diretorioEvtx = r"C:\Windows\System32\winevt\Logs"
    diretorioAtual = path.dirname(path.abspath(__file__))
    diretorioSalvarLogs = path.join(diretorioAtual, "logs")

    if isUserAdmin():
        count = 0
        if not path.exists(diretorioSalvarLogs):
            makedirs(diretorioSalvarLogs)
        for filename in listdir(diretorioEvtx):
            if filename.endswith(".evtx"):
                caminhoEvtx = path.join(diretorioEvtx, filename)
                caminhoLog = path.join(diretorioSalvarLogs, filename.replace(".evtx", ".log"))

                if converteEvtxParaLogLinux(caminhoEvtx, caminhoLog):
                    count += 1
        print(f"{count} arquivo(s) convertido(s) com sucesso.")
        input("Conversões concluídas. Pressione Enter para retornar ao terminal inicial.")
        exit(0)
    else:
        print("É necessário permissão de administrador para acessar os logs!")
        try:
            runAsAdmin()
        except Exception as e:
            return
        return

if __name__ == "__main__":
    main()