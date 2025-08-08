import os
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_financial_summary(prompt_text) -> str:
    prompt = f"""
You are a financial analyst. Independently research and analyze the company described below.
Provide a detailed report covering fundamentals, risks, opportunities, and technical analysis of the stock.
Conclude with a clear recommendation: BUY, HOLD, or SELL as of today.

Company Information:
{prompt_text}

Please be concise but thorough, and finish with your recommendation.
"""

    params = dict(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=1,               # Must be 1 for GPT-5 currently
        max_completion_tokens=1000,
        # verbosity="medium",        # Uncomment to test if supported
        # reasoning_effort="medium", # Uncomment to test if supported
    )

    try:
        response = client.chat.completions.create(**params)
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = str(e)
        # If error mentions unsupported parameter/value, retry without optional params
        if ("unsupported" in error_msg.lower() or "does not support" in error_msg.lower()) and ("verbosity" in error_msg.lower() or "reasoning_effort" in error_msg.lower()):
            # Remove optional params and retry once
            print("Retrying without verbosity and reasoning_effort due to unsupported parameter error.")
            for key in ["verbosity", "reasoning_effort"]:
                if key in params:
                    del params[key]
            try:
                response = client.chat.completions.create(**params)
                return response.choices[0].message.content.strip()
            except Exception as e2:
                return f"Error calling ChatGPT API on retry: {str(e2)}"
        # If error mentions temperature unsupported value, retry with temperature=1
        elif "temperature" in error_msg.lower():
            print("Retrying with temperature=1 due to unsupported temperature value.")
            params["temperature"] = 1
            try:
                response = client.chat.completions.create(**params)
                return response.choices[0].message.content.strip()
            except Exception as e3:
                return f"Error calling ChatGPT API on retry: {str(e3)}"
        else:
            return f"Error calling ChatGPT API: {error_msg}"
