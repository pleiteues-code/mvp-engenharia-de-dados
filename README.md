# 📘 MVP – Engenharia de Dados  
Análise de fundos de investimento  
Disciplina: Engenharia de Dados (40530010055_20260_01)

---
## 🎯 Perguntas de Negócio (Objetivo do MVP)

Este projeto foi desenvolvido para responder **quatro perguntas fundamentais** sobre fundos de investimento:

1️⃣ **Fundos com maior risco têm maior retorno?**  
2️⃣ **O índice Sharpe é consistente com o retorno real?**  
3️⃣ **Quais categorias têm melhor retorno ajustado ao risco?**  
4️⃣ **O custo (expense_ratio) impacta negativamente o retorno?**

Essas perguntas orientam toda a arquitetura Bronze–Silver–Gold e justificam a escolha do dataset.

---

## 📂 Dataset Utilizado

O dataset escolhido contém informações de fundos de investimento, incluindo:

- nome do fundo (`scheme_name`)  
- categoria (`category`)  
- taxa de administração (`expense_ratio`)  
- retorno em 1 ano (`returns_1yr`)  
- métricas calculadas (Sharpe, risco, eficiência)

### ✔ Por que este dataset foi escolhido?

- Ele possui **variáveis essenciais** para análises de risco, retorno e eficiência.  
- Permite calcular métricas financeiras clássicas (Sharpe, desvio padrão, retorno ajustado ao risco).  
- Contém **categorias distintas** (Debt, Equity, Hybrid, Other), possibilitando comparações.  
- É um dataset **simples, limpo e adequado para um MVP**, sem necessidade de grandes integrações externas.  
- Permite responder diretamente às quatro perguntas de negócio da disciplina.

---

## 🧩 Visão Geral
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

---

### 🔷 Silver — Dados Tratados
- Limpeza e padronização  
- Conversão de tipos  
- Remoção de duplicatas  
- Tratamento de nulos  
- Normalização das colunas  
- Preparação para análises  

---

### 🟡 Gold — Métricas e Modelagem
Criação das tabelas analíticas:

- `gold_risco_retorno`
- `gold_sharpe_retorno`
- `gold_categoria`
- `gold_eficiencia`

Cada tabela responde diretamente a uma pergunta de negócio.

---

## 📊 Perguntas Respondidas

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

## 📌 Conclusões Gerais
- Risco não se traduz automaticamente em retorno  
- Sharpe mede eficiência, não retorno bruto  
- Fundos de renda fixa (Debt) foram os mais eficientes  
- Custos mais altos reduzem a eficiência dos fundos  
---

## 🧭 Autoavaliação

- Todas as perguntas de negócio foram respondidas com base nas tabelas Gold.  
- A arquitetura Bronze–Silver–Gold foi implementada corretamente.  
- O dataset escolhido foi adequado ao escopo do MVP.  
- A limpeza e padronização dos dados foram suficientes para garantir qualidade analítica.  
- A ausência de gráficos não prejudicou a interpretação dos resultados.  
- Caso o projeto fosse evoluído, eu adicionaria:
  - automação do pipeline  
  - dashboards visuais  
  - ingestão contínua  
  - mais fontes de dados  
---

## 🛠️ Tecnologias Utilizadas
- Databricks  
- PySpark  
- Delta Lake  
- Spark SQL  
- Python  

---

