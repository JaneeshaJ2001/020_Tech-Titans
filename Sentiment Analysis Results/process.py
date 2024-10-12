import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from tqdm import tqdm
import os

# Load RoBERTa pre-trained model and tokenizer for sentiment analysis
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Function to get sentiment scores using RoBERTa
def get_sentiment_scores(comment):
    encoded_text = tokenizer(comment, return_tensors='pt', truncation=True, max_length=512)
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores 

# Function to classify sentiment
def classify_sentiment(scores):
    neg, neu, pos = scores
    if max(scores) == neg:
        return 'negative'
    elif max(scores) == neu:
        return 'neutral'
    else:
        return 'positive'

# Function to process an Excel file and calculate sentiment percentages
def process_excel_file(file_path):
    # Load Excel file and extract comments
    df = pd.read_excel(file_path)
    if 'Comment' not in df.columns:
        raise ValueError(f"'Comment' column not found in {file_path}")
    
    comments = df['Comments'].dropna().tolist()
    
    # Initialize counters
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}

    # Analyze sentiment for each comment
    for comment in tqdm(comments, desc=f"Processing {os.path.basename(file_path)}"):
        scores = get_sentiment_scores(comment)
        sentiment = classify_sentiment(scores)
        sentiment_counts[sentiment] += 1

    # Calculate percentages
    total_comments = len(comments)
    sentiment_percentages = {key: (value / total_comments) * 100 for key, value in sentiment_counts.items()}

    return sentiment_percentages

# List of Excel files to process
files = ['Ranil_cleaned.xlsx', 'namal_cleaned.xlsx', 'Ranil_cleaned.xlsx', 'sajith_cleaned.xlsx']

# Process each file and display results
for file in files:
    try:
        sentiment_percentages = process_excel_file(file)
        print(f"\nSentiment percentages for {file}:")
        print(f"Positive: {sentiment_percentages['positive']:.2f}%")
        print(f"Neutral: {sentiment_percentages['neutral']:.2f}%")
        print(f"Negative: {sentiment_percentages['negative']:.2f}%")
    except Exception as e:
        print(f"Error processing {file}: {e}")
