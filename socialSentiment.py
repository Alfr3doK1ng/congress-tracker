import tweepy
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Twitter API credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Authenticate Twitter API
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Load pre-trained model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

def scrape_twitter_for_stock_tweets(query, count=10):
    tweets = api.search(q=query, count=count, lang='en')
    return [(tweet.created_at, tweet.text) for tweet in tweets]

def analyze_sentiment_bert(tweet_texts):
    # Set the model to evaluation mode
    model.eval()
    
    sentiments = []
    for tweet_text in tweet_texts:
        # Tokenize the tweet and convert it to input IDs
        inputs = tokenizer.encode_plus(tweet_text, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"]

        # Perform inference
        with torch.no_grad():
            outputs = model(input_ids)
        
        # Get the predicted label (0 for negative, 1 for positive)
        predicted_label = torch.argmax(outputs[0]).item()

        # Map predicted label to sentiment
        sentiment = "positive" if predicted_label == 1 else "negative"
        
        sentiments.append(sentiment)
    
    return sentiments

if __name__ == "__main__":
    # Sample query related to stock trading
    query = "stock trading OR financial market"
    
    # Scrape Twitter for tweets related to stock trading
    stock_tweets = scrape_twitter_for_stock_tweets(query, count=20)
    
    # Extract tweet texts
    tweet_texts = [tweet_text for _, tweet_text in stock_tweets]
    
    # Analyze sentiments of scraped tweets
    tweet_sentiments = analyze_sentiment_bert(tweet_texts)
    
    # Print scraped tweets with sentiment analysis
    for i, (created_at, tweet_text) in enumerate(stock_tweets):
        print(f"Timestamp: {created_at}\nTweet: {tweet_text}\nSentiment: {tweet_sentiments[i]}\n")
