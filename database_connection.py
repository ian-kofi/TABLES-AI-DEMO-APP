import sqlalchemy
import pandas as pd
import NLP_INTENT_DETECTION, INTENT_DETECTION_FOR_REPORTS
from sqlalchemy import create_engine
import streamlit as st
import dateparser
from datetime import datetime



engine = create_engine('mysql+pymysql://root:iankofiaddo_db@localhost:3306/demo_db')


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
    
@st.cache_data
def database_connection(prediction,identified_product=None,timeframe=None,PoR=None, ranking_value=None, measurement=None):
    print("connecting to db.....")
    with engine.connect() as connection:
        metadata = sqlalchemy.MetaData()
        result = None
        
        
        match prediction:
#COST PRICE OR SELLING PRICE LOGIC--------------------------------------------------------------------------------------------------------------------------------------------------------------
            case NLP_INTENT_DETECTION.Search_Type.COST_PRICE | NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE if measurement:
                print("measurement found")
                productinfo = sqlalchemy.Table("product_info",metadata,autoload_with=engine)
                identified_product = f"{identified_product}%".upper()
                measurement = f"{measurement[0]}%".upper()
                print(measurement)
                print(identified_product)
                match prediction:
                    case NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE:
                        print("executing query")
                        query = sqlalchemy.select(productinfo.c["ITEMS"], productinfo.c["SELLING PRICE"]).where(productinfo.columns.ITEMS.like (identified_product), productinfo.columns.MEASUREMENT.like (measurement))

                    case NLP_INTENT_DETECTION.Search_Type.COST_PRICE:
                        print("executing query")
                        query = sqlalchemy.select(productinfo.c["ITEMS"], productinfo.c["COST PRICE"]).where(productinfo.columns.ITEMS.like (identified_product), productinfo.columns.MEASUREMENT.like (measurement) )
                        
                
                exe = connection.execute(query)
                result = pd.DataFrame(exe.fetchall())


            case NLP_INTENT_DETECTION.Search_Type.COST_PRICE | NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE if not measurement:
                productinfo = sqlalchemy.Table("product_info",metadata,autoload_with=engine)
                identified_product = f"{identified_product}%".upper()

                match prediction:
                    case NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE:
                        query = sqlalchemy.select(productinfo.c["ITEMS"], productinfo.c["SELLING PRICE"]).where(productinfo.columns.ITEMS.like (identified_product))

                    case NLP_INTENT_DETECTION.Search_Type.COST_PRICE:
                        query = sqlalchemy.select(productinfo.c["ITEMS"], productinfo.c["COST PRICE"]).where(productinfo.columns.ITEMS.like (identified_product))
                        
                
                exe = connection.execute(query)
                result = pd.DataFrame(exe.fetchall())
                    

# HISTORICAL SALES LOGIC--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            case NLP_INTENT_DETECTION.Search_Type.HISTORICAL_SALES:
                salestable = sqlalchemy.Table("sales_demo",metadata,autoload_with=engine)
                
                match PoR:
                    case "Profit":
                        print(f"timeframe for profit => {timeframe}")
                        match isinstance(timeframe,list):
                            case False:
                                query = sqlalchemy.select(sqlalchemy.func.sum(salestable.c["TOTAL PROFIT"])).where(salestable.columns.DATE == (timeframe))
                            case True:
                                query = sqlalchemy.select(sqlalchemy.func.sum(salestable.c["TOTAL PROFIT"])).where(salestable.columns.DATE.between((timeframe[0]),(timeframe[1])) )
                       
                    case "Revenue":
                        print(f"timeframe for revenue => {timeframe}")
                        match isinstance(timeframe,list):
                            case False:
                                query = sqlalchemy.select(sqlalchemy.func.sum(salestable.c["TOTAL SELLING PRICE"])).where(salestable.columns.DATE == (timeframe))
                            case True:
                                query = sqlalchemy.select(sqlalchemy.func.sum(salestable.c["TOTAL SELLING PRICE"])).where(salestable.columns.DATE.between((timeframe[0]),(timeframe[1])))

                exe = connection.execute(query)  
                result = pd.DataFrame(exe.fetchall())  


