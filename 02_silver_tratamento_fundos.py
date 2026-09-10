# Databricks notebook source
# ============================================================
# ETAPA SILVER - TRATAMENTO DOS DADOS
# Objetivo: transformar os dados brutos (Bronze) em dados limpos,
# padronizados e prontos para análises na camada Gold.
# ============================================================

# ------------------------------------------------------------
# 1. Ler a tabela Bronze
# ------------------------------------------------------------
df_silver = spark.table("default.comprehensive_mutual_funds_data")

display(df_silver)

# ------------------------------------------------------------
# 2. Substituir valores '-' por NULL
# Motivo: '-' impede conversão para tipos numéricos.
# ------------------------------------------------------------
df_silver = df_silver.replace('-', None)


# ------------------------------------------------------------
# 3. Converter colunas numéricas
# Motivo: Spark lê tudo como string inicialmente.
# Precisamos converter para double para análises futuras.
# ------------------------------------------------------------

from pyspark.sql.functions import col

numeric_cols = [
    "min_sip", "min_lumpsum", "expense_ratio", "fund_size_cr", "fund_age_yr",
    "sortino", "alpha", "sd", "beta", "sharpe",
    "returns_1yr", "returns_3yr", "returns_5yr"
]

for c in numeric_cols:
    df_silver = df_silver.withColumn(c, col(c).cast("double"))

# ------------------------------------------------------------
# 4. Padronizar categorias
# Motivo: categorias vêm com variações (Equity, Equity Fund, etc.)
# Queremos apenas: Equity, Debt, Hybrid, Other
# ------------------------------------------------------------

from pyspark.sql.functions import when

df_silver = df_silver.withColumn(
    "category",
    when(col("category").rlike("(?i)equity"), "Equity")
    .when(col("category").rlike("(?i)debt"), "Debt")
    .when(col("category").rlike("(?i)hybrid"), "Hybrid")
    .otherwise("Other")
)

# ------------------------------------------------------------
# 5. Preencher nulos em colunas categóricas
# Motivo: facilita agrupamentos e evita erros na Gold.
# ------------------------------------------------------------

categorical_cols = ["fund_manager", "amc_name", "sub_category"]

for c in categorical_cols:
    df_silver = df_silver.withColumn(
        c,
        when(col(c).isNull(), "Unknown").otherwise(col(c))
    )

# ------------------------------------------------------------
# 6. Criar flag de outliers
# Motivo: beta negativo e sd muito alto são inconsistências.
# Não removemos — apenas marcamos para análise futura.
# ------------------------------------------------------------

df_silver = df_silver.withColumn(
    "is_outlier",
    when(col("beta") < 0, True)
    .when(col("sd") > 50, True)
    .otherwise(False)
)

# ------------------------------------------------------------
# 7. Remover duplicatas
# ------------------------------------------------------------
df_silver = df_silver.dropDuplicates()

# ------------------------------------------------------------
# 8. Remover espaços extras
# Motivo: alguns campos vêm com espaços no início/fim.
# ------------------------------------------------------------

from pyspark.sql.functions import trim

df_silver = df_silver.select([trim(col(c)).alias(c) for c in df_silver.columns])

# ------------------------------------------------------------
# 9. Verificação de qualidade dos dados
# 
# ------------------------------------------------------------

# Estatísticas das colunas numéricas
display(df_silver.describe())

# Contagem de nulos por coluna
null_counts = df_silver.select([
    col(c).isNull().alias(c) for c in df_silver.columns
])
display(null_counts)

# ------------------------------------------------------------
# 10. Salvar tabela Silver em formato Delta
# ------------------------------------------------------------
df_silver.write.format("delta").mode("overwrite").saveAsTable("default.fundos_silver")

# ------------------------------------------------------------
# 11. Validar tabela Silver
# ------------------------------------------------------------


display(spark.table("default.fundos_silver"))
