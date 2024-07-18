import streamlit as st
import INTENT_DETECTION_FOR_REPORTS
from get_kpis import get_kpi
from query_processing import process_query
import dateparser
from datetime import datetime
from NER import load_model,model
import plotly.express as px
from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

st.set_page_config(page_title="analytics dashboard",
                   page_icon= "C:\\Users\\akofi\\OneDrive\\Desktop\\App_projects\\1x\\Asset 8.png",
                   layout="wide",
                   )

load_model()

report_prediction = None
total_sales = None

engine = create_engine('mysql+pymysql://root:iankofiaddo_db@localhost:3306/demo_db')

st.markdown(
    """
<style>
    h1 {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True,
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

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #000000;
    }
</style>
""", unsafe_allow_html=True)

quarters = {
    "Q1": {"start": f"{datetime.today().year}-01-01", "end": f"{datetime.today().year}-03-31"},
    "Q2": {"start": f"{datetime.today().year}-04-01", "end": f"{datetime.today().year}-06-30"},
    "Q3": {"start": f"{datetime.today().year}-07-01", "end": f"{datetime.today().year}-09-30"},
    "Q4": {"start": f"{datetime.today().year}-10-01", "end": f"{datetime.today().year}-12-31"},
            }

# Function to get the ISO format dates for a given quarter phrase
def get_quarter_dates(phrase):
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
    phrase = phrase.lower()
    if phrase in quarter_map:
        quarter = quarter_map[phrase]
        return quarters[quarter]
    else:
        return None


# Define CSS for centering content
st.markdown(
    """
    <style>
    .st-emotion-cache-1r6slb0 {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;  /* Ensures the height is consistent */
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
    .st-emotion-cache-17c4ue {
    display:flex;
    justify-content: center;
    align-element:center;
    text-align:center;

}

""",unsafe_allow_html=True
)


card_style = """
<style>
.user-select-none {
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    background-color: #f7f7f7;
}
</style>
"""


with st.sidebar:
                      
    st.title("Report Generation (Demo Version)")

    st.header(" Welcome to the Report Generation Section")                        
    st.caption(" Thank you for exploring the report generation capabilities of our AI assistant. Please note that this is a demo version, and as such, certain features and functionalities are limited, it is just for you to have a taste of what is capable with TABLES AI. Here’s what you can expect:")

    st.header("What This Demo Version Can Do:")
    st.caption("""
* Basic Data Visualization: Generate simple charts and graphs to visualize key metrics such as sales, profit, and product performance.
* Summary Insights: Receive concise, automated insights based on your data, highlighting trends, spikes, and notable changes.
* User Interaction: In the demo version, you can only ask the AI to generate a sales report. Follow-up questions or more complex queries are not supported in this demo.
               """)
    st.header("Example Query:")
    st.caption("""
               * generate a sales report for [ [date range] or quarter (Q1,Q2,Q3,Q4) ]
               * get me a report on sales for [ [date range] or quarter (Q1,Q2,Q3,Q4) ]
               """)
    
    st.header("Limitations of the Demo Version:")
    st.caption("""
* Sales Reports Only: This demo version is limited to generating sales reports. Other types of reports are not available in the demo.
* Feature Restrictions: Advanced features such as predictive analytics, detailed segmentation, and custom report templates are not available in this demo.
* Data Range: The demo version may be limited to a specific range or subset of your data, providing an overview rather than an in-depth analysis.
* Customization: Customizable reports and advanced formatting options are restricted in this version.
* Performance: The demo version may have performance constraints, including slower processing times and reduced responsiveness.
               
               """)
    
    st.header("Upcoming Full Version Features:")
    st.caption("""
* Comprehensive Analytics: Detailed and customizable reports with advanced analytics and predictive insights.
* Enhanced Data Visualization: A broader range of interactive charts, graphs, and dashboards tailored to your specific needs.
* Custom Report Templates: Create and save your own report templates for easy reuse and consistency.
* Scalability: Improved performance and scalability to handle larger datasets and more complex queries.
* Integration: Seamless integration with various data sources and business intelligence tools.
               
We appreciate your understanding as we continue to develop and enhance our AI assistant. Your feedback is invaluable in helping us create a more robust and versatile tool for all your data analysis needs.
               
               """)





# Render the CSS style
st.markdown(card_style, unsafe_allow_html=True)
# Text input for user questions
user_input = st.text_input("Ask a question", "")


