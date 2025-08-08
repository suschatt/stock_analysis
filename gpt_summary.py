import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def metrics_table(metrics: dict) -> str:
    """Format metrics dict into a markdown table string with values and scores."""
    lines = ["| Metric | Value | Score (out of 10) |", "|---|---|---|"]
    for metric, data in metrics.items():
        if isinstance(data, dict):
            val = data.get("value", "N/A")
            sc = data.get("score", "N/A")
        else:
            val = data
            sc = "N/A"
        lines.append(f"| {metric} | {val} | {sc} |")
    return "\n".join(lines)

def get_financial_summary(prompt_text, fh_score, fh_breakdown, buff_score, buff_breakdown, lynch_score, lynch_breakdown) -> str:
    """Call GPT with detailed prompt including financial scores and request a buy/hold/sell recommendation."""

    prompt = f"""
You are a financial analyst. Analyze the company based on these financial scores and breakdowns. Provide a detailed analysis covering strengths, weaknesses, risks, and opportunities. Finally, give a clear recommendation: BUY, HOLD, or SELL as of today.

## Summary Scores
- Financial Health Score: {fh_score:.2f}/10
- Buffett Score: {buff_score:.2f}/10
- Lynch Score: {lynch_score:.2f}/10

## Balance Sheet Breakdown
{metrics_table(fh_breakdown)}

## Buffett Breakdown
{metrics_table(buff_breakdown)}

## Lynch Breakdown
{metrics_table(lynch_breakdown)}

## Additional Notes
{prompt_text}

Please keep the analysis concise but thorough, and finish with your recommendation.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        # Response content is accessed via .choices[0].message.content for new OpenAI SDK
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling ChatGPT API: {str(e)}"
