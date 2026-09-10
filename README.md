# mvp-engenharia-de-dados
MVP da disciplina Engenharia de Dados (40530010055_20260_01) – análise de fundos de investimento

🧩 Visão Geral
Este projeto implementa uma arquitetura Bronze → Silver → Gold para análise de fundos de investimento, utilizando Databricks e PySpark.
O objetivo é responder quatro perguntas de negócio relacionadas a risco, retorno, eficiência e categorias de fundos.

🏗️ Arquitetura do Projeto
Bronze — Dados Brutos
Ingestão dos dados originais de fundos.

Nenhuma transformação aplicada.

Apenas armazenamento fiel da fonte.

Silver — Dados Tratados
Limpeza e padronização dos dados.

Conversão de tipos.

Remoção de duplicatas.

Tratamento de nulos.

Normalização de colunas.

Preparação para análises.

Gold — Métricas e Modelagem
Criação das tabelas analíticas:

gold_risco_retorno

gold_sharpe_retorno

gold_categoria

gold_eficiencia

Cada tabela responde a uma pergunta de negócio.

📊 Perguntas Respondidas
1️⃣ Fundos com maior risco têm maior retorno?
Não.  
A correlação entre risco (desvio padrão) e retorno foi de 0.06, indicando ausência de relação linear forte.

2️⃣ O índice Sharpe é consistente com o retorno real?
Não diretamente.  
A correlação entre Sharpe e retorno foi de 0.03, mostrando que Sharpe mede eficiência, não retorno bruto.

3️⃣ Quais categorias têm melhor retorno ajustado ao risco?
A categoria Debt apresentou o melhor retorno ajustado ao risco, seguida por Hybrid.
A categoria Equity teve maior risco e menor retorno no período analisado.

4️⃣ O custo (expense_ratio) impacta negativamente o retorno?
Sim.  
Fundos com taxas menores (0.05–0.10) aparecem entre os mais eficientes.
Fundos com taxas acima de 1.0 raramente têm boa eficiência.

📁 Notebooks do Projeto
01_bronze_ingestao
Leitura dos dados brutos

Armazenamento em formato Delta

02_silver_tratamento
Limpeza

Padronização

Conversão de tipos

Preparação para análises

03_gold_modelagem_analises
Criação das tabelas Gold

Cálculo de métricas

Verificação de qualidade analítica

04_analises_relatorio_final
Cálculo das correlações

Análise das categorias

Avaliação da eficiência

Conclusões finais

📌 Conclusões Gerais
Risco não se traduz automaticamente em retorno.

Sharpe não mede retorno bruto, mas retorno ajustado ao risco.

Fundos de renda fixa (Debt) são mais eficientes no período analisado.

Custos mais altos reduzem a eficiência dos fundos.

🛠️ Tecnologias Utilizadas
Databricks

PySpark

Delta Lake

Spark SQL

Python
