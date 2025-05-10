
import os
from cryptography.fernet import Fernet

def decrypt_file(file_path, fernet):
    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)

        if file_path.endswith(".enc"):
            output_file = file_path[:-4]
        else:
            output_file = file_path + ".dec"
        
        with open(output_file, "wb") as f:
            f.write(decrypted_data)
        print(f"Arquivo '{file_path}' descriptografado com sucesso em '{output_file}'.")
        
        os.remove(file_path)
        print(f"Arquivo criptografado '{file_path}' removido.")
    
    except Exception as e:
        print(f"Erro ao descriptografar '{file_path}': {e}")

def decrypt_directory(directory, fernet):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".enc"):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, fernet)

def main():
    key = input("Digite o caminho do arquivo de chave de criptografia (ex: C:\\MeuCaminho\\encryption.key): ").strip()
    
    if not os.path.exists(key):
        print(f"Arquivo de chave '{key}' não encontrado!")
        return

    with open(key, "rb") as f:
        key = f.read()
    fernet = Fernet(key)

    directory = input("Digite o caminho do diretório a ser descriptografado (ex: C:\\MeuDiretorio): ").strip()
    if not os.path.isdir(directory):
        print("Diretório inválido. Verifique o caminho informado.")
        return

    print(f"\nIniciando a descriptografia dos arquivos em: {directory}\n")
    decrypt_directory(directory, fernet)
    print("\nProcesso de descriptografia concluído.")

if __name__ == "__main__":
    main()