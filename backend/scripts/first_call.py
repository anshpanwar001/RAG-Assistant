"""
A standalone script to test the LLM client from the terminal.

Scripts like this are useful throughout the project: they let you test one
piece without starting the whole web server.
"""

from app.llm.gemini_client import LLMError, get_llm_client

SYSTEM_INSTRUCTION = (
    "You are a helpful assistant for learners. "
    "Answer in at most three short sentences."
)

QUESTION = "In plain language, what is Retrieval-Augmented Generation?"


def main() -> None:
    llm = get_llm_client()
    print("Answer:\n")
    for piece in llm.stream(QUESTION, system_instruction=SYSTEM_INSTRUCTION):
        print(piece, end="", flush=True)  # flush so each piece appears immediately
    print()


if __name__ == "__main__":
    try:
        main()
    except LLMError as error:
        print(f"Error: {error}")
        raise SystemExit(1)