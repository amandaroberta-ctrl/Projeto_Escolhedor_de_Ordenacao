import random
def insercao(v):
    a = list(v)
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        while j >= 0 and a[j] > chave:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = chave
    return a

def intercala(v):
    a = list(v)
    if len(a) <= 1:
        return a
    meio = len(a) // 2
    esquerda = intercala(a[:meio])
    direita = intercala(a[meio:])
    resultado, i, j = [], 0, 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i]); i += 1
        else:
            resultado.append(direita[j]); j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado

def rapida_aleatoria(v):
    if len(v) <= 1:
        return list(v)
    pivo = random.choice(v)
    menores = [x for x in v if x < pivo]
    iguais = [x for x in v if x == pivo]
    maiores = [x for x in v if x > pivo]
    return rapida_aleatoria(menores) + iguais + rapida_aleatoria(maiores)

def hibrida(v, limite=24):
    a = list(v)
    if len(a) <= limite:
        return insercao(a)
    meio = len(a) // 2
    esquerda = hibrida(a[:meio], limite)
    direita = hibrida(a[meio:], limite)
    resultado, i, j = [], 0, 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i]); i += 1
        else:
            resultado.append(direita[j]); j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado

def contagem(v, faixa_max=1_000_000):
    if len(v) <= 1:
        return list(v)
    minimo, maximo = min(v), max(v)
    faixa = maximo - minimo + 1
    if faixa > faixa_max:
        raise ValueError(f"Faixa {faixa} excede o limite seguro {faixa_max}")
    contadores = [0] * faixa
    for x in v:
        contadores[x - minimo] += 1
    saida = []
    for i, quantidade in enumerate(contadores):
        if quantidade:
            saida.extend([i + minimo] * quantidade)
    return saida

def _contagem_digito(valores, expoente):
    contadores = [0] * 10
    saida = [0] * len(valores)
    for x in valores:
        contadores[(x // expoente) % 10] += 1
    for i in range(1, 10):
        contadores[i] += contadores[i - 1]
    for x in reversed(valores):
        digito = (x // expoente) % 10
        contadores[digito] -= 1
        saida[contadores[digito]] = x
    return saida

def base(v):
    a = list(v)
    if len(a) <= 1:
        return a
    negativos = [-x for x in a if x < 0]
    positivos = [x for x in a if x >= 0]

    def ordenar_nao_negativos(valores):
        if not valores:
            return []
        resultado = list(valores)
        expoente = 1
        maior = max(resultado)
        while maior // expoente > 0:
            resultado = _contagem_digito(resultado, expoente)
            expoente *= 10
        return resultado

    neg_ordenados = ordenar_nao_negativos(negativos)
    pos_ordenados = ordenar_nao_negativos(positivos)
    return [-x for x in reversed(neg_ordenados)] + pos_ordenados

METODOS = {
    "insercao": insercao,
    "intercalacao": intercala,
    "rapida_aleatoria": rapida_aleatoria,
    "hibrida": hibrida,
    "contagem": contagem,
    "base": base,
}

def escolher(v):
    n = len(v)
    if n <= 32:
        return "insercao"
    minimo = maximo = v[0]
    descidas = 0
    anterior = v[0]
    for x in v[1:]:
        if x < minimo: minimo = x
        if x > maximo: maximo = x
        if x < anterior: descidas += 1
        anterior = x
    faixa = maximo - minimo + 1
    if faixa <= 256 and faixa <= max(32, 2 * n):
        return "contagem"
    if descidas <= max(2, n // 100):
        return "insercao"
    if max(abs(minimo), abs(maximo)) >= 10**7:
        return "base"
    return "hibrida"

def ordenar(v):
    nome = escolher(v)
    return METODOS[nome](v)
