import re
import NLP_INTENT_DETECTION
import Get_Historical_Data
import random
import time
import streamlit as st
from NER import load_model,model
from streamlit_option_menu import option_menu
from database_connection import database_connection
import pandas as pd




st.set_page_config(page_title="TABLES.AI", 
                   page_icon="IMAGES/Asset 8.png", 
                   layout="centered"
                   )


load_model()

product_history = []

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)




def get_response(y, x, z=None, ranking_value=None):
        list_of_responses = []
        print("get_response.....")

#COST PRICE LOGIC---------------------------------------------------------------------------------------------------------------------
        if y == NLP_INTENT_DETECTION.Search_Type.COST_PRICE and z:
            print(f"z is present = > {z}")
            x = x[0]
            z = z[0]

            print(z)
            db_response = database_connection(prediction= y, identified_product= x, timeframe=None, PoR=None, ranking_value=None, measurement= z)
            print(db_response)
            if len(db_response) == 1:
                product_name = db_response.iloc[0,0]
                cost_price = db_response.iloc[0,1]  
                COST = cost_price
                list_of_responses = [f"The cost price of {product_name} is ₵{COST}",
                                        f"{product_name} costs ₵{COST}",
                                        f"{product_name} has a cost price of ₵{COST}",
                                        f"The current cost price of {product_name} is ₵{COST}",
                                        f"₵{COST} is the cost price of {product_name}.",
                                        f"The base price for {product_name} is ₵{COST}",
                                        f"The cost for {product_name} is ₵{COST}",
                                        ]
                
                return random.choice(list_of_responses)
   
            elif len (db_response) > 1:
                data_frame = db_response
                list_of_responses = [f"There are {len(db_response)} products that match your search. Please see the table below for details."]

                return data_frame, list_of_responses[0]
            

        elif y == NLP_INTENT_DETECTION.Search_Type.COST_PRICE and not z:
            print(f"z is not present = > {z}")
            x = x[0]
            print(f"x => {x}")
            db_response = database_connection(y, x)
            print(db_response)
            if len(db_response) == 1:
                product_name = db_response.iloc[0,0]
                cost_price = db_response.iloc[0,1]  
                COST = cost_price
                list_of_responses = [f"The cost price of {product_name} is ₵{COST}",
                                        f"{product_name} costs ₵{COST}",
                                        f"{product_name} has a cost price of ₵{COST}",
                                        f"The current cost price of {product_name} is ₵{COST}",
                                        f"₵{COST} is the cost price of {product_name}",
                                        f"The base price for {product_name} is ₵{COST}",
                                        f"The cost for {product_name} is ₵{COST}",
                                        f"{product_name} comes at a cost of ₵{COST}"
                                        ]
                
                return random.choice(list_of_responses)
            
            elif len (db_response) > 1:
                data_frame = db_response
                list_of_responses = [f"There are {len(db_response)} products that match your search. Please see the table below for details."]

                return data_frame, list_of_responses[0]

