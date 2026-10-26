
Objetivo: 
O objetivo deste projeto é implementar seis métodos de ordenação e desenvolver um seletor adaptativo capaz de escolher um método de acordo com características da lista de entrada.
A proposta é comparar os algoritmos em diferentes cenários e verificar se a escolha automática apresenta um desempenho competitivo em relação aos métodos executados individualmente.
O seletor é uma heurística: ele utiliza características da entrada para tomar uma decisão, mas não garante que escolherá o método mais rápido em todas as situações.

| Método | Funcionamento | Complexidade e observações |
|---|---|---|
| Inserção | Insere cada elemento na posição correta de uma parte já ordenada. | O(n²) no pior caso. Costuma funcionar bem em listas pequenas ou quase ordenadas. |
| Intercalação | Divide a lista em partes menores, ordena essas partes e depois as intercala. | O(n log n) em tempo e O(n) de memória auxiliar. |
| Rápida aleatória | Escolhe um pivô aleatório e separa os elementos menores e maiores. | O(n log n) em média/esperado e O(n²) no pior caso. |
| Híbrida | Utiliza intercalação e aplica inserção em trechos pequenos. | Mantém comportamento O(n log n) para a ordenação, buscando reduzir o custo em partes pequenas. |
| Contagem | Conta quantas vezes cada valor aparece dentro de uma faixa. | O(n + k) em tempo e O(k) de memória, em que k representa a faixa de valores. Pode ser inadequada quando a faixa é muito grande. |
| Base | Ordena os números dígito por dígito. | O(d · n), considerando uma base fixa, em que d é a quantidade de dígitos. A implementação também trata inteiros negativos. |

As complexidades são referências teóricas; os tempos reais também dependem da implementação, dos dados e do ambiente de execução.

Regras do seletor:

A função `escolher(v)` utiliza as seguintes regras:

1. Se a lista possui até 32 elementos, escolhe inserção.
2. Para listas maiores, percorre os valores para estimar o mínimo, o máximo e a quantidade de descidas entre elementos vizinhos.
3. Se a faixa de valores for pequena — até 256 posições e relativamente pequena em relação ao tamanho da lista — escolhe contagem.
4. Se houver poucas descidas entre vizinhos, escolhe inserção.
5. Se algum valor tiver magnitude de pelo menos 10 milhões, escolhe base.
6. Nos demais casos, escolhe o método híbrido.

Os limites numéricos são parâmetros experimentais definidos nesta implementação, não valores obrigatórios estabelecidos pelo professor.
As regras foram inspiradas nas características dos algoritmos: inserção pode ser vantajosa em listas pequenas ou quase ordenadas; contagem é interessante quando a faixa é pequena; base trabalha dígito por dígito; e a híbrida oferece uma alternativa geral.

Cenários e resultados:

Os valores desta tabela foram obtidos na execução do benchmark realizada no computador utilizado para o projeto. Os tempos estão em milissegundos (ms) e foram arredondados para facilitar a leitura.

| Cenário | Inserção | Intercalação | Rápida aleatória | Híbrida | Contagem | Base | Adaptativo |
|---|---:|---:|---:|---:|---:|---:|---:|
| Aleatório com chaves grandes | 29,380 | 7,746 | 2,653 | 2,675 | Indisponível | 1,856 | 1,898 |
| Faixa estreita | 26,691 | 2,406 | 0,763 | 1,535 | 0,109 | 0,489 | 0,186 |
| Quase ordenado | 0,640 | 1,773 | 1,606 | 0,829 | 0,371 | 0,868 | 0,871 |
| Lista minúscula | 0,009 | 0,023 | 0,024 | 0,009 | 0,074 | 0,021 | 0,009 |

No cenário de chaves grandes, o método de contagem foi registrado como indisponível porque gerou um `ValueError`, conforme a proteção implementada para faixas de valores muito grandes.
Os resultados completos, incluindo os valores sem arredondamento e os estados de execução, estão em `dados/resultados.csv`. Os gráficos correspondentes estão na pasta `graficos/`.
Os tempos podem variar de acordo com o computador, a carga do sistema e a versão do Python.

