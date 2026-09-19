# 📘 MVP – Engenharia de Dados  
Análise de fundos de investimento  
Disciplina: Engenharia de Dados (40530010055_20260_01)

---
## 🧠 Contexto de Negócios

Investidores e analistas precisam comparar fundos de investimento considerando não apenas o retorno histórico, mas também o risco assumido e os custos envolvidos. Decisões baseadas apenas em retorno bruto podem levar a escolhas ineficientes, especialmente quando taxas elevadas reduzem o ganho líquido ou quando o risco é desproporcional ao retorno.

Este MVP implementa um pipeline de dados na nuvem para organizar, tratar e analisar informações de fundos de investimento, permitindo avaliar relações entre risco, retorno, categoria e custo, de forma estruturada e reproduzível.

Problema: compreender como risco, retorno, categoria e custos se relacionam no desempenho dos fundos de investimento analisados.

---

## 🎯 Perguntas de Negócio (Objetivo do MVP)

Este projeto foi desenvolvido para responder **quatro perguntas fundamentais** sobre fundos de investimento:

1️⃣ **Fundos com maior risco têm maior retorno?**  
2️⃣ **O índice Sharpe é consistente com o retorno real?**  
3️⃣ **Quais categorias têm melhor retorno ajustado ao risco?**  
4️⃣ **O custo (expense_ratio) impacta negativamente o retorno?**

Essas perguntas orientam toda a arquitetura Bronze–Silver–Gold e justificam a escolha do dataset.

---
## 📁 Estrutura do Projeto

- mvp-engenharia-de-dados/ — diretório raiz do projeto

- data/ — pasta com os dados utilizados no MVP
  - comprehensive_mutual_funds_data.csv — dataset original dos fundos
  

- notebooks/ — pasta com os notebooks do pipeline
  - 01_bronze_ingestao_fundos.py — ingestão dos dados brutos (Bronze)
  - 02_silver_tratamento_fundos.py — limpeza e padronização (Silver)
  - 03_gold_modelagem_analises.py — métricas e modelagem (Gold)
  - 04_analises_relatorio_final.py — análises e conclusões finais
  
    
- evidencias/ - prints do pipeline
  
- README.md — documentação principal do projeto

## 📥 Coleta dos Dados

O dataset utilizado neste MVP é o **Comprehensive Mutual Funds Dataset**, disponível publicamente no Kaggle.

- **Origem:** Kaggle – *Comprehensive Mutual Funds Dataset*
- **URL:** https://www.kaggle.com/datasets/ravibarnawal/mutual-funds-india-detailed
- **Autor:** Comunidade Kaggle
- **Licença:** Open Data (uso permitido para fins educacionais)
- **Formato:** CSV
- **Registros:** ~1.800 fundos
- **Colunas:** 14 atributos financeiros (retorno, risco, categoria, taxa, etc.)

## 🧩 Visão Geral da Arquitetura
Este projeto implementa uma arquitetura **Bronze → Silver → Gold** para análise de fundos de investimento utilizando **Databricks + PySpark**.

O objetivo é responder quatro perguntas de negócio relacionadas a:

- risco  
- retorno  
- eficiência  
- categorias de fundos  

---
## 🏗️ Arquitetura do Projeto

### 🔶 Bronze — Dados Brutos
- Ingestão dos dados originais de fundos  
- Nenhuma transformação aplicada  
- Armazenamento fiel da fonte
- O arquivo CSV foi obtido do Kaggle e carregado no ambiente Databricks. A partir do arquivo disponibilizado no diretório de dados, o notebook 01_bronze_ingestao_fundos.py realizou a leitura e persistiu os dados na camada Bronze em formato Delta.  

---

### 🔷 Silver — Dados Tratados
- Limpeza e padronização  
- Conversão de tipos  
- Remoção de duplicatas  
- Tratamento de nulos  
- Normalização das colunas  
- Preparação para análises  

---
## 📊 Qualidade dos Dados — Dimensões, Problemas e Tratamentos

