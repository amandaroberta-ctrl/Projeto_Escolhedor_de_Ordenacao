Projeto acadêmico desenvolvido em Python para implementar, comparar e analisar seis métodos de ordenação, além de um seletor adaptativo que escolhe um algoritmo com base nas características da lista de entrada.

Feito em dupla:

- Amanda Roberta Bandeira Santos

- Antonio Roberto Da Silva Santos

Objetivo: Implementar seis métodos de ordenação e um seletor que escolha um deles de acordo com características baratas da entrada.

- Inserção
- Intercalação (merge sort)
- Rápida com pivô aleatório
- Híbrida (intercalação com inserção nos trechos pequenos)
- Contagem (com proteção para faixa grande)
- Base (radix sort decimal, incluindo negativos)
O projeto também possui um seletor adaptativo que utiliza características da lista para escolher um dos métodos.

Como executar o benchmark:

Na raiz do projeto, execute:
```bash
python benchmark.py
```
O programa executa os cenários definidos no código, mede os tempos dos métodos e gera os arquivos de resultados e gráficos.
Por padrão, o benchmark utiliza 1.200 elementos nos cenários grandes e três repetições por método.
Para alterar esses parâmetros no Windows PowerShell:
```powershell
$env:G2_N="3000"
$env:G2_REPETICOES="5"
python benchmark.py
```
O exemplo acima utiliza 3.000 elementos nos cenários grandes e cinco repetições por método.
Importante: executar novamente o benchmark atualiza os resultados conforme a nova execução. Os tempos podem ser diferentes dos apresentados no relatório.

Resultados:
Os arquivos de resultados estão organizados da seguinte forma:

- `resultados.csv`: contém os tempos medidos e o estado de cada execução.
- `gráficos/`: contém os gráficos individuais dos cenários e o gráfico de comparação geral.
- `RELATORIO.md`: apresenta a metodologia, a tabela de resultados, a análise dos cenários, o custo do seletor e as limitações observadas.
Os resultados medidos indicam que nenhum método ou estratégia adaptativa deve ser considerado o mais rápido para todas as entradas sem evidências adicionais.

Observações:
O método contagem possui uma proteção para evitar o uso de uma faixa de valores excessivamente grande. A implementação didática da ordenação rápida utiliza listas auxiliares, não sendo uma versão *in-place*. O seletor adaptativo utiliza regras heurísticas e não garante escolher o método mais rápido em todas as situações. Os tempos de execução dependem do computador, da carga do sistema, da versão do Python e das características dos dados.

