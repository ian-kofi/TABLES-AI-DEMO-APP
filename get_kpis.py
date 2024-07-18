import plotly.express as px
import pandas as pd
import numpy as np
from database_connection import database_connection


def get_kpi(report_type,timeframe):
    match report_type:
        case "SALES_REPORT":
            df = database_connection(report_type,None,timeframe,None)

            if not df.empty:
#------------------------------------------------------------- TOP KPI'S --------------------------------------------------------------------------------
        #TOTAL REVENUE----------------------------------------------------------------------------------------------------        
                total_qty_per_product = df.groupby("ITEM")["QTY"].sum()
                total_revenue = int(df["TOTAL SELLING PRICE"].sum())
    
        #PROFIT----------------------------------------------------------------------------------------------------------- 
                total_cost_price = int(df["TOTAL COST PRICE"].sum())
                total_sales = int(df["TOTAL SELLING PRICE"].sum())
                total_profit = total_sales - total_cost_price
    
        #TOP SELLING------------------------------------------------------------------------------------------------------
                top_selling_product = total_qty_per_product.idxmax()
                total_qty_per_product = int(total_qty_per_product.max())




                return total_revenue, total_profit, top_selling_product, total_qty_per_product, df

            elif df.empty:
                return df