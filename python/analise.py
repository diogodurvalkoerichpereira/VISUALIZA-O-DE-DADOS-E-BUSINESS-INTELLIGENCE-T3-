# -*- coding: utf-8 -*-
"""
analise.py
==========
Analise Exploratoria de Dados (EDA) do projeto de Visualizacao de Dados e
Business Intelligence [T3] - base Human Resources (HR) do FreeSQL.

O script:
  1. Importa os dois CSV extraidos das consultas SQL (dados/query_01.csv e
     dados/query_02.csv).
  2. Faz uma EDA simples: estrutura, tipos, valores ausentes, primeiras linhas.
  3. Calcula as medidas estatisticas basicas (media, mediana, minimo, maximo,
     desvio-padrao e quartis) dos salarios.
  4. Compara salarios por DEPARTAMENTO, por CARGO e por REGIAO.
  5. Gera os graficos (histograma, boxplots e barras) na pasta graficos/.

Execucao:
    python analise.py
(Rode antes o gerar_dados.py caso os CSV ainda nao existam.)
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sem interface grafica (gera arquivos PNG)
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Configuracoes gerais
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, "dados")
GRAF_DIR = os.path.join(BASE_DIR, "graficos")
os.makedirs(GRAF_DIR, exist_ok=True)

ACENTO = "#3b6ea5"        # azul principal
ACENTO2 = "#c44e52"       # vermelho (linha de referencia / destaque)
ACENTO3 = "#55a868"       # verde (segundo grupo)
plt.rcParams.update({
    "figure.dpi": 120,
    "savefig.dpi": 120,
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def brl(x):
    """Formata um numero como valor monetario simples (US$, base salarial da HR)."""
    return "US$ {:,.2f}".format(x)


# Compatibilidade entre versoes do matplotlib para o boxplot:
# os argumentos 'labels'/'vert' foram substituidos por 'tick_labels'/'orientation'
# nas versoes 3.9/3.10. O helper abaixo escolhe o argumento certo para a versao
# instalada, funcionando tanto em matplotlib antigo (>=3.7) quanto no atual.
_MPL = tuple(int(p) for p in matplotlib.__version__.split(".")[:2])


def boxplot_compat(ax, dados, rotulos, horizontal):
    kw = dict(patch_artist=True, medianprops=dict(color=ACENTO2, linewidth=2))
    kw["tick_labels" if _MPL >= (3, 9) else "labels"] = rotulos
    if _MPL >= (3, 10):
        kw["orientation"] = "horizontal" if horizontal else "vertical"
    else:
        kw["vert"] = not horizontal
    return ax.boxplot(dados, **kw)


# ===========================================================================
# 1) IMPORTACAO DOS DADOS
# ===========================================================================
titulo("1) IMPORTACAO DOS ARQUIVOS CSV")
df1 = pd.read_csv(os.path.join(DADOS_DIR, "query_01.csv"))
df2 = pd.read_csv(os.path.join(DADOS_DIR, "query_02.csv"))
print("query_01.csv (Salario por Departamento e Cargo):", df1.shape[0], "linhas x", df1.shape[1], "colunas")
print("query_02.csv (Funcionarios por Regiao)         :", df2.shape[0], "linhas x", df2.shape[1], "colunas")

# ===========================================================================
# 2) ANALISE EXPLORATORIA (EDA)
# ===========================================================================
titulo("2) EDA - ESTRUTURA E QUALIDADE DOS DADOS")
print(">> Primeiras linhas de query_01 (Salario por Departamento e Cargo):")
print(df1.head(), "\n")
print(">> Tipos de dados (query_01):")
print(df1.dtypes, "\n")
print(">> Valores ausentes por coluna (query_01):")
print(df1.isna().sum(), "\n")
print(">> Valores ausentes por coluna (query_02):")
print(df2.isna().sum())

# ===========================================================================
# 3) MEDIDAS ESTATISTICAS BASICAS (SALARIO)
# ===========================================================================
titulo("3) MEDIDAS ESTATISTICAS BASICAS - SALARIO (query_01)")
sal = df1["SALARY"]
media = sal.mean()
mediana = sal.median()
minimo = sal.min()
maximo = sal.max()
desvio = sal.std()
q1, q3 = sal.quantile(0.25), sal.quantile(0.75)

print("Quantidade de funcionarios : {}".format(sal.count()))
print("Media   (mean)             : {}".format(brl(media)))
print("Mediana (median)           : {}".format(brl(mediana)))
print("Minimo  (min)              : {}".format(brl(minimo)))
print("Maximo  (max)              : {}".format(brl(maximo)))
print("Desvio-padrao (std)        : {}".format(brl(desvio)))
print("1o quartil (Q1)            : {}".format(brl(q1)))
print("3o quartil (Q3)            : {}".format(brl(q3)))
print("\nResumo estatistico (describe):")
print(sal.describe())
print("\nLeitura: media ({}) > mediana ({}) => distribuicao assimetrica a direita\n"
      "(poucos salarios muito altos - diretoria e gerencia - puxam a media para cima)."
      .format(brl(media), brl(mediana)))

# ===========================================================================
# 4) COMPARACOES POR DEPARTAMENTO, CARGO E REGIAO
# ===========================================================================
titulo("4a) SALARIO MEDIO / MEDIANO POR DEPARTAMENTO (query_01)")
por_depto = (df1.groupby("DEPARTMENT_NAME")["SALARY"]
             .agg(funcionarios="count", media="mean", mediana="median",
                  minimo="min", maximo="max")
             .sort_values("media", ascending=False)
             .round(2))
print(por_depto)

titulo("4b) SALARIO MEDIO POR CARGO (query_01) - TOP 5 e BOTTOM 5")
por_cargo = (df1.groupby("JOB_TITLE")["SALARY"]
             .agg(funcionarios="count", media="mean")
             .sort_values("media", ascending=False)
             .round(2))
print(">> Maiores medias:")
print(por_cargo.head(5))
print("\n>> Menores medias:")
print(por_cargo.tail(5))

titulo("4c) FUNCIONARIOS E SALARIO POR REGIAO (query_02)")
por_regiao = (df2.groupby("REGION_NAME")["SALARY"]
              .agg(funcionarios="count", media="mean", mediana="median",
                   minimo="min", maximo="max")
              .sort_values("funcionarios", ascending=False)
              .round(2))
print(por_regiao)

titulo("4d) FUNCIONARIOS E SALARIO POR PAIS (query_02)")
por_pais = (df2.groupby("COUNTRY_NAME")["SALARY"]
            .agg(funcionarios="count", media="mean")
            .sort_values("funcionarios", ascending=False)
            .round(2))
print(por_pais)

# ===========================================================================
# 5) GRAFICOS
# ===========================================================================
titulo("5) GERACAO DOS GRAFICOS (pasta graficos/)")

# --- 5.1 Histograma da distribuicao de salarios --------------------------
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.hist(sal, bins=15, color=ACENTO, edgecolor="white", alpha=0.9)
ax.axvline(media, color=ACENTO2, linestyle="--", linewidth=2,
           label="Media = {}".format(brl(media)))
ax.axvline(mediana, color="#333333", linestyle=":", linewidth=2,
           label="Mediana = {}".format(brl(mediana)))
ax.set_title("Distribuicao dos salarios (base HR - {} funcionarios)".format(sal.count()),
             fontweight="bold")
ax.set_xlabel("Salario (US$)")
ax.set_ylabel("Quantidade de funcionarios")
ax.legend()
fig.tight_layout()
f_hist = os.path.join(GRAF_DIR, "histograma_salarios.png")
fig.savefig(f_hist)
plt.close(fig)
print("[ok]", os.path.relpath(f_hist, BASE_DIR))

# --- 5.2 Boxplot de salario por departamento -----------------------------
ordem = (df1.groupby("DEPARTMENT_NAME")["SALARY"].median()
         .sort_values().index.tolist())
dados_box = [df1.loc[df1["DEPARTMENT_NAME"] == d, "SALARY"].values for d in ordem]
fig, ax = plt.subplots(figsize=(10, 6))
bp = boxplot_compat(ax, dados_box, ordem, horizontal=True)
for caixa in bp["boxes"]:
    caixa.set(facecolor=ACENTO, alpha=0.6)
ax.set_title("Salario por departamento (ordenado pela mediana)", fontweight="bold")
ax.set_xlabel("Salario (US$)")
ax.set_ylabel("Departamento")
fig.tight_layout()
f_box_dep = os.path.join(GRAF_DIR, "boxplot_salario_departamento.png")
fig.savefig(f_box_dep)
plt.close(fig)
print("[ok]", os.path.relpath(f_box_dep, BASE_DIR))

# --- 5.3 Barras: salario medio por departamento --------------------------
media_dep = df1.groupby("DEPARTMENT_NAME")["SALARY"].mean().sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
barras = ax.barh(media_dep.index, media_dep.values, color=ACENTO, alpha=0.9)
for b, v in zip(barras, media_dep.values):
    ax.text(v + 150, b.get_y() + b.get_height() / 2, "{:,.0f}".format(v),
            va="center", fontsize=9)
ax.set_title("Salario medio por departamento", fontweight="bold")
ax.set_xlabel("Salario medio (US$)")
ax.set_ylabel("Departamento")
ax.margins(x=0.12)
fig.tight_layout()
f_bar_dep = os.path.join(GRAF_DIR, "barras_media_salario_departamento.png")
fig.savefig(f_bar_dep)
plt.close(fig)
print("[ok]", os.path.relpath(f_bar_dep, BASE_DIR))

# --- 5.4 Boxplot de salario por regiao -----------------------------------
ordem_reg = (df2.groupby("REGION_NAME")["SALARY"].median()
             .sort_values().index.tolist())
dados_reg = [df2.loc[df2["REGION_NAME"] == r, "SALARY"].values for r in ordem_reg]
fig, ax = plt.subplots(figsize=(8, 5))
bp = boxplot_compat(ax, dados_reg, ordem_reg, horizontal=False)
for caixa in bp["boxes"]:
    caixa.set(facecolor=ACENTO3, alpha=0.6)
ax.set_title("Distribuicao salarial por regiao", fontweight="bold")
ax.set_xlabel("Regiao")
ax.set_ylabel("Salario (US$)")
fig.tight_layout()
f_box_reg = os.path.join(GRAF_DIR, "boxplot_salario_regiao.png")
fig.savefig(f_box_reg)
plt.close(fig)
print("[ok]", os.path.relpath(f_box_reg, BASE_DIR))

# --- 5.5 Barras: numero de funcionarios por regiao -----------------------
cont_reg = df2["REGION_NAME"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
barras = ax.bar(cont_reg.index, cont_reg.values, color=ACENTO, alpha=0.9)
for b, v in zip(barras, cont_reg.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.5, str(v), ha="center", fontsize=10)
ax.set_title("Numero de funcionarios por regiao", fontweight="bold")
ax.set_xlabel("Regiao")
ax.set_ylabel("Quantidade de funcionarios")
ax.margins(y=0.12)
fig.tight_layout()
f_bar_reg = os.path.join(GRAF_DIR, "barras_funcionarios_regiao.png")
fig.savefig(f_bar_reg)
plt.close(fig)
print("[ok]", os.path.relpath(f_bar_reg, BASE_DIR))

titulo("ANALISE CONCLUIDA")
print("5 graficos salvos em graficos/. Resumo dos principais numeros no README.md.")
