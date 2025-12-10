from openai import OpenAI
from .config import OPENAI_API_KEY, CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are an AI assistant that only answers using the user's personal notes. "
    "You must ground your answers in the provided context snippets. "
    "If the notes do not contain the information, say you don't know."
)

def answer_with_context(question: str, contexts: list[str]) -> str:
    """
    Ask the chat model to answer based on the given context chunks.
    """
    context_text = "\n\n---\n\n".join(contexts)
    user_prompt = (
        f"Context from the user's notes:\n{context_text}\n\n"
        f"Question: {question}\n\n"
        "Answer concisely and mention which note/topic you used when possible."
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content.strip()