#SELLING PRICE LOGIC------------------------------------------------------------------------------------------------------------------------------------------------------------------
        elif y == NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE and z:
            x = x[0]
            db_response = database_connection(prediction= y, identified_product= x, timeframe=None, PoR=None, ranking_value=None, measurement= z)
            if len(db_response) == 1:
                product_name = db_response.iloc[0,0].lower()
                selling_price = db_response.iloc[0,1]
                SELLING_PRICE = selling_price
                list_of_responses = [f"The selling price of {product_name} is ₵{SELLING_PRICE}",
                                     f"{product_name} sells for ₵{SELLING_PRICE}",
                                     f"{product_name} has a selling price of ₵{SELLING_PRICE}",
                                     f"The current selling price of {product_name} is ₵{SELLING_PRICE}",
                                     f"The price for {product_name} is ₵{SELLING_PRICE}",
                                     f"{product_name} is priced at ₵{SELLING_PRICE}",
                                     f"₵{SELLING_PRICE} is the selling price of {product_name}",
                                     f"₵{SELLING_PRICE} is what {product_name} sells for",
                                     f"The current price tag for {product_name} is ₵{SELLING_PRICE}",
                                     f"For {product_name}, the selling price is ₵{SELLING_PRICE}",
                                     ]
                return random.choice(list_of_responses)
            
            elif len (db_response) > 1:
                data_frame = db_response
                list_of_responses = [f"There are {len(db_response)} products that match your search. Please see the table below for details."]
                return data_frame, list_of_responses[0]
            
        elif y == NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE and not z:
            x = x[0]
            db_response = database_connection(y, x)
            if len(db_response) == 1:
                product_name = db_response.iloc[0,0].lower()
                selling_price = db_response.iloc[0,1]
                SELLING_PRICE = selling_price
                list_of_responses = [f"The selling price of {product_name} is ₵{SELLING_PRICE}",
                                     f"{product_name} sells for ₵{SELLING_PRICE}",
                                     f"{product_name} has a selling price of ₵{SELLING_PRICE}",
                                     f"The current selling price of {product_name} is ₵{SELLING_PRICE}",
                                     f"The price for {product_name} is ₵{SELLING_PRICE}",
                                     f"{product_name} is priced at ₵{SELLING_PRICE}",
                                     f"₵{SELLING_PRICE} is the selling price of {product_name}",
                                     f"₵{SELLING_PRICE} is what {product_name} sells for",
                                     f"The current price tag for {product_name} is ₵{SELLING_PRICE}",
                                     f"For {product_name}, the selling price is ₵{SELLING_PRICE}",
                                     ]
                return random.choice(list_of_responses)
            
            elif len (db_response) > 1:
                data_frame = db_response
                list_of_responses = [f"There are {len(db_response)} products that match your search. Please see the table below for details."]
                return data_frame, list_of_responses[0]


