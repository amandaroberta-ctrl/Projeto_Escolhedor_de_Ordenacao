"""Gera CSVs e gráficos comparando os seis métodos e o seletor."""
import csv, random, time, statistics, os
from src.ordenacao import METODOS, escolher, ordenar

N = int(os.environ.get("G2_N", "1200"))
REPETICOES = int(os.environ.get("G2_REPETICOES", "3"))
os.makedirs("dados", exist_ok=True)
os.makedirs("graficos", exist_ok=True)
rng = random.Random(2026)

def cenarios(n):
    aleatorio = [rng.randint(-10**8, 10**8) for _ in range(n)]
    faixa_estreita = [rng.randint(-50, 50) for _ in range(n)]
    quase = list(range(n))
    for _ in range(max(1, n // 100)):
        i, j = rng.randrange(n), rng.randrange(n)
        quase[i], quase[j] = quase[j], quase[i]
    minuscula = [rng.randint(-1000, 1000) for _ in range(20)]
    return {
        "aleatorio_chaves_grandes": aleatorio,
        "faixa_estreita": faixa_estreita,
        "quase_ordenado": quase,
        "lista_minuscula": minuscula,
    }

def medir(func, entrada):
    tempos = []
    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        saida = func(entrada)
        tempos.append(time.perf_counter() - inicio)
        if saida != sorted(entrada):
            raise AssertionError(f"{func.__name__} produziu resultado incorreto")
    return statistics.median(tempos) * 1000

def main():
    linhas = []
    for cenario, entrada in cenarios(N).items():
        for nome, func in METODOS.items():
            try:
                ms = medir(func, entrada)
                status = "ok"
            except (ValueError, MemoryError, RecursionError) as e:
                ms, status = "", f"indisponivel: {type(e).__name__}"
            linhas.append({"cenario": cenario, "metodo": nome, "tempo_ms": ms, "status": status})
        tempos_escolher = []
        for _ in range(REPETICOES):
            inicio = time.perf_counter()
            escolher(entrada)
            tempos_escolher.append(time.perf_counter() - inicio)
        t_escolher = statistics.median(tempos_escolher) * 1000
        nome = escolher(entrada)
        t_total = medir(ordenar, entrada)
        linhas.append({"cenario": cenario, "metodo": "ordenar_adaptativo", "tempo_ms": t_total, "status": f"escolheu:{nome}"})
        linhas.append({"cenario": cenario, "metodo": "escolher_sozinho", "tempo_ms": t_escolher, "status": f"escolheu:{nome}"})
    with open("dados/resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["cenario", "metodo", "tempo_ms", "status"])
        w.writeheader(); w.writerows(linhas)
    try:
        import matplotlib.pyplot as plt
        cen = list(cenarios(N).keys())
        for cenario in cen:
            subset = [x for x in linhas if x["cenario"] == cenario and x["tempo_ms"] != "" and x["metodo"] != "escolher_sozinho"]
            plt.figure(figsize=(10, 5))
            plt.bar([x["metodo"] for x in subset], [float(x["tempo_ms"]) for x in subset])
            plt.title(f"Tempos por método — {cenario}")
            plt.ylabel("Tempo mediano (ms)")
            plt.xticks(rotation=25, ha="right")
            plt.tight_layout()
            plt.savefig(f"graficos/{cenario}.png", dpi=140)
            plt.close()
        print("Gráficos salvos em graficos/.")
    except ImportError:
        print("matplotlib não instalado; CSV gerado. Instale com: pip install matplotlib")
    print("CSV gerado em dados/resultados.csv")
    print(f"N={N}; repetições={REPETICOES}; tempos em milissegundos.")

if __name__ == "__main__":
    main()
