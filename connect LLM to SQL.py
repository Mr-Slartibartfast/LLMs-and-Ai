import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=TestDB;Trusted_Connection=yes;"
)

def run_query(query):
    return pd.read_sql(query, conn)

print(run_query("SELECT TOP 10 * FROM metrics"))