Análise dos resultados:

Aleatório com chaves grandes - O método base apresentou o menor tempo entre os métodos disponíveis, com **1,856 ms**. O adaptativo escolheu base e levou **1,898 ms**.
A pequena diferença é compatível com o custo adicional de executar o seletor antes da ordenação. Nesse cenário, a escolha do algoritmo foi adequada, mas o adaptativo não foi mais rápido que executar base diretamente.

Faixa estreita - O método contagem foi o mais rápido, com **0,109 ms**. O adaptativo também escolheu contagem e levou **0,186 ms**.
Esse resultado é coerente com a característica do algoritmo de contagem: quando a faixa de valores é pequena, ele pode ordenar os elementos sem precisar comparar cada par de valores.

Quase ordenado - O método contagem foi o mais rápido nesta execução, com **0,371 ms**. Entretanto, o adaptativo escolheu a versão híbrida, que levou **0,871 ms**.
Esse cenário mostra uma limitação da heurística: mesmo ao identificar características da lista, o seletor não necessariamente escolhe o algoritmo que terá o menor tempo medido.

Lista minúscula - A inserção apresentou o menor tempo, aproximadamente **0,0088 ms**. O adaptativo também escolheu inserção e levou aproximadamente **0,0089 ms**.
A diferença é muito pequena e pode variar entre execuções. Em listas desse tamanho, o custo de preparação e medição pode ter influência significativa no resultado.

Custo do seletor:
Para listas maiores que 32 elementos, o seletor percorre a entrada uma vez para calcular características como mínimo, máximo e quantidade de descidas entre vizinhos.
Assim, a análise realizada pelo seletor tem custo de tempo O(n) e espaço auxiliar O(1), desconsiderando o espaço usado pela lista de entrada.
Para listas com até 32 elementos, a função retorna inserção diretamente, sem precisar realizar essa análise.
O seletor acrescenta um custo antes da ordenação. Por isso, mesmo quando escolhe o algoritmo mais rápido para determinado cenário, o tempo total de `ordenar(v)` pode ser ligeiramente maior do que executar esse algoritmo diretamente.
No CSV, `escolher_sozinho` representa o tempo gasto apenas para selecionar o método, enquanto `ordenar_adaptativo` inclui a seleção e a ordenação.

Caso em que o seletor não escolheu o método mais rápido:
No cenário de lista quase ordenada, o seletor escolheu a versão híbrida, que levou **0,871 ms**. Entretanto, o método contagem levou **0,371 ms** e foi o mais rápido entre os métodos disponíveis.
Portanto, esse resultado demonstra que as regras do seletor não identificam sempre a melhor opção para cada entrada.
Além disso, no cenário de faixa estreita, o adaptativo levou **0,186 ms**, enquanto executar contagem diretamente levou **0,109 ms**. Isso demonstra que o custo adicional da seleção também deve ser considerado na comparação.

Testes:
A suíte de testes verifica o comportamento dos algoritmos em diferentes casos:

- Lista vazia.
- Lista com um único elemento.
- Lista com todos os valores iguais.
- Lista já ordenada.
- Lista em ordem inversa.
- Presença de números negativos.
- Proteção do método contagem para uma faixa de valores muito grande.

Esses testes ajudam a verificar se os algoritmos produzem resultados corretos em situações comuns e em casos especiais.

Para executar os testes, utilize:

```bash
python -m unittest discover -s tests -v
```

Final:
O projeto permitiu implementar e comparar seis métodos de ordenação, além de desenvolver um seletor adaptativo baseado nas características da entrada.
Nos resultados obtidos, o adaptativo apresentou desempenho competitivo em alguns cenários, mas não foi sempre mais rápido que os métodos executados individualmente. Em especial, o cenário quase ordenado mostrou que a heurística pode escolher uma opção diferente da mais rápida na medição.
Conclui-se que a escolha adaptativa é uma estratégia útil para experimentar decisões automáticas, mas sua eficiência depende das regras utilizadas, das características dos dados e do custo adicional da seleção.
