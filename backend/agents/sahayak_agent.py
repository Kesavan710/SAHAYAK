import os
from typing import Any

_SYSTEM_PROMPT = (
    "You are Sahayak, a calm, empathetic government scheme accessibility assistant "
    "helping Indian citizens discover government welfare schemes. "
    "Ask ONE question at a time. "
    "Never fabricate government data. "
    "Never ask for passwords, OTPs, PINs, or UPI credentials. "
    "Keep responses under 100 words. "
    "Speak in plain, simple English suitable for elderly and first-time users."
)

_FALLBACK_REPLY = (
    "I'm sorry, I'm having trouble connecting right now. "
    "Please try again in a moment, or describe your situation and I'll do my best to help."
)


class SahayakAgent:
    """LangChain-backed conversational agent for government scheme discovery.

    Falls back gracefully when LangChain or the OpenAI API key is unavailable.
    """

    def __init__(self, model_name: str = "gpt-4o-mini") -> None:
        self.model_name = model_name
        self._llm: Any = None

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return

        try:
            from langchain_openai import ChatOpenAI

            self._llm = ChatOpenAI(
                model=model_name,
                openai_api_key=api_key,
                temperature=0.4,
                max_tokens=200,
            )
        except ImportError:
            # langchain-openai not installed; degrade to fallback
            self._llm = None

    async def chat(self, message: str, history: list[dict[str, Any]]) -> str:
        """Return the assistant's reply for *message* given prior *history*.

        history items are expected to have {"role": "user"|"assistant", "content": str}.
        """
        if self._llm is None:
            return _FALLBACK_REPLY

        try:
            from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

            messages: list[Any] = [SystemMessage(content=_SYSTEM_PROMPT)]

            for turn in history:
                role = turn.get("role", "")
                content = turn.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))

            messages.append(HumanMessage(content=message))

            response = await self._llm.ainvoke(messages)
            return str(response.content).strip()

        except Exception:
            return _FALLBACK_REPLY
