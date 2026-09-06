"""
llm_connector.py

Thin wrapper around the LLM API so the rest of the app doesn't care
which provider is behind it. Set your API key as an environment
variable before running:

    export ANTHROPIC_API_KEY="sk-ant-..."
    # or
    export OPENAI_API_KEY="sk-..."
"""

import os
from typing import List, Dict


class LLMConnector:
    def __init__(self, provider: str = "anthropic", model: str = "claude-sonnet-4-6"):
        self.provider = provider
        self.model = model

        if provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        elif provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def generate(self, system_prompt: str, conversation: List[Dict[str, str]], max_tokens: int = 1000) -> str:
        """
        conversation: list of {"role": "user"|"assistant", "content": str},
        in chronological order, most recent message last.
        """
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=conversation,
            )
            return response.content[0].text

        elif self.provider == "openai":
            messages = [{"role": "system", "content": system_prompt}] + conversation
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