A camada Silver passou por uma análise completa de qualidade dos dados, garantindo consistência, completude e confiabilidade para as métricas da camada Gold. A tabela abaixo resume os principais problemas identificados, os tratamentos aplicados e o impacto direto na base.

| Dimensão          | Problema encontrado                               | Tratamento aplicado                     | Resultado / Impacto                                   |
|-------------------|---------------------------------------------------|------------------------------------------|--------------------------------------------------------|
| **Completude**    | Valores nulos em colunas críticas (`sortino`, `alpha`, `sd`, `beta`, `sharpe`, `returns_3yr`, `returns_5yr`) | Remoção ou manutenção conforme relevância analítica | **342 ocorrências tratadas** (somatório de nulos)      |
| **Unicidade**     | Possível duplicidade após ingestão                | `dropDuplicates()`                       | **0 duplicatas** na camada Silver                     |
| **Consistência**  | Categorias com nomenclaturas diferentes           | Padronização (`Debt`, `Equity`, `Hybrid`, `Other`) | Categorias normalizadas e prontas para agregações      |
| **Tipagem**       | Campos numéricos armazenados como texto           | Conversão para `double` / `integer`      | Dados numéricos prontos para cálculos estatísticos     |
| **Valores inválidos** | Presença de valores como `null`, `-0.1`, `-0.9` em retornos | Conversão para nulo ou marcação como outlier | **167 nulos em returns_5yr** tratados                  |
| **Outliers**      | Valores extremos em `sd`, `beta`, `sharpe`, `returns_1yr`, `returns_5yr` | Criação da coluna `is_outlier`           | **34 registros sinalizados** (4,18% da base Silver)    |

---

### ✔ Resultado geral dos tratamentos

Após os tratamentos aplicados:

- A base Silver ficou **consistente**, **padronizada** e **adequada para análises estatísticas**.  
- As métricas da camada Gold puderam ser calculadas sem erros.  
- As correlações e agregações passaram a refletir a realidade dos dados.  
- A marcação de outliers permitiu análises mais seguras, sem distorções.  


---

### 🟡 Gold — Métricas e Modelagem
Criação das tabelas analíticas:

- `gold_risco_retorno`
- `gold_sharpe_retorno`
- `gold_categoria`
- `gold_eficiencia`

Cada tabela responde diretamente a uma pergunta de negócio.

---
## 📚 Catálogo Técnico das Tabelas

### 🟤 Bronze — `comprehensive_mutual_funds_data`
**Descrição:**  
Tabela bruta contendo os dados originais dos fundos de investimento conforme disponibilizados no Kaggle.  
Sem transformações aplicadas, servindo como base para as camadas seguintes.

**Linhagem:**  
Fonte externa (Kaggle) → Bronze (Databricks Upload Manual)

| Coluna | Tipo | Descrição | Domínio / Observações |
|--------|------|------------|-----------------------|
| scheme_name | string | Nome do fundo de investimento | Texto livre |
| category | string | Categoria principal do fundo | Debt, Equity, Hybrid, Other |
| expense_ratio | double | Taxa de administração | 0–5% |
| returns_1yr | double | Retorno em 1 ano | -100% a +200% |
| returns_3yr | double | Retorno em 3 anos | -100% a +200% |
| returns_5yr | double | Retorno em 5 anos | -100% a +200% |
| fund_size_cr | double | Tamanho do fundo em crores | Numérico |
| fund_age_yr | double | Idade do fundo em anos | Numérico |
| rating | double | Classificação do fundo | Escala numérica |
| risk_level | string | Nível de risco | Baixo, Médio, Alto |

---

### ⚪ Silver — `fundos_silver`
**Descrição:**  
Tabela tratada e padronizada, contendo informações detalhadas sobre fundos, métricas de desempenho e indicadores de risco.  
Utilizada para análises comparativas e correlações entre risco, retorno e eficiência.

