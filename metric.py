#Metric = w_s * S + w_l * L + w_a * A + w_r * R + w_u * U
from textblob import TextBlob
import pandas as pd


def email_class(eclass):
    if eclass in ["Fraudulent", "Harrassment"]:
        return 2
    elif eclass == 'Suspicious':
        return 1
    else:
        return 0

def reputation_count(csv_file):
    data = pd.read_csv(csv_file)
    normal_count = data[data['Email Class'] == 'Normal'].shape[0]
    num_emails = data.shape[0]
    if num_emails - normal_count > 10 or normal_count//num_emails > 0.05:
        return 1
    return 0


def sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    if sentiment.polarity > 0:
        return 1
    elif sentiment.polarity < 0:
        return -1
    return 0

def urgency(email_text):
    urgency_keywords = ["urgent", "important", "deadline", "asap", "priority", "critical", "immediate"]
    lower_email_text = email_text.lower()
    urgency_count = sum(keyword in lower_email_text for keyword in urgency_keywords)
    
    if urgency_count > 0:
        return 1
    return 0

def email_length(email_text):
    if len(email_text)>500:
        return 1
    return 0

def sender_reputation(csv_file):
    data = pd.read_csv(csv_file)
    normal_count = data[data['Email Class'] == 'Normal'].shape[0]
    num_emails = data.shape[0]
    if num_emails - normal_count > 10 or normal_count//num_emails > 0.05:
        return 1
    return 0

def attachment_present(attachment):
    if attachment:
        return 1
    else:
        return 0
    
