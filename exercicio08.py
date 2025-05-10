# Faça  um  programa  que  verifique  as  permissões  de  acesso  de  arquivos  em  um diretório e informe se eles estão ou não vulneráveis.
import os
import subprocess

def check_vulnerability(file_path):
    try:
        result = subprocess.check_output(
            ["icacls", file_path],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Erro ao verificar '{file_path}': {e.output}")
        return None

    vulnerable = False
    for line in result.splitlines():
        if "Everyone:" in line:
            if any(perm in line for perm in ["(F)", "(M)", "(W)", "(RXW)"]):
                vulnerable = True
                break
        if "BUILTIN\\Users:" in line or "Users:" in line:
            if any(perm in line for perm in ["(F)", "(M)", "(W)", "(RXW)"]):
                vulnerable = True
                break
    return vulnerable

def scan_directory(directory):
    vulnerable_files = []
    secure_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            file_path = os.path.join(root, f)
            status = check_vulnerability(file_path)
            if status is None:
                continue
            if status:
                vulnerable_files.append(file_path)
            else:
                secure_files.append(file_path)
    return vulnerable_files, secure_files

def main():
    directory = input("Digite o caminho do diretório a ser verificado (ex: C:\\MeuDiretorio): ").strip()
    
    if not os.path.isdir(directory):
        print("Diretório inválido. Verifique o caminho informado.")
        return

    print(f"\nVerificando arquivos em: {directory}\n")
    vulnerable, secure = scan_directory(directory)
    
    if vulnerable:
        print("Arquivos vulneráveis:")
        for file in vulnerable:
            print(f"{file}")
    else:
        print("Nenhum arquivo vulnerável encontrado.")

    if secure:
        print("\nArquivos com permissões seguras:")
        for file in secure:
            print(f"{file}")
    else:
        print("\nNenhum arquivo com permissões seguras encontrado.")

if __name__ == "__main__":
    main()