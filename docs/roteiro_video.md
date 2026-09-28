# Roteiro do Vídeo de Apresentação (até 7 minutos)

> **Formato exigido:** apresentação técnica de até 7 min, **mostrando o rosto** e
> **compartilhando a tela** com o código. Responda de forma objetiva às perguntas abaixo.
> Ao final, coloque o link do vídeo no `README.md` e/ou no AVA.

**Aluno:** Diogo Durval Koerich Pereira — **Turma:** T3 (Visualização de Dados e BI)

---

## Sugestão de tempo

| Bloco | Tempo | Tela |
|---|---|---|
| Abertura e objetivo | 0:00 – 0:40 | rosto + README |
| Estrutura e as 2 consultas SQL | 0:40 – 2:10 | `sql/query_1.sql`, `sql/query_2.sql` |
| Análise em Python (EDA) | 2:10 – 3:40 | `python/analise.py` ou notebook rodando |
| Gráficos e resultados | 3:40 – 6:00 | pasta `graficos/` |
| Insight final e limitações | 6:00 – 6:50 | README (Seção 5) |
| Encerramento | 6:50 – 7:00 | rosto |

---

## Perguntas obrigatórias — respostas prontas (adapte com suas palavras)

### 1) Qual foi o objetivo da análise e quais filtros você aplicou? Como influenciaram os resultados?
- **Objetivo:** entender a estrutura salarial da empresa por **departamento**, **cargo** e
  **região**, usando a base HR do FreeSQL.
- **Filtros aplicados (`WHERE`):**
  - Query 1: `WHERE DEPARTMENT_ID IS NOT NULL` → só funcionários alocados a um departamento.
  - Query 2: `WHERE REGION_NAME IS NOT NULL` → só registros com região identificada.
- **Influência:** a base tem 107 funcionários e as consultas retornam **106**. Os dois filtros
  removem o mesmo registro — a funcionária **Kimberely Grant (ID 178)**, sem departamento na
  base. Isso deixa a análise mais consistente (todo salário fica ligado a um departamento e a
  uma região) e já revela um **problema de qualidade de dados**.

### 2) Como os salários variam entre departamentos e cargos? (comparação encontrada nos dados)
- **Departamentos:** o **Executive** tem a maior média (~**US$ 19.333**) e o **Shipping** a
  menor (~**US$ 3.476**) — uma diferença de mais de **5x**.
- **Cargos:** vai do **President (US$ 24.000)** até o **Stock/Purchasing Clerk (~US$ 2.800)**.
- **Comparação clara:** *Sales* é um departamento grande (34 pessoas) com média alta
  (~US$ 8.956), enquanto *Shipping* (45 pessoas) puxa a base salarial para baixo.

### 3) Como os funcionários estão distribuídos entre as regiões e quais diferenças salariais?
- **Americas: 70 funcionários** (mediana **US$ 3.300**); **Europe: 36** (mediana **US$ 8.900**).
- A **Americas** tem **mais gente, mas mediana menor**, porque concentra o setor operacional
  (Shipping/Stock, nos EUA). A **Europe** tem menos gente e mediana maior, por reunir
  **Vendas** (Reino Unido) e **Relações Públicas** (Alemanha).

### 4) A média e a mediana ficaram próximas ou distantes? O que isso sugere?
- **Média US$ 6.456,75** e **mediana US$ 6.150,00** — relativamente próximas, mas com a
  **média acima da mediana**. Isso indica **assimetria à direita**: a maioria ganha salários
  menores e poucos salários altos (diretoria) elevam a média. O **histograma** confirma isso.

### 5) O que o gráfico escolhido ajuda a entender? (explique um resultado)
- O **boxplot de salário por departamento** mostra, de uma vez, **mediana, dispersão e
  outliers**. Ele deixa claro que *Executive* está muito acima dos demais e que *Finance*,
  *IT* e *Purchasing* têm **outliers** (o gerente ganha muito mais que a equipe).
- O **boxplot por região** explica visualmente por que a *Americas* tem mediana baixa apesar
  dos salários altos da diretoria (que aparecem como **pontos fora da caixa**).

### 6) Principal insight e limitação para uma decisão de RH
- **Insight:** as diferenças de salário entre **regiões** são explicadas pelo **mix de cargos**
  de cada local (operacional x comercial x diretoria), e não por "país que paga mais".
- **Limitação:** a base **não tem senioridade, jornada nem custo de vida** por região. Portanto,
  esses números **não devem, sozinhos**, embasar decisões de reajuste ou contratação — servem
  como ponto de partida, exigindo dados complementares.

---

## Dica de fechamento
Mostre rapidamente que o projeto é **reprodutível**: `python gerar_dados.py` recria os CSV a
partir do SQL e `python analise.py` gera os gráficos — tudo versionado no GitHub.
