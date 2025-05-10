# Faça  um  programa  que  criptografe  uma  sequência  de  arquivos  de  um  diretório específico do sistema.
import os
from cryptography.fernet import Fernet

def generate_key(key_file="encryption.key"):
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)
    print(f"Chave gerada e salva em '{key_file}'.")
    return key

def load_key(key_file="encryption.key"):
    if not os.path.exists(key_file):
        return generate_key(key_file)
    with open(key_file, "rb") as f:
        key = f.read()
    return key

def encrypt_file(file_path, fernet):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        encrypted_data = fernet.encrypt(data)
        new_file = file_path + ".enc"
        with open(new_file, "wb") as f:
            f.write(encrypted_data)
        print(f"Arquivo '{file_path}' criptografado com sucesso em '{new_file}'.")
        os.remove(file_path)
        print(f"Arquivo original '{file_path}' removido.")
    except Exception as e:
        print(f"Erro ao criptografar o arquivo '{file_path}': {e}")

def encrypt_directory(directory, fernet):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".enc"):
                continue
            file_path = os.path.join(root, file)
            encrypt_file(file_path, fernet)

def main():
    directory = input("Digite o caminho do diretório a ser criptografado (ex: C:\\MeuDiretorio): ").strip()
    if not os.path.isdir(directory):
        print("Diretório inválido. Verifique o caminho informado.")
        return

    key = load_key()
    fernet = Fernet(key)
    
    print(f"\nIniciando a criptografia dos arquivos em: {directory}\n")
    encrypt_directory(directory, fernet)
    print("\nProcesso de criptografia concluído.")

if __name__ == "__main__":
    main()
