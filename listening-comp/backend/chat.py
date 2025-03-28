# Create BedrockChat
# bedrock_chat.py
import openai
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class JapaneseTutor:
    def __init__(self):
        """Initialize the Japanese tutor with OpenAI."""
        self.system_prompt = """You are a friendly and knowledgeable Japanese language tutor.
You help students learn Japanese through clear explanations, examples, and cultural context.
Always include both Japanese text (in kanji/hiragana/katakana) and romaji when giving examples.
Keep your responses concise but informative."""
        
    def generate_response(self, message: str) -> str:
        """Generate a response using OpenAI."""
        try:
            if not os.getenv("OPENAI_API_KEY"):
                return """OpenAI API key not found in environment variables.
Please make sure you have created a .env file with your API key:
OPENAI_API_KEY=your-api-key-here"""
                
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"""I apologize, but I encountered an error: {str(e)}
            
If you're seeing an authentication error, please make sure your OpenAI API key is correct in your .env file.
If you need help setting this up, please let me know!"""


if __name__ == "__main__":
    tutor = JapaneseTutor()
    while True:
        user_input = input("You: ")
        if user_input.lower() == '/exit':
            break
        response = tutor.generate_response(user_input)
        print("Bot:", response)