**Linhagem:**  
Bronze → Silver  
Transformações: limpeza de nulos, padronização de tipos, normalização de categorias, inclusão de campo `is_outlier`.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| scheme_name | string | Nome do fundo |
| min_sip | string | Valor mínimo para aplicação via SIP |
| min_lumpsum | string | Valor mínimo para aplicação única |
| expense_ratio | double | Taxa de administração |
| fund_size_cr | double | Tamanho do fundo |
| fund_age_yr | double | Idade do fundo |
| fund_manager | string | Gestor responsável |
| sortino | double | Índice Sortino |
| alpha | double | Alfa — desempenho ajustado ao benchmark |
| sd | double | Desvio padrão (volatilidade) |
| beta | double | Beta — sensibilidade ao mercado |
| sharpe | double | Índice Sharpe |
| risk_level | string | Nível de risco |
| amc_name | string | Administradora do fundo |
| rating | double | Classificação do fundo |
| category | string | Categoria principal |
| sub_category | string | Subcategoria |
| returns_1yr | double | Retorno em 1 ano |
| returns_3yr | double | Retorno em 3 anos |
| returns_5yr | double | Retorno em 5 anos |
| is_outlier | string | Indicador de outlier |

---

### 🟡 Gold — Tabelas Analíticas

#### `gold_risco_retorno`
**Descrição:**  
Tabela analítica que relaciona risco (desvio padrão) e retorno dos fundos.  
Base para responder à pergunta “Fundos com maior risco têm maior retorno?”.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| scheme_name | string | Nome do fundo |
| sd | double | Desvio padrão (risco) |
| returns_1yr | double | Retorno em 1 ano |
| categoria | string | Categoria do fundo |

**Linhagem:** Silver → Gold (cálculo de correlação risco-retorno)

---

#### `gold_sharpe_retorno`
**Descrição:**  
Tabela analítica que relaciona o índice Sharpe com o retorno real dos fundos.  
Base para avaliar eficiência versus retorno bruto.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| scheme_name | string | Nome do fundo |
| sharpe | double | Índice Sharpe |
| returns_1yr | double | Retorno em 1 ano |
| categoria | string | Categoria do fundo |

**Linhagem:** Silver → Gold (cálculo de correlação Sharpe-retorno)

---

#### `gold_categoria`
**Descrição:**  
Tabela que consolida o desempenho médio por categoria de fundo.  
Base para responder “Quais categorias têm melhor retorno ajustado ao risco?”.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| categoria | string | Categoria principal |
| retorno_medio | double | Retorno médio ajustado |
| risco_medio | double | Desvio padrão médio |
| eficiencia_media | double | Eficiência média calculada |

**Linhagem:** Silver → Gold (agregação por categoria)

---

#### `gold_eficiencia`
**Descrição:**  
Tabela que relaciona custo (expense_ratio) e eficiência dos fundos.  
Base para responder “O custo impacta negativamente o retorno?”.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| scheme_name | string | Nome do fundo |
| expense_ratio | double | Taxa de administração |
| eficiencia | double | Retorno ajustado ao custo |
| categoria | string | Categoria do fundo |

**Linhagem:** Silver → Gold (cálculo de eficiência e correlação custo-retorno)


---

## 📊 Resultado das Perguntas

### **1️⃣ Fundos com maior risco têm maior retorno?**
**Não.**  
A correlação entre risco (desvio padrão) e retorno foi de **0.06**, indicando ausência de relação linear forte.

---

### **2️⃣ O índice Sharpe é consistente com o retorno real?**
**Não diretamente.**  
A correlação entre Sharpe e retorno foi de **0.03**, mostrando que Sharpe mede eficiência, não retorno bruto.

---

### **3️⃣ Quais categorias têm melhor retorno ajustado ao risco?**
- **Debt** foi a categoria mais eficiente  
- **Hybrid** ficou em segundo lugar  
- **Equity** teve maior risco e menor retorno no período analisado  

---

### **4️⃣ O custo (expense_ratio) impacta negativamente o retorno?**
**Sim.**  
Fundos com taxas menores (0.05–0.10) aparecem entre os mais eficientes.  
Fundos com taxas acima de 1.0 raramente têm boa eficiência.

