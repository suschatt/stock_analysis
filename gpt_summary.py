import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_financial_summary(prompt_text) -> str:
    """
    Calls GPT-5 to perform an independent financial and technical analysis 
    with a buy/hold/sell recommendation based solely on prompt_text.
    """

    prompt = f"""
You are a financial analyst. Independently research and analyze the company described below.
Provide a detailed report covering fundamentals, risks, opportunities, and technical analysis of the stock.
Conclude with a clear recommendation: BUY, HOLD, or SELL as of today.

Company Information:
{prompt_text}

Please be concise but thorough, and finish with your recommendation.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling ChatGPT API: {str(e)}"