# RANKING LOGIC-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
            case NLP_INTENT_DETECTION.Search_Type.RANKING:
                salestable = sqlalchemy.Table("sales_demo",metadata,autoload_with=engine)
                print("in db connection")
                identified_product = f"{identified_product[0]}".upper()
                print(f" => {identified_product}\n and {timeframe}")

                if ranking_value is None:
                    if timeframe is None:
                        match identified_product:
                            case "QUANTITY" | "VOLUME" | "QTY" | "AMOUNT" | "UNITS SOLD" | "SALES VOLUME":
                                query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['QTY']).label('total quantity')).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total quantity")).limit(10)   
                                exe = connection.execute(query)  
                                result = pd.DataFrame(exe.fetchall())  
                            case "REVENUE" | "SALES" | "TOTAL SALES" | "GROSS REVENUE":
                                query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL SELLING PRICE']).label('total revenue')).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total revenue")).limit(10)   
                                result = connection.execute(query).fetchall() 
                                formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                result = pd.DataFrame(formatted_results, columns=["Item","Total Revenue"])
                            case "PROFIT" | "PROFITS":
                                query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL PROFIT']).label('total profit')).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total profit")).limit(10)   
                                result = connection.execute(query).fetchall() 
                                formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                result = pd.DataFrame(formatted_results, columns=["Item","Total Profit"])

                    else:
                        if any(key.upper() in ["quarter","Q1","Q2","Q3","Q4","q1","q2","q3","q4"] for key in timeframe):
                            date_list = get_quarter_dates(list(timeframe))
                            iso_format_date = list(date_list.values())
                            print(f"date list for quarters: \n {date_list}")
                            print(f"formated date = > {iso_format_date}")
                        else:
                            data = [dateparser.parse(i, languages=["en"]) for i in timeframe ]
                            iso_format_date = [item.isoformat() if item else None for item in data]
                            iso_format_date = [datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').date() for s in iso_format_date]
                            print(f"formatted date {iso_format_date}")
                        if len(iso_format_date) == 1:
                            specified_date = iso_format_date[0]
                            match identified_product:
                                case "QUANTITY" | "VOLUME" | "QTY" | "AMOUNT" | "UNITS SOLD" | "SALES VOLUME":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['QTY']).label('total quantity')).where(salestable.columns.DATE == (specified_date)).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total quantity")).limit(10)   
                                    exe = connection.execute(query)  
                                    result = pd.DataFrame(exe.fetchall())  
                                case "REVENUE" | "SALES" | "TOTAL SALES" | "GROSS REVENUE":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL SELLING PRICE']).label('total revenue')).where(salestable.columns.DATE == (specified_date)).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total revenue")).limit(10)   
                                    result = connection.execute(query).fetchall() 
                                    formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                    result = pd.DataFrame(formatted_results, columns=["Item","Total Revenue"])
                                case "PROFIT" | "PROFITS":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL PROFIT']).label('total profit')).where(salestable.columns.DATE == (specified_date)).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total profit")).limit(10)   
                                    result = connection.execute(query).fetchall() 
                                    formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                    result = pd.DataFrame(formatted_results, columns=["Item","Total Profit"])

                        elif len(iso_format_date) == 2:
                            
                            timeframe_1 = iso_format_date[0]
                            timeframe_2 = iso_format_date[1]
                            match identified_product:
                                case "QUANTITY" | "VOLUME" | "QTY" | "AMOUNT" | "UNITS SOLD" | "SALES VOLUME":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['QTY']).label('total quantity')).where(salestable.columns.DATE.between((timeframe_1),(timeframe_2))).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total quantity")).limit(10)   
                                    exe = connection.execute(query)  
                                    result = pd.DataFrame(exe.fetchall())  
                                case "REVENUE" | "SALES" | "TOTAL SALES" | "GROSS REVENUE":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL SELLING PRICE']).label('total revenue')).where(salestable.columns.DATE.between((timeframe_1),(timeframe_2))).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total revenue")).limit(10)   
                                    result = connection.execute(query).fetchall() 
                                    formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                    result = pd.DataFrame(formatted_results, columns=["Item","Total Revenue"])
                                case "PROFIT" | "PROFITS":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL PROFIT']).label('total profit')).where(salestable.columns.DATE.between((timeframe_1),(timeframe_2))).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total profit")).limit(10)   
                                    result = connection.execute(query).fetchall() 
                                    formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                    result = pd.DataFrame(formatted_results, columns=["Item","Total Profit"])

                else:
                    ranking_value = int(ranking_value)
                    if timeframe is None:
                        match identified_product:
                            case "QUANTITY" | "VOLUME" | "QTY" | "AMOUNT" | "UNITS SOLD" | "SALES VOLUME":
                                query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['QTY']).label('total quantity')).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total quantity")).limit(ranking_value)   
                                exe = connection.execute(query)  
                                result = pd.DataFrame(exe.fetchall())  
                            case "REVENUE" | "SALES" | "TOTAL SALES" | "GROSS REVENUE":
                                query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL SELLING PRICE']).label('total revenue')).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total revenue")).limit(ranking_value)   
                                result = connection.execute(query).fetchall() 
                                formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                result = pd.DataFrame(formatted_results, columns=["Item","Total Revenue"])
                            case "PROFIT" | "PROFITS":
                                query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL PROFIT']).label('total profit')).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total profit")).limit(ranking_value)   
                                result = connection.execute(query).fetchall() 
                                formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                result = pd.DataFrame(formatted_results, columns=["Item","Total Profit"])

                    else:
                        print(f"{timeframe} is present")
                        if any(key.upper() in ["quarter","Q1","Q2","Q3","Q4","q1","q2","q3","q4"] for key in timeframe):
                            date_list = get_quarter_dates(list(timeframe))
                            iso_format_date = list(date_list.values())
                            print(f"date list for quarters: \n {date_list}")
                            print(f"formated date = > {iso_format_date}")
                        else:
                            data = [dateparser.parse(i, languages=["en"]) for i in timeframe ]
                            iso_format_date = [item.isoformat() if item else None for item in data]
                            iso_format_date = [datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').date() for s in iso_format_date]

                        if len(iso_format_date) == 1:
                            specified_date = iso_format_date[0]
                            print(f"=> {specified_date}")
                            match identified_product:
                                case "QUANTITY" | "VOLUME" | "QTY" | "AMOUNT" | "UNITS SOLD" | "SALES VOLUME":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['QTY']).label('total quantity')).where(salestable.columns.DATE == (specified_date)).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total quantity")).limit(ranking_value)   
                                    exe = connection.execute(query)  
                                    result = pd.DataFrame(exe.fetchall())  
                                case "REVENUE" | "SALES" | "TOTAL SALES" | "GROSS REVENUE":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL SELLING PRICE']).label('total revenue')).where(salestable.columns.DATE == (specified_date)).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total revenue")).limit(ranking_value)   
                                    result = connection.execute(query).fetchall() 
                                    formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                    result = pd.DataFrame(formatted_results, columns=["Item","Total Revenue"])
                                case "PROFIT" | "PROFITS":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL PROFIT']).label('total profit')).where(salestable.columns.DATE == (specified_date)).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total profit")).limit(ranking_value)   
                                    result = connection.execute(query).fetchall() 
                                    formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                    result = pd.DataFrame(formatted_results, columns=["Item","Total Profit"])

                        elif len(iso_format_date) == 2:
                            timeframe_1 = iso_format_date[0]
                            timeframe_2 = iso_format_date[1]
                            match identified_product:
                                case "QUANTITY" | "VOLUME" | "QTY" | "AMOUNT" | "UNITS SOLD" | "SALES VOLUME":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['QTY']).label('total quantity')).where(salestable.columns.DATE.between((timeframe_1),(timeframe_2))).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total quantity")).limit(ranking_value)   
                                    exe = connection.execute(query)  
                                    result = pd.DataFrame(exe.fetchall())  
                                case "REVENUE" | "SALES" | "TOTAL SALES" | "GROSS REVENUE":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL SELLING PRICE']).label('total revenue')).where(salestable.columns.DATE.between((timeframe_1),(timeframe_2))).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total revenue")).limit(ranking_value)   
                                    result = connection.execute(query).fetchall() 
                                    formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                    result = pd.DataFrame(formatted_results, columns=["Item","Total Revenue"])
                                case "PROFIT" | "PROFITS":
                                    query = sqlalchemy.select(salestable.c['ITEM'], sqlalchemy.func.sum(salestable.c['TOTAL PROFIT']).label('total profit')).where(salestable.columns.DATE.between((timeframe_1),(timeframe_2))).group_by(salestable.c['ITEM']).order_by(sqlalchemy.desc("total profit")).limit(ranking_value)   
                                    result = connection.execute(query).fetchall() 
                                    formatted_results = [(i, f"{v:,.2f}") for i, v in result]
                                    result = pd.DataFrame(formatted_results, columns=["Item","Total Profit"])

#REPORT LOGIC----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            case INTENT_DETECTION_FOR_REPORTS.report_type.SALES_REPORT:
                salestable = sqlalchemy.Table("sales_demo",metadata,autoload_with=engine)
                if len(timeframe) == 1:
                    query = salestable.select().where(salestable.columns.DATE == (timeframe[0]))
                elif len(timeframe) == 2:
                    query = salestable.select().where(salestable.columns.DATE.between((timeframe[0]),(timeframe[1])))
                
                exe = connection.execute(query)  
                result = pd.DataFrame(exe.fetchall())  

            

        print(result)
    return result 
                