#HISTORICAL SALES LOGIC -------------------------------------------------------------------------------------------------------------------------------------------------------------
        elif y == NLP_INTENT_DETECTION.Search_Type.HISTORICAL_SALES:
            HISTORICAL_VALUE = Get_Historical_Data.get_historical_data(user_query=processing_result[-1], input=processing_result[2], prediction=processing_result[0])

            if HISTORICAL_VALUE[-1] == "REVENUE":
                if len(processing_result[2]) == 1:
                    x = x[0]
                    if HISTORICAL_VALUE[0] != "0.0":
                            list_of_responses = [f"the total revenue for {x} is ₵{HISTORICAL_VALUE[0]}",
                                                    f"We made ₵{HISTORICAL_VALUE[0]} in total on {x}",
                                                    f" ₵{HISTORICAL_VALUE[0]}",
                                                    f"On {x}, our total revenue was ₵{HISTORICAL_VALUE[0]}",
                                                    f"Our earnings on {x} amounted to ₵{HISTORICAL_VALUE[0]}",
                                                    f"₵{HISTORICAL_VALUE[0]} was the revenue for {x}",
                                                    f"The revenue recorded on {x} was ₵{HISTORICAL_VALUE[0]}",
                                                    f"Total revenue for {x}: ₵{HISTORICAL_VALUE[0]}",
                                                    f"₵{HISTORICAL_VALUE[0]} was made on {x}",
                                                    f"On {x}, we generated ₵{HISTORICAL_VALUE[0]} in revenue",
                                                    f"Our sales revenue for {x} reached ₵{HISTORICAL_VALUE[0]}",
                                                    f"We achieved ₵{HISTORICAL_VALUE[0]} in total revenue on {x}",
                                                    f"₵{HISTORICAL_VALUE[0]} was the total revenue on {x}",
                                                    f"The total earnings on {x} were ₵{HISTORICAL_VALUE[0]}",
                                                    f"On {x}, we earned ₵{HISTORICAL_VALUE[0]}",
                                                    f"₵{HISTORICAL_VALUE[0]} in revenue was recorded on {x}",
                                                    f"Total earnings for {x} were ₵{HISTORICAL_VALUE[0]}",
                                                    f"We brought in ₵{HISTORICAL_VALUE[0]} on {x}",
                                                    f"₵{HISTORICAL_VALUE[0]} was the total sales revenue for {x}",
                                                    f"Our revenue on {x} was ₵{HISTORICAL_VALUE[0]}"
                                                    ]
                    else:
                            list_of_responses = [f"we didn't make any sales on {x}.",
                                                    f"it seems i dont have any recorded sales for {x}, we may not have been open on that date.",
                                                    f"there's no data for {x}.",
                                                    f"No sales were recorded on {x}.",
                                                    f"It looks like {x} was a quiet day with no sales activity.",
                                                    f"There are no sales entries for {x} in our records.",
                                                    f"{x} shows no sales transactions in our database.",
                                                    f"Sadly, no sales data is available for {x}.",
                                                    f"{x} appears to have no sales recorded.",
                                                    f"We have no transaction data for {x}.",
                                                    f"It looks like we didn't process any sales on {x}.",
                                                    f"No sales information is available for {x}.",
                                                    f"It appears that there were no sales on {x}.",
                                                    f"We don't have any sales records for {x}.",
                                                    f"{x} has no sales data associated with it.",
                                                    f"Our system shows zero sales for {x}.",
                                                    f"We weren't able to find any sales for {x}.",
                                                    f"No sales took place on {x}, according to our records.",
                                                    f"{x} has no recorded sales transactions."
                                                ]
                
                elif len(processing_result[2]) == 2:
                        x[0] = processing_result[2][0]
                        x[1] = processing_result[2][1]
                        if HISTORICAL_VALUE[0] != "0.0":
                            list_of_responses = [f"The total revenue for {x[0]} to {x[1]} was ₵{HISTORICAL_VALUE[0]}",
                                                    f"We made ₵{HISTORICAL_VALUE[0]} in total from {x[0]} to {x[1]}",
                                                    f" ₵{HISTORICAL_VALUE[0]}",
                                                    f"From {x[0]} to {x[1]}, we generated a revenue of ₵{HISTORICAL_VALUE[0]}",
                                                    f"Our sales revenue from {x[0]} to {x[1]} reached ₵{HISTORICAL_VALUE[0]}",
                                                    f"Total earnings from {x[0]} to {x[1]} amounted to ₵{HISTORICAL_VALUE[0]}",
                                                    f"Between {x[0]} and {x[1]}, we earned ₵{HISTORICAL_VALUE[0]} in revenue.",
                                                    f"Revenue from {x[0]} to {x[1]} was ₵{HISTORICAL_VALUE[0]}",
                                                    f"₵{HISTORICAL_VALUE[0]} was the total revenue from {x[0]} to {x[1]}",
                                                    f"From {x[0]} to {x[1]}, we accumulated ₵{HISTORICAL_VALUE[0]} in sales.",
                                                    f"The revenue recorded from {x[0]} to {x[1]} was ₵{HISTORICAL_VALUE[0]}",
                                                    f"Our total revenue between {x[0]} and {x[1]} was ₵{HISTORICAL_VALUE[0]}",
                                                    f"We achieved ₵{HISTORICAL_VALUE[0]} in revenue from {x[0]} to {x[1]}",
                                                    f"₵{HISTORICAL_VALUE[0]} was generated in sales from {x[0]} to {x[1]}",
                                                    f"From {x[0]} to {x[1]}, our revenue totaled ₵{HISTORICAL_VALUE[0]}",
                                                    f"The total sales revenue from {x[0]} to {x[1]} was ₵{HISTORICAL_VALUE[0]}",
                                                    f"We brought in ₵{HISTORICAL_VALUE[0]} from sales between {x[0]} and {x[1]}",
                                                    f"₵{HISTORICAL_VALUE[0]} was the revenue from {x[0]} to {x[1]}",
                                                    f"Our total earnings from {x[0]} to {x[1]} were ₵{HISTORICAL_VALUE[0]}",
                                                    f"Between {x[0]} and {x[1]}, our revenue reached ₵{HISTORICAL_VALUE[0]}"
                                                ]
                        else:
                            list_of_responses = [f"we didn't make any sales from {x[0]} to {x[1]}",
                                                f"it seems i dont have any recorded sales for the period of {x[0]} to {x[1]}, we may not have been open on those dates",
                                                f"there's no data for {x[0]} to {x[1]}",f"Unfortunately, we have no sales records for {x}.",
                                                ]
                    
            elif HISTORICAL_VALUE[-1] == "PROFIT":
                if len(processing_result[2]) == 1:
                    x = x[0]
                    if HISTORICAL_VALUE[0] != "0.0":
                        list_of_responses = [f"the total profit for {x} was ₵{HISTORICAL_VALUE[0]}",
                                                f"We made ₵{HISTORICAL_VALUE[0]} in profit on {x}",
                                                f" ₵{HISTORICAL_VALUE[0]}"
                                                ]
                    else:
                        list_of_responses = [f"we didn't make any sales on {x}",
                                                 f"it seems i dont have any recorded profit for {x}, we may have not been opened on that date.",
                                                 f"there's no data for {x}"
                                                 ]
                elif len(processing_result[2]) == 2:
                    if HISTORICAL_VALUE[0] != "0.0":
                        list_of_responses = [f"The total profit from {x[0]} to {x[1]} was ₵{HISTORICAL_VALUE[0]}",
                                            f"We made ₵{HISTORICAL_VALUE[0]} in profit from {x[0]} to {x[1]}",
                                            f" ₵{HISTORICAL_VALUE[0]}",
                                            f"From {x[0]} to {x[1]}, we generated ₵{HISTORICAL_VALUE[0]} in profit.",
                                            f"Our total profit from {x[0]} to {x[1]} reached ₵{HISTORICAL_VALUE[0]}"
                                            ]
                        
                    else:
                        list_of_responses = [f"we didn't make any sales from {x[0]} to {x[1]}",
                                            f"it seems i dont have any recorded profit information for the period of {x[0]} to {x[1]}, we may have not been opened on those dates",
                                            f"there's no data for {x[0]} to {x[1]}"
                                            ]
                            
            return random.choice(list_of_responses) 
            

        elif y == NLP_INTENT_DETECTION.Search_Type.RANKING:
                if ranking_value is None:
                    print("it is none")
                    if z is None:
                        db_response = database_connection(y, x)
                    else:
                        db_response = database_connection(y, x, z)
                else:
                    print("it is not none")
                    if z is None:
                        print("getting data.....")
                        db_response = database_connection(prediction = y, identified_product = x, timeframe = None, PoR = None, ranking_value = ranking_value)
                        print(db_response)
                    else:
                        db_response = database_connection(prediction= y,identified_product= x,timeframe= z,PoR= None, ranking_value= ranking_value)


                if db_response.empty :
                    list_of_responses = [f"we didn't make any sales on {z}, so i cant get you that information",
                                        f"there's no data for {z}"
                                                 ]
                    return random.choice(list_of_responses)
                else:
                    return db_response
        

        

