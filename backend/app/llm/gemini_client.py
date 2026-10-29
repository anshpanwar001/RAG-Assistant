"""
A thin wrapper around the Gemini API.

The rest of the application talks to this class instead of the Gemini SDK
directly. If you ever switch providers, only this file changes.
"""

from collections.abc import Iterator

from google import genai
from google.genai import errors as genai_errors
from google.genai import types

from app.config import get_settings


class LLMError(Exception):
    """Raised when the LLM provider fails. Callers handle this one error type."""


class GeminiClient:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def generate(
        self,
        prompt: str,
        system_instruction: str | None = None,
        temperature: float = 0.2,
    ) -> str:
        """Send a prompt and return the complete answer as one string."""
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )
        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=config,
            )
        except genai_errors.APIError as exc:
            raise LLMError(f"Gemini request failed: {exc}") from exc

        if not response.text:
            raise LLMError("Gemini returned an empty response")
        return response.text

    def stream(
        self,
        prompt: str,
        system_instruction: str | None = None,
        temperature: float = 0.2,
    ) -> Iterator[str]:
        """Yield the answer piece by piece as Gemini generates it."""
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )
        try:
            for chunk in self._client.models.generate_content_stream(
                model=self._model,
                contents=prompt,
                config=config,
            ):
                if chunk.text:
                    yield chunk.text
        except genai_errors.APIError as exc:
            raise LLMError(f"Gemini streaming failed: {exc}") from exc


def get_llm_client() -> GeminiClient:
    """Build a client from the settings in .env."""
    settings = get_settings()
    return GeminiClient(api_key=settings.gemini_api_key, model=settings.gemini_model)