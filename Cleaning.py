# Databricks notebook source
df = spark.table("adnoc.raw.adnoc_stock_historical_data")

# COMMAND ----------

display(df)

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window
 
# To change date to date column
df.withColumn("Date", F.to_date("Date"))

# COMMAND ----------

#Round by 4 decimals
df = df.withColumn("Price_Change", F.round("Price_Change",4))
df = df.withColumn("Percentage_Change", F.round("Percentage_Change",4))
df = df.withColumn("Average_Price", F.round("Average_Price",4))
df = df.withColumn("Range", F.round("Range",4))

# COMMAND ----------

display(df)

# COMMAND ----------

# order by date

df = df.orderBy("Date")
display(df)

# COMMAND ----------

# Add a column for daily return
w = Window.orderBy("Date")
df = df.withColumn(
    "Daily_Return",
    F.round((F.col("Close") / F.lag("Close", 1).over(w)) - 1, 6)
)


# COMMAND ----------

#Divide date parts
df = (
    df.withColumn("Year", F.year("Date"))
      .withColumn("Month", F.month("Date"))
      .withColumn("DayOfWeek", F.date_format("Date", "E"))
)

# COMMAND ----------

display(df)

# COMMAND ----------

#flag if close > open and overnight gap
df = (
    df.withColumn("Is_Green", F.col("Close") > F.col("Open"))
      .withColumn("Gap", F.round(F.col("Open") - F.lag("Close", 1).over(w), 4))
)

# COMMAND ----------

display(df)

# COMMAND ----------

#moving averages, volatility, volume MA
w20 = Window.orderBy("Date").rowsBetween(-19, 0)
w50 = Window.orderBy("Date").rowsBetween(-49, 0)
w200 = Window.orderBy("Date").rowsBetween(-199, 0)
 
df = (
    df.withColumn("MA_20", F.round(F.avg("Close").over(w20), 4))
      .withColumn("MA_50", F.round(F.avg("Close").over(w50), 4))
      .withColumn("MA_200", F.round(F.avg("Close").over(w200), 4))
      .withColumn("Volatility_20d", F.round(F.stddev("Daily_Return").over(w20), 6))
      .withColumn("Volume_MA_20", F.round(F.avg("Volume").over(w20), 0))
)

# COMMAND ----------

display(df)

# COMMAND ----------

# Bollinger Bands
df = (
    df.withColumn("Close_STD_20", F.stddev("Close").over(w20))
      .withColumn("Bollinger_Upper", F.round(F.col("MA_20") + 2 * F.col("Close_STD_20"), 4))
      .withColumn("Bollinger_Lower", F.round(F.col("MA_20") - 2 * F.col("Close_STD_20"), 4))
      .drop("Close_STD_20")
)

# COMMAND ----------

#RSI
w14 = Window.orderBy("Date").rowsBetween(-13, 0)
 
df = df.withColumn("Gain", F.when(F.col("Daily_Return") > 0, F.col("Daily_Return")).otherwise(0))
df = df.withColumn("Loss", F.when(F.col("Daily_Return") < 0, -F.col("Daily_Return")).otherwise(0))
 

# COMMAND ----------


 
df = (
    df.withColumn("Avg_Gain_14", F.avg("Gain").over(w14))
      .withColumn("Avg_Loss_14", F.avg("Loss").over(w14))
      .withColumn(
          "RSI_14",
          F.round(100 - (100 / (1 + (F.col("Avg_Gain_14") / F.when(F.col("Avg_Loss_14") == 0, None).otherwise(F.col("Avg_Loss_14"))))), 2)
      )
      .drop("Gain", "Loss", "Avg_Gain_14", "Avg_Loss_14")
)
 

# COMMAND ----------

df.write.format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .saveAsTable("adnoc.clean.adnoc_stock_features")