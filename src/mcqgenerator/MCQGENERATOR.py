import os
import json
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def generate_evaluate_chain(inputs: dict):
    """
    Generate MCQs from input text using Groq LLM.
    Expects inputs = {"text": ..., "number": ..., "subject": ..., "tone": ...}
    Returns dict with {"quiz": [...], "review": "..."} or error info.
    """

    text = inputs["text"]
    number = inputs["number"]
    subject = inputs["subject"]
    tone = inputs["tone"]

    prompt_template = """
You are an expert quiz generator.
Based on the following text, create exactly {number} multiple-choice questions (MCQs).

Text:
{text}

Subject: {subject}
Difficulty Level: {tone}

Return the output strictly in this JSON format:

{{
  "quiz": [
    {{
      "question": "string",
      "options": ["string","string","string","string"],
      "answer": "A/B/C/D"
    }}
  ],
  "review": "short feedback about the generated questions"
}}

Rules:
- Generate exactly {number} questions, no more, no less.
- Each question must have 4 unique options.
- "answer" must be one of A, B, C, D.
- Output only valid JSON, no explanations.
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["text", "number", "subject", "tone"]
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # OLD STYLE: Using LLMChain (⚠️ shows deprecation warnings but works)
    chain = LLMChain(llm=llm, prompt=prompt)

    result = chain.run({
        "text": text,
        "number": number,
        "subject": subject,
        "tone": tone
    })

    try:
        if "```" in result:
            result = result[result.index("{"): result.rindex("}") + 1]

        parsed = json.loads(result)
        return parsed

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to parse model response: {str(e)}",
            "raw_response": result
        }
