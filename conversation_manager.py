"""
conversation_manager.py

The heart of Member 1's module. Given a user query, this:
  1. pulls relevant memories from the memory system
  2. builds a prompt combining those memories with the query + history
  3. calls the LLM
  4. stores the new turn back into memory
  5. returns the response
"""

from typing import Dict, List

from memory_interface import MemoryStoreInterface
from llm_connector import LLMConnector


class ConversationManager:
    def __init__(self, memory_store: MemoryStoreInterface, llm: LLMConnector):
        self.memory_store = memory_store
        self.llm = llm
        self.session_history: Dict[str, List[dict]] = {}  # user_id -> chat turns

    def _build_system_prompt(self, memories) -> str:
        if not memories:
            memory_block = "No prior memories are available for this user yet."
        else:
            memory_block = "\n".join(f"- {m.content}" for m in memories)

        return (
            "You are a helpful assistant with long-term memory of this user.\n"
            "Use the memories below only when they are relevant to the current "
            "message; do not force them in if they don't apply.\n\n"
            f"Relevant memories:\n{memory_block}"
        )

    def handle_query(self, user_id: str, user_message: str) -> str:
        # 1. Retrieve relevant memories from Member 2/3's module
        memories = self.memory_store.retrieve_relevant(user_id, user_message, top_k=5)

        # 2. Build the system prompt with memory context injected
        system_prompt = self._build_system_prompt(memories)

        # 3. Update this user's running conversation history
        history = self.session_history.setdefault(user_id, [])
        history.append({"role": "user", "content": user_message})

        # 4. Call the LLM
        response_text = self.llm.generate(system_prompt, history)

        # 5. Update history and persist the turn so memory can evolve from it
        history.append({"role": "assistant", "content": response_text})
        self.memory_store.store_interaction(user_id, user_message, response_text)

        return response_text