def typing_effect(text):
    response = text
    for word in response.split():
        for letter in word:
             yield letter
        yield " "
        time.sleep(0.1)  # Print a newline after the typing effect is complete




def word_processing(UserInput):
    global model
    if model is None:
        load_model()

    product_list = None
    date_list = None
    UserInput = UserInput.lower()
    UserInput = re.sub(r"\s{2,}"," ",UserInput) #substitute extra spaces if any with a singular whitespace
    UserInput = UserInput.lower().strip()
    numerical_value = re.findall(r"top\s*(\d+)| bottom\s*(\d+) | \b(\d+)\b\s+highest | \b(\d+)\b\s+lowest",UserInput)
    print(type(numerical_value))
    print(numerical_value)
    if numerical_value:
        numerical_value = next((item for item in numerical_value[0] if item), None)
        numerical_value = int(numerical_value)
    else:
        numerical_value = None

    print(f"original: {UserInput}")
    print(f"numerical value => {numerical_value}")
            
                   
    UserInput = re.sub(r"((?<=\d)th|(?<=\d)st|(?<=\d)rd|(?<=\d)nd)\b","",UserInput)
    print(f"formated:  {UserInput}")
    query_keywords_search = re.findall(r"\b(does|of|or|is|for)\b",UserInput) # look for "of,"does","is" & "or" in the query string so we can lowercase them later
    question_mark_search = re.search(r"\?$",UserInput) #look for the question mark so we can either add it if not in the query string
    query_tokens = UserInput.split() #break down the query into smaller chunks

    if question_mark_search:
        pass #if "?" is present do nothing
    else: 
        query_tokens.append("?") #if "?" is not in the query we append it to it

    if len(query_keywords_search) >= 1 :
        tokens_after_last_keyword = query_tokens[query_tokens.index(query_keywords_search[-1])+1:] # Find the indexes of the objects found from the "query_keyword_search" in the query string
        capitalized_remaining_tokens = [word.capitalize() for word in tokens_after_last_keyword] # Capitalize every word after the last keyword found from "query_keywords_search" in the query string, including the keyword itself
        query_tokens[query_tokens.index(query_keywords_search[-1])+1:] = capitalized_remaining_tokens # Replace the tokens in "query_tokens" from the index after the last keyword found in "query_keywords_search"
    # with the capitalized tokens in "capitalized_remaining_tokens"
        do_index = next((i for i, words in enumerate(query_tokens) if re.match(r'\bDo\b', words)), None) # Find the index of the first token in query_tokens that matches the pattern for the word "Do"
        for index, words in enumerate(query_tokens):
            # Convert tokens containing "On","In", "Cost" to lowercase in the query_tokens list
            if "On" in words:
                query_tokens[index] = words.lower()         
            elif "In" in words:
                query_tokens[index] = words.lower()
            elif "Cost" in words:
                query_tokens[index] = words.lower()
            if do_index is not None:
                #if do is found, delete it from the "query_tokens"
                del query_tokens[do_index:]

    capitalized_product = " ".join(query_tokens)

    test_x = [UserInput]
    docs = [NLP_INTENT_DETECTION.nlp(text) for text in test_x]
    test_x_vectors = [doc.vector for doc in docs] 
    prediction = NLP_INTENT_DETECTION.classify_svm.predict(test_x_vectors)
    print(prediction)

    if prediction == NLP_INTENT_DETECTION.Search_Type.COST_PRICE or prediction == NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE:
        labels = ["product", "measurement"]

    elif prediction == NLP_INTENT_DETECTION.Search_Type.HISTORICAL_SALES:
        labels = ["product", "date", "timeframe"]

    elif prediction == NLP_INTENT_DETECTION.Search_Type.RANKING:
        labels = ["timeframe", "metric"]

    entities = model.predict_entities(UserInput,labels,threshold=0.4)
     ## classification
    entities_dict = {entity["text"]:entity["label"] for entity in entities}
    

    print(f"dict of entities from gliner \n {entities_dict}")
    

    date_list = [key for key, value in entities_dict.items() if value == "date"]
    print(date_list)
    for i ,date_str in enumerate(date_list):
        if "of" in date_str:
            date_list[i] = date_str.replace("of","")
            date_list = [date_str.strip() for date_str in date_list]    

    product_list = [key for key, value in entities_dict.items() if value == "product"]

    metric_list = [key for key, value in entities_dict.items() if value == "metric"]

    timeframe_list = [key for key, value in entities_dict.items() if value == "timeframe"]

    measurement_list = [key for key, value in entities_dict.items() if value == "measurement"]
