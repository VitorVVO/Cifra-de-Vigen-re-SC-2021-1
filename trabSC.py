# Trabalho 1 Seguranca computacional - Cifra de Vigenere
# Álvaro Veloso Cavalcanti Luz - 180115391
# Vitor Vasconcelos de Oliveira - 180114778


MAX_SENHA = 20
alfabeto = 'abcdefghijklmnopqrstuvwxyz'
idioma = 2  # 1 para portugues e 2 para ingles

# vetores de frequencias PTBR e ENG
frequencias_ENG = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
                   0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                   0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                   0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

frequencias_PTBR = [0.14630, 0.01400, 0.03880, 0.04990, 0.12570, 0.01020, 0.01300,
                    0.01280, 0.06180, 0.00400, 0.00020, 0.02780, 0.04740, 0.05050,
                    0.10730, 0.02520, 0.01200, 0.06530, 0.07810, 0.04340, 0.04630,
                    0.01670, 0.00010, 0.00210, 0.00010, 0.00470]


# funcao responsavel por cifrar a frase
# encontra a letra cifrada atraves da soma das posicoes no alfabeto das letras da chave e da frase
def cifra(frase, senha):
    new_frase = ''
    frase = frase.lower()
    senha = senha.replace(" ", "")
    contS = 0
    for i in range(0, len(frase)):
        if frase[i] in alfabeto:
            x = alfabeto.find(frase[i])
            if(contS == len(senha)):
                contS = 0
            y = alfabeto.find(senha[contS])
            if(x+y <= 25):
                new_frase = new_frase + alfabeto[x+y]
            else:
                new_frase = new_frase + alfabeto[x+y-26]
            contS += 1
        else:
            new_frase = new_frase + ""
    return new_frase.upper()


# funcao responsavel por decifrar a frase
# encontra a letra cifrada atraves da subtracao das posicoes no alfabeto das letras da chave e da frase
def decifra(frase, senha):
    new_frase = ''
    frase = frase.lower()
    senha = senha.replace(" ", "")
    contS = 0
    for i in range(0, len(frase)):
        if frase[i] in alfabeto:
            x = alfabeto.find(frase[i])
            if(contS == len(senha)):
                contS = 0
            y = alfabeto.find(senha[contS])
            if(x+y >= 0):
                new_frase = new_frase + alfabeto[x-y]
            else:
                new_frase = new_frase + alfabeto[x-y+26]
            contS += 1
        else:
            new_frase = new_frase + ""
    return new_frase.upper()


# Retorna o tamanho da chave mais provavel, ou seja, com maior IC


def get_tamanho_senha(texto):
    tabela_indice = []
    # Quebra o texto cifrado em sequencias baseadas no comprimento de chave de 0 ao tamanho maximo.
    for tamanho in range(MAX_SENHA):
        # A chave com maior IC eh a chave mais provavel
        soma_indice = 0.0
        media_indice = 0.0
        for i in range(tamanho):
            sequencia = ""
            for j in range(0, len(texto[i:]), tamanho):
                sequencia += texto[i+j]
            if len(sequencia) > 1:
                soma_indice += get_indice(sequencia)
        # se o tamanho for diferente de 0
        if tamanho != 0:
            media_indice = soma_indice/tamanho

        tabela_indice.append(media_indice)

    # retorna o comprimento da chave com  maior indice de coincidencia (chave mais provavel)
    melhor_tamanho = tabela_indice.index(
        sorted(tabela_indice, reverse=True)[0])
    segundo_melhor_tamanho = tabela_indice.index(
        sorted(tabela_indice, reverse=True)[1])

    if melhor_tamanho % segundo_melhor_tamanho == 0:
        # se sao multiplos
        return segundo_melhor_tamanho
    else:
        # se nao sao
        return melhor_tamanho


# Achando o indice de coincidencia atraves da formula
def get_indice(texto):
    N = float(len(texto))
    soma_frequencias = 0.0

    # Usinando a formula do indice de coincidencia
    for letra in alfabeto:
        soma_frequencias += texto.count(letra) * (texto.count(letra)-1)

    indice = soma_frequencias/(N*(N-1))

    return indice

# funcao responsavel por descobrir e retornar a senha
# realiza isso analisando a frequencia de cada letra da senha apra varias sequencias do texto


def get_senha(texto, tamanho):
    senha = ''
    for i in range(tamanho):
        sequencia = ""
        for j in range(0, len(texto[i:]), tamanho):
            sequencia += texto[i+j]
        senha += analisa_freq(sequencia)

    return senha


# Performa uma analise de frequencia no texto e retorna a letra decodificada para determinada parte da chave
# Usa o calculo estatistico de qui-quadrado para testar o quao similar duas distribuicoies sao
def analisa_freq(sequencia):
    qui_quadrados = [0] * len(alfabeto)

    for i in range(len(alfabeto)):
        soma_quadrados = 0.0
        offset = []
        valor_obs = [0] * len(alfabeto)

        for j in range(len(sequencia)):
            offset.append(
                chr(((ord(sequencia[j])-ord('a')-i) % len(alfabeto))+ord('a')))

        # conta o numero de vezes que cada letra do offset aparece para o calculo de frequencia
        for j in offset:
            valor_obs[ord(j) - ord('a')] += 1

        # divide o os valores de obs pelo tamanho da sequencia
        for j in range(len(alfabeto)):
            valor_obs[j] = valor_obs[j]/float(len(sequencia))

        # comparando utilizando a formula do qui-quadrado
        for j in range(len(alfabeto)):
            if(idioma == 1):
                soma_quadrados += ((valor_obs[j] - float(frequencias_PTBR[j])) * (
                    valor_obs[j] - float(frequencias_PTBR[j])))/float(frequencias_PTBR[j])
            elif(idioma == 2):
                soma_quadrados += ((valor_obs[j] - float(frequencias_ENG[j])) * (
                    valor_obs[j] - float(frequencias_ENG[j])))/float(frequencias_ENG[j])
        # adiciona na tabela
        qui_quadrados[i] = soma_quadrados

    # menor valor equivale ao deslocamento equivalente aa letra da chave
    deslocamento = qui_quadrados.index(min(qui_quadrados))

    # retorna a letra para qual a sequencia foi deslocada
    return chr(deslocamento+ord('a'))


while True:
    opt = int(input("escolha oque deseja fazer:\n1-> cifrar frase\n2-> decifrar frase\n3-> descobrir a senha por frequencia\n0-> EXIT\n"))
    if(opt == 1):
        frase = str(input("frase para ser cifrada:"))
        senha = str(input("senha:"))
        frase_filtrada = ''.join(x.lower()for x in frase if x.isalpha())
        new_frase = cifra(frase_filtrada, senha)
        print(new_frase)
    elif(opt == 2):
        frase = str(input("frase para ser decifrada:"))
        senha = str(input("senha:"))
        frase_filtrada = ''.join(x.lower()for x in frase if x.isalpha())
        new_frase = decifra(frase_filtrada, senha)
        print(new_frase)
    elif(opt == 3):
        frase = str(input("frase cifrada:"))
        idioma = int(input("idioma da mensagem:\n1-> Portugues\n2-> Ingles\n"))
        frase_filtrada = ''.join(x.lower()for x in frase if x.isalpha())
        tamanho_senha = get_tamanho_senha(frase_filtrada)
        senha = get_senha(frase_filtrada, tamanho_senha)
        new_frase = decifra(frase_filtrada, senha)
        print("Senha:", senha)
        print("Frase:", new_frase)
    elif(opt >= 4 or opt < 0):
        print("Escolha invalida!!!\n")
    elif(opt == 0):
        break
