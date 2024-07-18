import spacy
from sklearn import svm


report_nlp = spacy.load("en_core_web_lg")

class report_type:
    SALES_REPORT = "SALES_REPORT"
    FINANCIAL_REPORT = "FINANCIAL_REPORT"
    INVENTORY_REPORT = "INVENTORY_REPORT"
    PRODUCT_REPORT = "PRODUCT_REPORT"
    

training_text_2 = [ "Generate a sales report for the last quarter",
                    "show me the weekly sales performance report",
                    "i need a sales report comparing this month to the previous month",
                    "get me a sales report for q2",

                    "Can you provide a financial summary for the past year?",
                    "Generate a profit and loss statement for Q2.",
                    "I need a detailed expense report for the last month.",
                    "generate a financial report for the last quarter,"
                 ]
training_report_type = [report_type.SALES_REPORT,
                        report_type.SALES_REPORT,
                        report_type.SALES_REPORT,
                        report_type.SALES_REPORT,

                        report_type.FINANCIAL_REPORT,
                        report_type.FINANCIAL_REPORT,
                        report_type.FINANCIAL_REPORT,
                        report_type.FINANCIAL_REPORT,
                        ]

docs = [report_nlp(text) for text in training_text_2]
training_vectors = [x.vector for x in docs]
report_classify_svm = svm.SVC(kernel="linear")

report_classify_svm.fit(training_vectors,training_report_type)