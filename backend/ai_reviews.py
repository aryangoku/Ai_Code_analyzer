import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def review_code(code):

    prompt = f"""
    Analyze the following code and provide:
    - potential bugs
    - performance improvements
    - code quality suggestions

    Code:
    {code[:2000]}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content