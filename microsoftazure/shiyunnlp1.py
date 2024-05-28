# https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/quickstart?tabs=macos&pivots=programming-language-python
# export LANGUAGE_KEY=your-key
# export LANGUAGE_ENDPOINT=your-endpoint
# source ~/.bash_profile 
# unset LANGUAGE_KEY
# unset LANGUAGE_ENDPOINT

# azure.ai.textanalytics documentation: https://pypi.org/project/azure-ai-textanalytics/5.1.0/
# resolved eror by changing python interpretor to anocanda one.
import os
# Access the environment variables
language_key = os.getenv('LANGUAGE_KEY')
language_endpoint = os.getenv('LANGUAGE_ENDPOINT')
# print(language_key, language_endpoint)

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
text_analytics_client = TextAnalyticsClient(language_endpoint, AzureKeyCredential(language_key))

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for detecting sentiment and opinions in text 
def sentiment_analysis_with_opinion_mining_example(client):

    documents = [
        "The food and service were unacceptable. The concierge was nice, however."
    ]

    result = client.analyze_sentiment(documents, show_opinion_mining=True)
    doc_result = [doc for doc in result if not doc.is_error]

    positive_reviews = [doc for doc in doc_result if doc.sentiment == "positive"]
    negative_reviews = [doc for doc in doc_result if doc.sentiment == "negative"]

    positive_mined_opinions = []
    mixed_mined_opinions = []
    negative_mined_opinions = []

    for document in doc_result:
        print("Document Sentiment: {}".format(document.sentiment))
        print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
            document.confidence_scores.positive,
            document.confidence_scores.neutral,
            document.confidence_scores.negative,
        ))
        for sentence in document.sentences:
            print("Sentence: {}".format(sentence.text))
            print("Sentence sentiment: {}".format(sentence.sentiment))
            print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
                sentence.confidence_scores.positive,
                sentence.confidence_scores.neutral,
                sentence.confidence_scores.negative,
            ))
            for mined_opinion in sentence.mined_opinions:
                target = mined_opinion.target
                print("......'{}' target '{}'".format(target.sentiment, target.text))
                print("......Target score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                    target.confidence_scores.positive,
                    target.confidence_scores.negative,
                ))
                for assessment in mined_opinion.assessments:
                    print("......'{}' assessment '{}'".format(assessment.sentiment, assessment.text))
                    print("......Assessment score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                        assessment.confidence_scores.positive,
                        assessment.confidence_scores.negative,
                    ))
            print("\n")
        print("\n")

## Result:          
# sentiment_analysis_with_opinion_mining_example(client)

# Document Sentiment: mixed
# Overall scores: positive=0.43; neutral=0.04; negative=0.53 

# Sentence: The food and service were unacceptable. 
# Sentence sentiment: negative
# Sentence score:
# Positive=0.00
# Neutral=0.01
# Negative=0.99

# ......'negative' target 'food'
# ......Target score:
# ......Positive=0.01
# ......Negative=0.99

# ......'negative' assessment 'unacceptable'
# ......Assessment score:
# ......Positive=0.01
# ......Negative=0.99

# ......'negative' target 'service'
# ......Target score:
# ......Positive=0.01
# ......Negative=0.99

# ......'negative' assessment 'unacceptable'
# ......Assessment score:
# ......Positive=0.01
# ......Negative=0.99



# Sentence: The concierge was nice, however.
# Sentence sentiment: positive
# Sentence score:
# Positive=0.86
# Neutral=0.08
# Negative=0.07

# ......'positive' target 'concierge'
# ......Target score:
# ......Positive=1.00
# ......Negative=0.00

# ......'positive' assessment 'nice'
# ......Assessment score:
# ......Positive=1.00
# ......Negative=0.00
