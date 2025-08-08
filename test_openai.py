from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Explain the basics of financial analysis."}]
)

print("Response content:", response.choices[0].message.content)