#-------------------------------------------------------------------------------------------------------------------------------------------  
    if prediction == NLP_INTENT_DETECTION.Search_Type.HISTORICAL_SALES :
        if date_list:
            return [prediction, capitalized_product, date_list, query_tokens]
        else:
            return [prediction, capitalized_product, timeframe_list, query_tokens]
#-------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------      
    elif prediction == NLP_INTENT_DETECTION.Search_Type.COST_PRICE or prediction == NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE:
        if product_list:
            print("product is present")
            if measurement_list:
                print(f"meas {measurement_list}")
                return [prediction, measurement_list, product_list]
            else:
                print("no meas")
                return [prediction, capitalized_product, product_list, query_tokens]
        else:
            print("product is not present")
            if measurement_list:
                print(f"meas {measurement_list}")
                return [prediction, measurement_list, None]
            else:
                print("no meas")
                return [prediction, capitalized_product, None, query_tokens]
        
#-------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------   
    elif prediction == NLP_INTENT_DETECTION.Search_Type.RANKING:
        if metric_list:
            print(f"metric is present")
            if numerical_value is not None:
                print("number is present")
                print(f" =>  {numerical_value}")
                if timeframe_list:
                    print(timeframe_list)
                    return [prediction, capitalized_product, metric_list, numerical_value, timeframe_list]
                else:
                    print(metric_list)
                    return [prediction, capitalized_product, metric_list, numerical_value]

            else:
                print("number is not present")
                if timeframe_list:
                    print(timeframe_list)
                    return [prediction, capitalized_product, metric_list, query_tokens, timeframe_list]
                else:
                    print(metric_list)
                return [prediction, capitalized_product, metric_list, query_tokens]
        else:
            print(f"no metric")
            metric_list = ["volume"]
            print(metric_list[0])
            if numerical_value is not None:
                print("number is present")
                print(f" =>  {numerical_value}")
                if timeframe_list:
                    print(timeframe_list)
                    return [prediction, capitalized_product, metric_list, numerical_value, timeframe_list]
                else:
                    print(metric_list)
                    return [prediction, capitalized_product, metric_list, numerical_value]

            else:
                print("number is not present")
                if timeframe_list:
                    print(timeframe_list)
                    return [prediction, capitalized_product, metric_list, query_tokens, timeframe_list]
                else:
                    print(metric_list)
                return [prediction, capitalized_product, metric_list, query_tokens]





