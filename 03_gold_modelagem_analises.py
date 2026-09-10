# Databricks notebook source
# ============================================================
# ETAPA GOLD - MODELAGEM E ANÁLISES
# Objetivo: criar tabelas analíticas que respondem às perguntas
# do MVP usando os dados limpos da camada Silver.
# ============================================================

# ------------------------------------------------------------
# 1. Ler a tabela Silver
# ------------------------------------------------------------
df_silver = spark.table("fundos_silver")

display(df_silver)


# COMMAND ----------

# ------------------------------------------------------------
# 2. GOLD: Risco x Retorno
# ------------------------------------------------------------

df_risco_retorno = df_silver.select(
    "scheme_name", "category", "sub_category",
    "sd", "beta", "sortino",
    "returns_1yr", "returns_3yr", "returns_5yr"
)

display(df_risco_retorno)

df_risco_retorno.write.format("delta").mode("overwrite").saveAsTable("gold_risco_retorno")


# COMMAND ----------

# ------------------------------------------------------------
# 3. GOLD: Sharpe x Retorno
# ------------------------------------------------------------

df_sharpe_retorno = df_silver.select(
    "scheme_name", "category", "sharpe",
    "returns_1yr", "returns_3yr", "returns_5yr"
)

display(df_sharpe_retorno)

df_sharpe_retorno.write.format("delta").mode("overwrite").saveAsTable("gold_sharpe_retorno")


# COMMAND ----------

# ------------------------------------------------------------
# 4. GOLD: Análise por categoria
# ------------------------------------------------------------

from pyspark.sql.functions import avg

df_categoria = df_silver.groupBy("category").agg(
    avg("returns_1yr").alias("avg_return_1yr"),
    avg("returns_3yr").alias("avg_return_3yr"),
    avg("returns_5yr").alias("avg_return_5yr"),
    avg("sd").alias("avg_sd"),
    avg("beta").alias("avg_beta"),
    avg("sortino").alias("avg_sortino")
)

display(df_categoria)

df_categoria.write.format("delta").mode("overwrite").saveAsTable("gold_categoria")


# COMMAND ----------

# ------------------------------------------------------------
# 5. GOLD: Eficiência (Retorno / Custo)
# ------------------------------------------------------------

from pyspark.sql.functions import col, when

# Garantir que as colunas estão em DOUBLE
df_silver = df_silver.withColumn("returns_1yr", col("returns_1yr").cast("double"))
df_silver = df_silver.withColumn("expense_ratio", col("expense_ratio").cast("double"))

# Calcular eficiência, evitando divisão por zero
df_eficiencia = df_silver.select(
    "scheme_name", "category", "expense_ratio",
    "returns_1yr",
    when(col("expense_ratio") == 0, None)  # evita erro de divisão por zero
    .otherwise(col("returns_1yr") / col("expense_ratio"))
    .alias("eficiencia_1yr")
)

display(df_eficiencia)

df_eficiencia.write.format("delta").mode("overwrite").saveAsTable("gold_eficiencia")


# COMMAND ----------

# ============================================================
# VERIFICAÇÃO GOLD - Tabelas criadas corretamente
# ============================================================

tabelas = spark.catalog.listTables("default")
for t in tabelas:
    print(f"{t.name} - {t.tableType}")


# COMMAND ----------

# ============================================================
# VERIFICAÇÃO GOLD - Quantidade de registros
# ============================================================

print("gold_risco_retorno:", spark.table("gold_risco_retorno").count())
print("gold_sharpe_retorno:", spark.table("gold_sharpe_retorno").count())
print("gold_categoria:", spark.table("gold_categoria").count())
print("gold_eficiencia:", spark.table("gold_eficiencia").count())


# COMMAND ----------

# ============================================================
# VERIFICAÇÃO GOLD - Estrutura das tabelas
# ============================================================

print("Schema gold_risco_retorno:")
spark.table("gold_risco_retorno").printSchema()

print("\nSchema gold_sharpe_retorno:")
spark.table("gold_sharpe_retorno").printSchema()

print("\nSchema gold_categoria:")
spark.table("gold_categoria").printSchema()

print("\nSchema gold_eficiencia:")
spark.table("gold_eficiencia").printSchema()


# COMMAND ----------

# ============================================================
# VERIFICAÇÃO GOLD - Correlação risco x retorno
# ============================================================

from pyspark.sql.functions import corr

df_risco = spark.table("gold_risco_retorno")
cor_sd_ret = df_risco.select(corr("sd", "returns_1yr")).collect()[0][0]

print(f"Correlação sd x retorno (1 ano): {cor_sd_ret:.2f}")


# COMMAND ----------

# ============================================================
# VERIFICAÇÃO GOLD - Correlação sharpe x retorno
# ============================================================

df_sharpe = spark.table("gold_sharpe_retorno")
cor_sharpe_ret = df_sharpe.select(corr("sharpe", "returns_1yr")).collect()[0][0]

print(f"Correlação sharpe x retorno (1 ano): {cor_sharpe_ret:.2f}")


# COMMAND ----------

# ============================================================
# VERIFICAÇÃO GOLD - Ranking de categorias por retorno
# ============================================================

df_cat = spark.table("gold_categoria")
display(df_cat.orderBy(df_cat.avg_return_1yr.desc()))


# COMMAND ----------

# ============================================================
# VERIFICAÇÃO GOLD - Eficiência dos fundos
# ============================================================

df_efi = spark.table("gold_eficiencia")
display(df_efi.orderBy(df_efi.eficiencia_1yr.desc()))
