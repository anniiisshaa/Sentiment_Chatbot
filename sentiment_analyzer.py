
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import statistics
from typing import Tuple, List

# Initialize VADER (Valence Aware Dictionary and Sentiment Reasoner)
# VADER is a rule-based tool optimized for social media/short text.
# It returns a 'compound' score between -1 (very negative) and +1 (very positive).

analyzer = SentimentIntensityAnalyzer()

def classify_sentiment(compound_score: float) -> str:
    """Classifies a VADER compound score into a simple label."""
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# --- TIER 2 Implementation (Statement-Level) ---
def get_statement_sentiment(text: str) -> Tuple[str, float]: # Note the capital 'T' in Tuple
    """
    Performs sentiment analysis on a single user statement.
    Returns: (Sentiment_Label, Compound_Score)
    """
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']
    sentiment_label = classify_sentiment(compound_score)
    return sentiment_label, compound_score

# --- TIER 1 Implementation (Conversation-Level) ---
def get_conversation_sentiment(user_messages: List[str]) -> str:
    """
    Performs sentiment analysis on the entire conversation history.
    1. Concatenates all messages into one text block.
    2. Calculates the overall sentiment based on the aggregate text.
    3. Provides a final descriptive summary (Optional enhancement for Tier 1).
    """
    # Join all user messages into a single string for overall analysis
    full_text = " ".join(user_messages)
    
    # Calculate sentiment for the entire conversation text
    scores = analyzer.polarity_scores(full_text)
    overall_compound_score = scores['compound']
    
    # Simple classification 
    simple_sentiment = classify_sentiment(overall_compound_score)
    
    # descriptive summary 
    if overall_compound_score > 0.6:
        descriptive_summary = f"{simple_sentiment} - Strong Satisfaction"
    elif overall_compound_score > 0.2:
        descriptive_summary = f"{simple_sentiment} - General Contentment"
    elif overall_compound_score < -0.6:
        descriptive_summary = f"{simple_sentiment} - Significant Dissatisfaction"
    elif overall_compound_score < -0.2:
        descriptive_summary = f"{simple_sentiment} - Mild Concern/Dissatisfaction"
    else:
        descriptive_summary = f"{simple_sentiment} - Balanced/Neutral Exchange"
        
    return descriptive_summary

# --- TIER 2 Enhancement (Mood Trend) ---
def summarize_mood_trend(compound_scores: List[float]) -> str:
    """
    Summarises the trend or shift in mood across the conversation.
    This function analyzes the list of individual message scores.
    """
    if not compound_scores or len(compound_scores) < 2:
        return "Not enough data to determine a trend."

    # Compare the average of the first half vs. the second half
    midpoint = len(compound_scores) // 2
    first_half_avg = statistics.mean(compound_scores[:midpoint])
    second_half_avg = statistics.mean(compound_scores[midpoint:])
    
    delta = second_half_avg - first_half_avg

    if delta > 0.2:
        trend = "Mood noticeably **improved**."
    elif delta < -0.2:
        trend = "Mood noticeably **declined**."
    elif abs(delta) > 0.05:
        trend = "Mood had a slight shift."
    else:
        trend = "Mood remained largely stable."
    
    return trend
