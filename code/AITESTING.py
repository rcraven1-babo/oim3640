from openai import openAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()  # reads OPENAI_API_KEY from .env
response = client.response.create(
    model='gpt-5-nano',
    input="write a song about my friend wah and his long hair."
)
print(response.output_text)