#------------------------------------------------------------------------------------------------------------------------   
st.markdown(
    """
<style>
    .st-emotion-cache-1c7y2kd {
        flex-direction: row-reverse;
        text-align: right;
        color: #0000FF ;
    }
</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
<style>
    h2 {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True,
)


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages_2 = []


hide_element_css = """
<style>
.object-key-val {
    display: none;
}
</style>
"""
st.markdown(hide_element_css, unsafe_allow_html=True)


st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #000000;
    }
</style>
""", unsafe_allow_html=True)


st.logo("IMAGES/Asset 9.png",icon_image="IMAGES/Asset 9@4x-8.png")

with st.sidebar:

    selected = option_menu(
                           menu_title=None, 
                           options= ["About","Get Started","List of Products"], 
                           icons=["info"],
                           menu_icon=None,
                           orientation="horizontal",
                           styles={
                                    "container": {
                                                    "padding": "0px", 
                                                    "background-color": "black",
                                                    "border-radius": "0px",
                                                    "width": "100%",
                                                    "display": "flex",
                                                    "justify-content": "space-evenly"
                                                },

                                    "icon": {   
                                                "color": "white", 
                                                "font-size": "18px"
                                            }, 

                                    "nav-link": {
                                                    "font-size": "15px", 
                                                    "text-align": "left", 
                                                    "margin":"0px", 
                                                    "--hover-color": "grey", 
                                                    "color": "white",
                                                    "white-space": "nowrap"
                                                },

                                    "nav-link-selected": {
                                                            "background-color": "white",
                                                            "color": "black"
                                                        },
                           }
                           )
                   
    if selected == "About":
        st.header("Introducing TABLES: Technology Assisting Business Logic Efficiency System")

        st.caption("""
                
    TABLES.AI is your ultimate companion for streamlined data retrieval and insightful analytics within your company. 
    Designed to save time and enhance productivity, this innovative AI-powered application functions as both a virtual assistant and a data analyst, 
    providing instant access to crucial company information and generating comprehensive reports upon request.

    Key Features:

    * Fast Data Retrieval: Retrieve information swiftly on basic company details, product information, sales figures, and more.

    * Natural Language Interaction: Communicate effortlessly with the AI using natural language, just like conversing with a knowledgeable data analyst.

    * Comprehensive Knowledge: Gain access to a wealth of company knowledge, including historical data, financial insights, and operational metrics.

    * Report Generation: Prompt the AI to generate detailed reports tailored to specific queries or requirements.

    TABLES.AI revolutionizes how you access and utilize company data, empowering you to make informed decisions efficiently. 
    Whether you're managing operations, analyzing market trends, or planning strategies, TABLES.AI is your reliable partner in maximizing productivity and driving success. 
                
                """)
        
        st.header("Part of the Larger TABLES Software Suite")
        st.caption("""TABLES.AI is a component of the comprehensive TABLES software suite, designed to help gather data within your organization. The suite includes:

* POS Section: For recording transactions efficiently.
* Inventory Management: To keep track of stock levels and manage orders.
* Warehouse Management System: To streamline logistics and warehouse operations
                   
                   """)
        
        st.header("Customizable to Your Business Needs")
        st.caption("""The TABLES software suite, including TABLES.AI, is highly customizable to fit the unique requirements of your company. Whether your business is in wholesale, retail, construction, or any other industry, TABLES can be adapted to suit your needs.
* Industry-Specific AI Training: The AI will be trained on data specific to your organization, ensuring that it provides relevant insights and recommendations.
* Enhanced Decision-Making: Empower stakeholders to make better decisions based on robust data analysis and actionable insights.
* Efficient Data Recording: Enable employees to record data effectively, reducing errors and increasing efficiency.
                   
Even if your company does not have a dedicated data analyst, TABLES.AI ensures you benefit from strong data analysis and visual representations, which can be used to inform stakeholders and drive business success.

""")
        
    if selected == "Get Started":
        st.header("""  Welcome to Our Chatbot Demo! """)
        
        st.caption("""

Explore the capabilities of our interactive chatbot designed to assist you with:
                   
* Information Retrieval: Get instant answers about product details, sales data, and more.
""")

        st.header("Step-by-Step Guide: Getting Started with Our Chatbot")    
              
        st.caption("""        
Type Your Query: Start by typing a search query such as:

* "What is the cost price of [product]?"
* "What was the revenue on [date]?"
* "what was our profit on [date]?"
* "How much did we make from [date] to [date]?"
* "What were the top products by [ volume | revenue | profit ] for [date]?"
                   
Receive Instant Answers: Our chatbot will process your query and provide real-time responses, including:

* Cost Prices: Get detailed cost price information for specific products.
* Revenue Data: Retrieve revenue figures for any date you specify.
* Sales Insights: Explore sales data dynamically updated throughout the day.(feature not included in demo version)

Get started now and experience seamless information retrieval with our interactive chatbot!
                   """)
                   
        st.header("Tips for Users:")
        st.caption("""
- Please write the dates in full eg ("4th december 2024" | "december 4th 2024" | "4/12/2024" | "4-12-2024" | "q1" | "q2" ) this is also a limitation of this demo version
- Table Disappearance Note: Tables vanish once a new message is sent, so review results promptly. This is due to limitations due to streamlit
                    """)

                   
        

    if selected == "List of Products":
        st.header("THIS IS A LIST OF THE PRODUCTS IN THE DATABASE")

        st.caption("""
- ARIZONA VARIETY PACK (591ML X24)                 
- ARIZONA WATERMELON (591ML X24)                
- AWAKE PURIFIED WATER (500ML X16)          
- AWAKE PURIFIED WATER (750ML X16)        
- BEL AQUA ACTIVE (500ML X16)
- BEL AQUA BOTTLE (330ML X15)
- BEL AQUA BOTTLE (500ML X15)
- BEL AQUA WATER (1.5L X12)
- BEL AQUA WATER (17L X1)
- BEL AQUA WATER (4L X1)
- BEL AQUA WATER (750ML X15)
- BEL PORTELLO (350ML X16)
- COCA COLA BOTTLE (300ML X12)
- COCA COLA CAN (330ML X24)
- DIORA GOLD KDM RICE (5KG X5)
- FAIRY ADW AIO ORIGINAL (6 X189)
- FAIRY BEADS IN-WASH SCENT (176GM X6)
- FAIRY CLEAN AND FRESH POMEGRANATE (10 X320ML)
- FANTA COCKTAIL BOTTLE (300ML X12)
- FANTA ORANGE BOTTLE (1.5L X6)
- FANTA ORANGE BOTTLE (1L X6)
- FANTA ORANGE BOTTLE (2L X4)
- FRUITY COCKTAIL JUICE PACK (125ML X24)
- GLADE GELL (150GM X8)
- GLADE SPICED APPLE CINNAMON (120G X6)
- GINO PEPPER AND ONION TOMATO MIX (200G X24)
- GINO TOMATO MIX (1.05KG X12)
- HAPIC ACTIVE FRESH FRESH CITRUS (750ML X12)
- HAPIC ACTIVE FRESH PINK BLOSSOM (750ML X12)
- GUINESS BEER CAN (330ML X12)
- GUINESS BEER CAN (330ML X24)
- GUINESS BEER CAN (330ML X6)
- GUINESS MALT CAN (330ML X12)
- GUINESS MALT CAN (330ML X24)
- HEINEKEN BEER CAN (330ML X24)
- HONEY NUT CHEERIOS (10X 436G)
- HUNTERS GOLD BEER BOTTLE (330ML X24)
- INDOMIE BELLE FULL ONION CHICKEN (280GM X18)
- INDOMIE HUNGRY MAN ONION CHICKEN (180GM X26)
- LIME CORDIAL BOTTLE (750ML X12)
- MONSTER ENERGY (500ML X12)
- MONSTER ENERGY MANGO LOCO (500ML X12)
- MONSTER ENERGY PIPELINE PUNCH (500ML X12)
- MONT WATER (330ML X20)
- MONT WATER (500ML X20)

""")

        st.header("THESE ARE THE DATES AVAILABLE")
        st.caption("[4th DECEMBER 2023 - 29th JUNE 2024], you can also specify the quarter (q1 | q2 | q3 | q4)")


