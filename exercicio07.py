# Faça  um  programa  que  gere  um  arquivo  de  saída,  como  um  log,  para  uma determinada aplicação. Pode ser um servidor Web, ou qualquer outro serviço.
import logging
import time
import random
from datetime import datetime

class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%Y-%m-%d %H:%M:%S.%f")
        return s

def setup_logger(log_file):
    logger = logging.getLogger("Servico Teste")
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        logger.handlers.clear()
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    formatter = CustomFormatter(
        fmt="%(asctime)s %(name)s[991]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S.%f"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def simulate_application(logger):
    logger.info("Servico iniciado")
    
    for i in range(10):
        time.sleep(random.uniform(0.1, 0.5))
        event = random.choice(["REQUEST", "PROCESS", "ERROR", "DEBUG"])
        if event == "REQUEST":
            logger.info("Requisicao recebida: GET /index.html")
        elif event == "PROCESS":
            logger.info("Processando dados do usuario")
        elif event == "ERROR":
            logger.error("Erro ao conectar ao banco de dados")
        elif event == "DEBUG":
            logger.debug("Valor de x=42, y=3.14 para depuracao")
            
    logger.info("Servico finalizado")

def main():
    # Define o arquivo de saída dos logs
    log_file = "logs/appTeste.log"
    
    # Configura o logger com o nosso formatter customizado
    logger = setup_logger(log_file)
    
    # Simula a execução da aplicação
    simulate_application(logger)
    
    print(f"Log gerado com sucesso no arquivo: {log_file}")

if __name__ == "__main__":
    main()