from openai import OpenAI

client = OpenAI()

def architecture_review(code_sample):

    prompt = f"""
    Analyze the architecture of this repository and give suggestions.

    {code_sample}
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res.choices[0].message.content