# Display chat messages from history on app rerun

for message in st.session_state.messages:
    avatar = "IMAGES/icons8-user-male-64.png" if message["role"] == "user" else "IMAGES/Asset 5.png"
    with st.chat_message(message["role"],avatar=avatar):
        st.markdown(message["content"])


if user_query := st.chat_input("ask a question"):
    global processing_result
    st.session_state.messages.append({"role":"user","content":user_query}) 

    print(f"previous = >  {st.session_state.messages_2}")
    try:
        with st.chat_message("user",avatar="IMAGES/icons8-user-male-64.png"):
            st.markdown(user_query)
           
            processing_result = word_processing(user_query)
            if processing_result[2] is None:
                processing_result[2] = [st.session_state.messages_2[-1]]
            else:
                processing_result[2] = processing_result[2]
                print(processing_result[2])
            

            if processing_result[0] == NLP_INTENT_DETECTION.Search_Type.RANKING:
                if isinstance (processing_result[3], int):
                    if len(processing_result) == 5:
                        response_selection = get_response(processing_result[0], processing_result[2], processing_result[-1], processing_result[3])
                    else:
                        print(f"processing result 3 => {processing_result[3]}")
                        response_selection = get_response(processing_result[0],processing_result[2],None,processing_result[3])
                        print("ok")

                else:
                    if len(processing_result) == 5:
                        response_selection = get_response(processing_result[0], processing_result[2], processing_result[-1])
                    else:
                        print(f"processing result 3 => {processing_result[3]}")
                        response_selection = get_response(processing_result[0],processing_result[2])
                        print("ok")

            elif processing_result[0] == NLP_INTENT_DETECTION.Search_Type.COST_PRICE or processing_result[0] == NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE:
                product = processing_result[2][0]
                st.session_state.messages_2.append(product)
                
                if len(processing_result) == 3:
                    print(f"get response with measurement ")
                    response_selection = get_response(y= processing_result[0],x=  processing_result[2], z = processing_result[1])

                elif len(processing_result) == 4:
                    print(f"get response without measurement ")
                    response_selection = get_response(y= processing_result[0],x= processing_result[2])

            else:
                response_selection = get_response(processing_result[0], processing_result[2])

            response_selection = response_selection

        ##entity recognition

        #display bot message in chat container
        with st.chat_message("assistant",avatar="IMAGES/Asset 5.png"):

        ##this codeblock below is for checking cost and selling price
            if (processing_result != "no" and 
                isinstance(processing_result[2], list) and 
                (processing_result[0] == NLP_INTENT_DETECTION.Search_Type.COST_PRICE or 
                processing_result[0] == NLP_INTENT_DETECTION.Search_Type.SELLING_PRICE)
                ):

                if isinstance(response_selection,str):
                    response = st.write_stream(typing_effect(response_selection))


                elif isinstance(response_selection[0], pd.DataFrame):
                    response = st.write_stream(typing_effect(response_selection[1]))
                    st.write(response_selection[0])
                    st.caption("Note: This table will disappear once a new message is sent,Please be more specific next time, mentioning the measurement along with the product name.\neg - [product => (Awake)] [measurement => (500ml)]")

    ## this codeblock below is for checking historical sales
            elif processing_result[0] == NLP_INTENT_DETECTION.Search_Type.HISTORICAL_SALES:
                Get_Historical_Data.get_historical_data(processing_result[-1], processing_result[2], processing_result[0])
                response = st.write_stream(typing_effect(response_selection))


            elif processing_result[0] == NLP_INTENT_DETECTION.Search_Type.RANKING:
                if isinstance(response_selection,pd.DataFrame):
                    response = st.write(response_selection)
                    st.caption("Note: This table will disappear once a new message is sent, due to limitations in the current Streamlit setup. This issue will not be present in the final product. you can download the table's data by clicking the download icon above it")
                else:
                    response = st.write_stream(typing_effect(response_selection))
            

                #add prompt to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    
    except :
        with st.chat_message("assistant",avatar="C:\\Users\\akofi\\OneDrive\\Desktop\\App_projects\\PNG\\Asset 5.png"):
            if TypeError:
                response = st.write_stream(typing_effect("There was an issue processing your request. Please try again or ask a different question."))
                st.session_state.messages.append({"role": "assistant", "content": response})
            elif IndexError:
                response = st.write_stream(typing_effect("No product found"))
                st.session_state.message.append({"role": "assistant", "content": response})
