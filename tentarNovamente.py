def main(mensagem='Tentar novamente'):
    while True:
        resposta = input(f"{mensagem}? (s/n)\n").upper()
        if resposta == 'S':
            return True
        elif resposta == 'N':
            return False
        else:
            print("Resposta inválida. Tente novamente.")
            continue

if __name__ == "__main__":
    main()