---


## 📁 Notebooks do Projeto

### `01_bronze_ingestao`
- Leitura dos dados brutos  
- Armazenamento em formato Delta  

### `02_silver_tratamento`
- Limpeza  
- Padronização  
- Conversão de tipos  
- Preparação para análises  

### `03_gold_modelagem_analises`
- Criação das tabelas Gold  
- Cálculo de métricas  
- Verificação de qualidade analítica  

### `04_analises_relatorio_final`
- Cálculo das correlações  
- Análise das categorias  
- Avaliação da eficiência  
- Conclusões finais  

---
## 📸 Evidências do MVP — Engenharia de Dados

Todas as imagens abaixo foram geradas durante a execução do pipeline no Databricks, documentando cada etapa da arquitetura **Bronze → Silver → Gold → Análises**.

---

### 🟤 Etapa Bronze — Ingestão dos Dados
Leitura e visualização inicial da tabela bruta.

![Tabela Bronze](./evidencias/01_databricks_comprehensive_mutual_funds_data.png)

---

### ⚪ Etapa Silver — Tratamento e Padronização
Transformação dos dados brutos em dados limpos e prontos para análise.

![Tabela Silver](./evidencias/02_silver.png)

---

### 🟡 Etapa Gold — Modelagem Analítica
Criação das tabelas analíticas com métricas de risco, retorno e eficiência.

![Gold - Sharpe x Retorno](./evidencias/03_gold_sharpe_retorno.png)
![Gold - Categoria](./evidencias/04_gold_categoria.png)
![Gold - Eficiência](./evidencias/05_gold_eficiencia.png)
![Gold - Risco x Retorno](./evidencias/06_gold_risco_retorno.png)

---

### 📚 Catálogo Completo
Visualização do schema `default` com todas as tabelas criadas.

![Catálogo Completo](./evidencias/07_catalogo_completo.png)

---

### ⚙️ Execução dos Notebooks
Evidências da execução das etapas do pipeline no Databricks.

![Notebook Bronze](./evidencias/08_notebook_bronze.png)
![Notebook Silver](./evidencias/09_notebook_silver.png)
![Notebook Gold](./evidencias/10_notebook_gold.png)
![Notebook Análises](./evidencias/11_notebook_analises_relatorio_final.png)

---

### 📊 Análises e Conclusões
Resultados das correlações e análises finais.

![Correlação Risco x Retorno](./evidencias/12_AN_correlacao_risco_retorno.png)
![Correlação Sharpe x Retorno](./evidencias/13_AN_correlacao_sharpe_retorno.png)

---

## 🧩 Conclusão Geral

O pipeline foi executado com sucesso, demonstrando a aplicação prática da arquitetura **Bronze–Silver–Gold** para análise de fundos de investimento.  
As evidências comprovam:
- ✅ Ingestão e padronização dos dados  
- ✅ Criação das tabelas analíticas  
- ✅ Execução completa dos notebooks  
- ✅ Análises quantitativas respondendo às perguntas de negócio  

O projeto documenta todo o processo de ponta a ponta e serve como referência para futuros trabalhos de engenharia de dados.


# 🧭 Autoavaliação

O MVP atingiu os principais objetivos propostos, permitindo implementar o pipeline e realizar análises sobre as quatro perguntas de negócio. Como limitações, destacam-se a ausência de automação, a utilização de uma única fonte de dados e a necessidade de ampliar as validações de qualidade e as visualizações


### 🚀 Possíveis evoluções futuras
- Implementar orquestração com Databricks Workflows ou Apache Airflow.
- Criar um modelo preditivo para estimar retorno ajustado ao risco.
- Adicionar testes automatizados para validação das transformações.
- Expandir o projeto para múltiplos datasets financeiros.

## 🛠️ Tecnologias Utilizadas
- Databricks  
- PySpark  
- Delta Lake  
- Spark SQL  
- Python  

---
