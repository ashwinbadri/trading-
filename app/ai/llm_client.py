import os

from openai import OpenAI


class LLMClient:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    def analyze_stock(
        self,
        symbol: str,
        current_price: float,
        day_change_percent: float,
        volume: int
    ):

        prompt = f"""
You are an AI trading analyst for a PAPER trading system.

Rules:
- This is paper trading only.
- Do not give real financial advice.
- Choose exactly one action: BUY, HOLD, or SELL.
- Return valid JSON only.
- Do not include markdown.

Stock data:
Symbol: {symbol}
Current Price: {current_price}
Day Change Percent: {day_change_percent}
Volume: {volume}

JSON schema:
{{
  "action": "BUY | HOLD | SELL",
  "confidence": 0.0,
  "reason": "short explanation"
}}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        return response.choices[0].message.content
