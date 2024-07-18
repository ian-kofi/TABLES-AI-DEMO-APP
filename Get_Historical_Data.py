
import pandas as pd
import NLP_INTENT_DETECTION
from datetime import datetime
from dateutil import parser
from database_connection import database_connection
import dateparser

input_key = None
user_query_tokens = None
df = None
revenue = None
profit = None



# Function to get the ISO format dates for a given quarter phrase
def get_quarter_dates(phrase):
    quarters = {
            "Q1": {"start": f"{datetime.today().year}-01-01", "end": f"{datetime.today().year}-03-31"},
            "Q2": {"start": f"{datetime.today().year}-04-01", "end": f"{datetime.today().year}-06-30"},
            "Q3": {"start": f"{datetime.today().year}-07-01", "end": f"{datetime.today().year}-09-30"},
            "Q4": {"start": f"{datetime.today().year}-10-01", "end": f"{datetime.today().year}-12-31"},
          }
    
    quarter_map = {
        "q1": "Q1",
        "quarter 1": "Q1",
        "first quarter": "Q1",
        "q2": "Q2",
        "quarter 2": "Q2",
        "second quarter": "Q2",
        "q3": "Q3",
        "quarter 3": "Q3",
        "third quarter": "Q3",
        "q4": "Q4",
        "quarter 4": "Q4",
        "fourth quarter": "Q4",
    }
    # Normalize the input phrase to lower case for matching
    phrase = phrase[0]
    phrase = phrase.lower()
    if phrase in quarter_map:
        quarter = quarter_map[phrase]
        return quarters[quarter]
    else:
        return None
        


def get_historical_data(user_query,input,prediction):
    global input_key, collection, df, profit, revenue,user_query_tokens
    
    input_key = input
    user_query_tokens = user_query
    print(f"INPUT KEY => {input_key}")
    # Convert to ISO 8601 format
    
    if any(key.upper() in ["quarter","Q1","Q2","Q3","Q4","q1","q2","q3","q4"] for key in input_key):
            date_list = get_quarter_dates(input_key)
            iso_format_date = list(date_list.values())
            print(f"date list for quarters: \n {date_list}")
    else:
        data = [dateparser.parse(i, languages=["en"]) for i in input_key ]
        iso_format_date = [item.isoformat() if item else None for item in data]
        iso_format_date = [datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').date() for s in iso_format_date]
    

        print(data)
    print(f"ISO FORMAT DATE LIST => {iso_format_date}")

    if len(input_key) == 2 or any (key.upper() in ["quarter","Q1","Q2","Q3","Q4","q1","q2","q3","q4"] for key in input_key):

        specified_date_1 = iso_format_date[0]
        specified_date_2 = iso_format_date[1]
        if prediction == NLP_INTENT_DETECTION.Search_Type.HISTORICAL_SALES:

            if "profit" in user_query_tokens or "profits" in user_query_tokens:
                profit = database_connection(prediction,identified_product=None,timeframe=[specified_date_1,specified_date_2],PoR="Profit")
                if profit.iloc[0,0] != None:
                    profit = format(round(profit.iloc[0,0],2),",")
                else:
                    profit = "0.0"
                return [profit, "PROFIT"]
            
            else:
                revenue = database_connection(prediction,identified_product=None,timeframe=[specified_date_1,specified_date_2],PoR="Revenue")
                if revenue.iloc[0,0] != None:
                    revenue = format(round(revenue.iloc[0,0],2),",")
                else:
                    revenue = "0.0"
                return [revenue, "REVENUE"]


    elif len(input_key) == 1 or any (key.upper() not in ["quarter","Q1","Q2","Q3","Q4","q1","q2","q3","q4"] for key in input_key):
        specified_date = iso_format_date[0]
        if prediction == NLP_INTENT_DETECTION.Search_Type.HISTORICAL_SALES:
            
            if "profit" in user_query_tokens or "profits" in user_query_tokens:
                profit = database_connection(prediction,identified_product=None,timeframe=specified_date,PoR="Profit")
                if profit.iloc[0,0] != None:
                    profit = format(round(profit.iloc[0,0],2),",")
                else:
                    profit = "0.0"  
                return [profit, "PROFIT"]

            else:
                revenue = database_connection(prediction,identified_product=None,timeframe=specified_date,PoR="Revenue")
                print(revenue)

                if revenue.iloc[0,0] != None:
                    revenue = format(round(revenue.iloc[0,0],2),",")
                else:
                    revenue = "0.0"

                return [revenue, "REVENUE"]