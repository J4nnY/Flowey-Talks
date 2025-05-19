from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
import torch
from scipy.special import softmax

# Load model and tokenizer
# MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
SAVE_DIR = "./local_model"
tokenizer = AutoTokenizer.from_pretrained(SAVE_DIR)
model = AutoModelForSequenceClassification.from_pretrained(SAVE_DIR)
config = AutoConfig.from_pretrained(SAVE_DIR)

# tokenizer.save_pretrained(SAVE_DIR)
# model.save_pretrained(SAVE_DIR)

# Function to clean Twitter text
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = "@user" if t.startswith("@") else t
        t = "http" if t.startswith("http") else t
        new_text.append(t)
    return " ".join(new_text)

# Function to analyze sentiment
def analyze_sentiment(text):
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        output = model(**encoded_input)
    scores = softmax(output.logits[0].numpy())

    # Print sentiment scores
    results = {config.id2label[i]: float(scores[i]) for i in range(len(scores))}
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return sorted_results

# Example usage
# prompt = "Good day"
# sentiment = analyze_sentiment(prompt)
# print(sentiment)