# Databricks notebook source
# Ler a tabela Bronze criada
df_bronze = spark.table("default.comprehensive_mutual_funds_data")

# Exibir as primeiras linhas
display(df_bronze)
