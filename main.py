
from chatbot import Chatbot

if __name__ == "__main__":
    
    # Initialize the Chatbot
    bot = Chatbot()
    
    print("--- LiaPlus Sentiment Chatbot ---")
    print("Start chatting. Type 'bye' or 'exit' to end the session.")
    
    # Main Chat Loop
    while bot.running:
        try:
            user_input = input("\n[User]: ")
            if not user_input.strip():
                continue
                
            bot.process_message(user_input)
            
        except EOFError:
            # Handles Ctrl+D/Ctrl+Z termination
            bot.running = False
        except KeyboardInterrupt:
            # Handles Ctrl+C termination
            bot.running = False
    
    # Run the final analysis (Tier 1 Mandatory)
    bot.conclude_and_analyze()