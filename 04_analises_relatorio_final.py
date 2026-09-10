# Databricks notebook source
# ============================================================
# ETAPA 04 - ANÁLISES E RELATÓRIO FINAL
# ============================================================

# Ler as tabelas Gold

df_risco_retorno = spark.table("gold_risco_retorno")
df_sharpe_retorno = spark.table("gold_sharpe_retorno")
df_categoria = spark.table("gold_categoria")
df_eficiencia = spark.table("gold_eficiencia")

display(df_risco_retorno)


# COMMAND ----------

# ============================================================
# Análise 1: Risco x Retorno
# ============================================================
from pyspark.sql.functions import corr

cor_sd_ret = df_risco_retorno.select(corr("sd", "returns_1yr")).collect()[0][0]
print(f"Correlação risco x retorno (1 ano): {cor_sd_ret:.2f}")


# COMMAND ----------

# MAGIC %md
# MAGIC ### Interpretação — Risco x Retorno
# MAGIC A correlação entre risco (desvio padrão) e retorno foi de **0.06**, um valor extremamente baixo.
# MAGIC Isso indica que **não existe relação linear forte** entre risco e retorno no período analisado.
# MAGIC Ou seja, fundos mais arriscados **não necessariamente** entregaram retornos maiores.
# MAGIC

# COMMAND ----------

# ============================================================
# Análise 2: Sharpe x Retorno
# ============================================================
cor_sharpe_ret = df_sharpe_retorno.select(corr("sharpe", "returns_1yr")).collect()[0][0]
print(f"Correlação Sharpe x retorno (1 ano): {cor_sharpe_ret:.2f}")


# COMMAND ----------

# MAGIC %md
# MAGIC ### Interpretação — Sharpe x Retorno
# MAGIC A correlação entre Sharpe e retorno foi de **0.03**, praticamente zero.
# MAGIC Isso confirma que o índice Sharpe **não mede retorno bruto**, mas sim retorno ajustado ao risco.
# MAGIC Portanto, fundos com Sharpe alto não necessariamente têm retornos altos — eles têm **eficiência**, não magnitude.
# MAGIC

# COMMAND ----------

# ============================================================
# Análise 3: Categorias
# ============================================================
display(df_categoria.orderBy(df_categoria.avg_return_1yr.desc()))


# COMMAND ----------

# MAGIC %md
# MAGIC ### Interpretação — Categorias
# MAGIC A categoria **Debt** apresentou o melhor retorno ajustado ao risco, com:
# MAGIC - retorno médio de 5.54%
# MAGIC - desvio padrão muito baixo (2.09)
# MAGIC
# MAGIC A categoria **Hybrid** ficou em segundo lugar, com risco moderado e retorno razoável.
# MAGIC
# MAGIC A categoria **Equity** teve o maior risco (16.96) e o menor retorno médio (2.84%) no período analisado.
# MAGIC
# MAGIC A categoria **Other** é heterogênea e não apresentou bom desempenho ajustado ao risco.
# MAGIC
# MAGIC Conclusão: **Debt é a categoria mais eficiente**, seguida por Hybrid.
# MAGIC

# COMMAND ----------

# ============================================================
# Análise 4: Eficiência (Retorno / Custo)
# ============================================================
display(df_eficiencia.orderBy(df_eficiencia.eficiencia_1yr.desc()))


# COMMAND ----------

# MAGIC %md
# MAGIC ### Interpretação — Eficiência (Retorno / Custo)
# MAGIC Os fundos mais eficientes possuem **expense_ratio muito baixo** (entre 0.05 e 0.10).
# MAGIC Fundos com taxas acima de 1.0 raramente aparecem entre os mais eficientes.
# MAGIC
# MAGIC Isso mostra que **custos mais altos reduzem o retorno líquido**, confirmando impacto negativo do expense_ratio na eficiência.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC CONCLUSÕES DO MVP
# MAGIC
# MAGIC 1️⃣ Risco x Retorno
# MAGIC A correlação entre risco (sd) e retorno foi de apenas 0.06, indicando que fundos mais arriscados não apresentaram retornos maiores no período analisado.
# MAGIC
# MAGIC 2️⃣ Sharpe x Retorno
# MAGIC A correlação entre Sharpe e retorno foi de 0.03, mostrando que o índice Sharpe não está diretamente associado ao retorno bruto, mas sim ao retorno ajustado ao risco.
# MAGIC
# MAGIC 3️⃣ Categorias mais eficientes
# MAGIC A categoria Debt apresentou o melhor retorno ajustado ao risco, seguida por Hybrid. Equity teve maior risco e não compensou em retorno no período analisado.
# MAGIC
# MAGIC 4️⃣ Impacto do custo
# MAGIC Fundos com expense_ratio baixo (0.05–0.10) aparecem entre os mais eficientes. Fundos com taxas acima de 1.0 raramente apresentam boa eficiência. Custos mais altos reduzem o retorno líquido.
# MAGIC """)
# MAGIC