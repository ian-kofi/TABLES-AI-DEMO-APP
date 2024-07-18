import INTENT_DETECTION_FOR_REPORTS

from datetime import datetime

def process_query(user_input):

    print(user_input)

    
    test_x = [user_input]
    docs = [INTENT_DETECTION_FOR_REPORTS.report_nlp(text) for text in test_x]
    test_x_vectors = [doc.vector for doc in docs] 
    report_prediction = INTENT_DETECTION_FOR_REPORTS.report_classify_svm.predict(test_x_vectors)
    print(report_prediction)




    return report_prediction