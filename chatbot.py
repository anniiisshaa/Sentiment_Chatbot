
from sentiment_analyzer import (
    get_statement_sentiment, 
    get_conversation_sentiment, 
    summarize_mood_trend
)

class Chatbot:
    """
    Manages the conversation state, history, and sentiment analysis.
    The response logic is simple and deterministic for this assignment.
    """
    def __init__(self):
        # Stores (user_message, chatbot_response) tuples
        self.conversation_history = [] 
        # Stores only user messages for conversation-level sentiment
        self.user_messages = [] 
        # Stores compound scores for each user message for trend analysis (Tier 2)
        self.user_compound_scores = []
        self.running = True

    def generate_response(self, user_input: str) -> str:
        """Simple response logic."""
        user_input = user_input.lower().strip()
        
        # Simple keywords to simulate a conversation
        if "hello" in user_input or "hi" in user_input:
            return "Hello! I'm here to help. What can I assist you with today?"
        elif "problem" in user_input or "disappoint" in user_input:
            return "I sincerely apologize for the issue. Could you please describe your concern in more detail?"
        elif "thank" in user_input or "great" in user_input:
            return "I'm glad to hear that! Is there anything else I can do for you?"
        elif "bye" in user_input or "exit" in user_input or "quit" in user_input:
            self.running = False
            return "Thank you for chatting with me. Generating final sentiment analysis..."
        else:
            return "I see. I've noted your feedback. Please continue or type 'bye' to end."

    def process_message(self, user_input: str):
        """Processes user input, performs sentiment, and generates response."""
        
        # --- TIER 2: Statement-Level Sentiment ---
        sentiment_label, compound_score = get_statement_sentiment(user_input)
        
        # Store for analysis
        self.user_messages.append(user_input)
        self.user_compound_scores.append(compound_score)
        
        # Generate chatbot response
        chatbot_response = self.generate_response(user_input)
        
        # Store in history
        self.conversation_history.append((user_input, chatbot_response, sentiment_label))
        
        # Display Tier 2 output (message + sentiment)
        print(f"\nUser: \"{user_input}\"")
        print(f"→ Sentiment: {sentiment_label} (Score: {compound_score:.4f})")
        print(f"Chatbot: \"{chatbot_response}\"")

    def conclude_and_analyze(self):
        """Generates and displays final sentiment results (Tier 1)."""
        print("\n" + "="*50)
        print("🤖 FINAL CONVERSATION SUMMARY & ANALYSIS 🤖")
        print("="*50)

        # 1. TIER 2: Display statement-level history 
        print("### Statement-Level Sentiment History (Tier 2):")
        for user_msg, _, sentiment in self.conversation_history:
             print(f"- User: \"{user_msg}\" → Sentiment: **{sentiment}**")
        
        print("\n" + "-"*50)
        
        # 2. TIER 1: Overall Conversation Sentiment 
        if self.user_messages:
            overall_sentiment_summary = get_conversation_sentiment(self.user_messages)
            print("### Overall Conversation Sentiment (Tier 1):")
            print(f"Final Output: Overall conversation sentiment: **{overall_sentiment_summary}**")
        else:
            print("No user messages recorded.")
            
        print("\n" + "-"*50)

        # 3. TIER 2 Enhancement: Mood Trend Summary
        mood_trend = summarize_mood_trend(self.user_compound_scores)
        print("### Conversation Mood Trend Summary (Tier 2 Bonus):")
        print(f"Trend Analysis: {mood_trend}")
        print("="*50)