# Button to submit the question
if st.button("Submit"):

    @st.cache_data
    def database_connection_for_reports(prediction, timeframe):
        print("connecting to db.....")
        print(timeframe)
        with engine.connect() as connection:
            metadata = sqlalchemy.MetaData()
            if prediction == INTENT_DETECTION_FOR_REPORTS.report_type.SALES_REPORT:
                salestable = sqlalchemy.Table("sales_demo",metadata,autoload_with=engine)
                match isinstance(timeframe,list):
                            case False:
                                query = salestable.select().where(salestable.columns.DATE == (timeframe))
                            case True:
                                query = salestable.select().where(salestable.columns.DATE.between((timeframe[0]),(timeframe[1])))
                exe = connection.execute(query)  
                df = pd.DataFrame(exe.fetchall())
        return df
    


    print(user_input)
    report_prediction = process_query(user_input)

    labels = ["date"]
    entities = model.predict_entities(user_input,labels,threshold=0.4)
    print(entities)

    entities_dict = {entity["text"]:entity["label"] for entity in entities}
    print(entities_dict)

    if any(key in entities_dict for key in ["quarter","Q1","Q2","Q3","Q4","q1","q2","q3","q4"]):
        date_list = get_quarter_dates(list(entities_dict.keys())[0])
        date_list = list(date_list.values())
        print(f"date list for quarters: \n {date_list}")

    else:
        date_list = [dateparser.parse(key, languages=["en"]) for key, value in entities_dict.items() if value == "date"]
        iso_format_date = [item.isoformat() if item else None for item in date_list]
        date_list = [datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').date() for s in iso_format_date]
    
    
    print(f"date_list => {date_list}")
# Additional content can go here
    match report_prediction:
        case INTENT_DETECTION_FOR_REPORTS.report_type.SALES_REPORT:
           
            df = database_connection_for_reports(report_prediction,date_list)
            kpi_data = get_kpi(report_prediction,date_list)
            
#CREATION ON FIELDS FOR KPIS-----------------------------------------------------------------------------------
            left_column, middle_column, right_column = st.columns(3)
            if len(kpi_data) != 0 :
                with left_column:
                    st.markdown('<div class="centered-metric">', unsafe_allow_html=True)
                    st.metric(label="total revenue",
                            value=f"GH₵ {format(round(kpi_data[0]),",")}"
                                            )
                    st.markdown('</div>', unsafe_allow_html=True)

                with middle_column:
                    st.markdown('<div class="centered-metric">', unsafe_allow_html=True)
                    st.metric(label=f"Most Popular Product for {list(entities_dict.keys())[0]}:",
                            value=f"{kpi_data[2]}",
                            delta=f"{kpi_data[3]} sold"
                                         )
                    st.markdown('</div>', unsafe_allow_html=True)

                with right_column:
                    st.markdown('<div class="centered-metric">', unsafe_allow_html=True)
                    st.metric( label=f"**Gross Profit:**",
                            value=f"GH₵ {format(round(kpi_data[1]),",")}"
                                        )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                st.markdown("---")

                            
#------------------------------------------------------------------------CHARTS-----------------------------------------------------------

#SALES BY ITEM [BAR CHART] ------------------------------------------------------------------------------------------------------------
                
                QTY_by_item = df.groupby("ITEM")["QTY"].sum().reset_index()
                QTY_by_item = QTY_by_item.sort_values(by="QTY",ascending=False)
                QTY_by_item = QTY_by_item.head(10)
                fig_product_QTY = px.bar(QTY_by_item,
                                        x="QTY",
                                        y="ITEM",
                                        orientation="h",
                                        title=f"<b> Top {10} Best-Performing Products Per Quantity Sold </b>",
                                        color_discrete_sequence=["#FF6F0A"]* len(QTY_by_item),
                                        template="plotly_dark",
                                        )
                fig_product_QTY.update_layout(
                    yaxis_title = "",
                    xaxis_title = "total volume (GH₵)",
                    barmode="stack",
                    yaxis_categoryorder="total ascending",
                    xaxis_tickformat=",.0f",
                    height=500
                )

#LINE CHART ---------------------------------------------------------------------------------------------------------------------------

                total_profits_over_time = df.groupby("DATE")["TOTAL PROFIT"].sum()
                line_chart_fig = px.line(total_profits_over_time,
                                        title= "<b> total profits over time </b>",
                                        color_discrete_sequence=["#FFA500"]*len(df),
                                        template="plotly_white"
                                        )
                line_chart_fig.update_layout(xaxis_title="Date", yaxis_title=None)
                

#M.O.M Revenue [BAR CHART] ------------------------------------------------------------------------------------------------------------

                mom_revenue = df.groupby("MONTH")["TOTAL SELLING PRICE"].sum().reset_index()
                mom_revenue = mom_revenue.sort_values(by="MONTH",ascending=False)

                mom_revenue_fig = px.bar(mom_revenue,
                                        x="MONTH",
                                        y="TOTAL SELLING PRICE",
                                        orientation="v",
                                        title=f"<b> M.O.M Revenue",
                                        color_discrete_sequence=["#FF6F0A"]* len(mom_revenue),
                                        template="plotly_dark",
                                        )



#HISTOGRAM-----------------------------------------------------------------------------------------------------------------------------
                category_dominance = df["TOTAL SELLING PRICE"].idxmax()
                product_category_dominance = px.histogram(df,
                                                        title="<b> Category Dominance </b>",
                                                        x="CATEGORY",
                                                        y="TOTAL SELLING PRICE",                            
                                                        color_discrete_sequence=["indianred"],
                                                        height=600,
                                                        template="plotly_dark",
                                                        text_auto=True,
                                                        histnorm="percent",
                                                        hover_data=["TOTAL SELLING PRICE"],
                                                        )
                product_category_dominance.update_layout(xaxis={"categoryorder":"total ascending"},
                                                        xaxis_title="Categories",
                                                        )
                product_category_dominance.update_traces(hovertemplate="%{y:.2f}%",
                                                        textposition="outside",
                                                        )



#PIE CHART --------------------------------------------------------------------------------------------------------------------------------

                total_qty_per_category = df.groupby("CATEGORY")["QTY"].sum()
                total_qty_per_category = total_qty_per_category.sort_values(ascending=False)
                total_qty_per_category = total_qty_per_category.head(5).reset_index()

                norm = plt.Normalize(total_qty_per_category['QTY'].min(), total_qty_per_category['QTY'].max())
                normed_values = norm(total_qty_per_category['QTY'])
                custom_normed_values = 0.2 + 0.6 * normed_values

                # Generate colors using a colormap
                colormap = plt.cm.Oranges  # You can choose any matplotlib colormap
                colors = [mcolors.to_hex(colormap(val)) for val in normed_values]

                pie_chart_fig = px.pie(total_qty_per_category, 
                                       values='QTY', 
                                       names='CATEGORY', 
                                       title='Category Dominance',
                                       template="plotly_white")
                
                pie_chart_fig.update_traces(marker=dict(colors=colors))
                

                left_column , right_column = st.columns(2)
                
                st.markdown('<div class="card">', unsafe_allow_html=True)
                left_column.plotly_chart(line_chart_fig,use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                right_column.plotly_chart(fig_product_QTY, use_container_width=False)
                st.markdown("##")

                right_column.plotly_chart(pie_chart_fig,use_container_width=True)
                st.markdown("##")

                left_column.plotly_chart(mom_revenue_fig, use_container_width=False)
                st.markdown("##")

                def generate_insights(piechartdata,momrevenuedata,topproducts=None,revenuedata=None):
                    # Replace this with your actual AI model code to generate insights
                    top_category = piechartdata.iloc[0,0]
                    top_qty = piechartdata.iloc[0,1]

                    top_product = topproducts.iloc[0,0]
                    top_product_qty = topproducts.iloc[0,1]
                    total_products = topproducts["QTY"].sum()
                    percentage_of_product = (top_product_qty/total_products)*100
                    
                    top_month = momrevenuedata.iloc[0,0]
                    top_month_revenue = momrevenuedata.iloc[0,1]

                    previous_top_month = momrevenuedata.iloc[1,0]
                    previous_month_revenue = momrevenuedata.iloc[1,1]

                    revenue_percentage_change = ((top_month_revenue - previous_month_revenue)/ previous_month_revenue)*100

                    latest_date = revenuedata.index.max()
                    total_profit_latest_date = revenuedata.loc[latest_date]
                    oldest_date = revenuedata.index.min()
                    total_profit_oldest_date = revenuedata.loc[oldest_date]

                    insights = ""
                    
                    insights += "Insights:\n"
                    insights += f"1. Category {top_category} has the highest number of goods bought with a total of GH₵ {top_qty:,} units,\n with {top_product} having sold {top_product_qty:,} units contributing to {percentage_of_product:.2f}% of the total volume\n\n"
                    insights += f"2. The month with the highest revenue is {top_month} with a total revenue of GH₵ {top_month_revenue:,.2f}\nwhich is a {revenue_percentage_change:.2f}% increase in our revenue compared to the previous month of {previous_top_month}\n\n"
                    insights += f"3. Total profit for the latest date ({latest_date}): GH₵ {total_profit_latest_date:,.2F}"
        
                    
                    return insights

                # Generate insights using the AI model
                insights = generate_insights(total_qty_per_category, mom_revenue, QTY_by_item, total_profits_over_time)
                
                

                st.text_area("TABLE AI Insights",insights,height=200)

                #st.plotly_chart(product_category_dominance,use_container_width=True)

            elif len(df) == 0:
                st.write("there is no data for that date")