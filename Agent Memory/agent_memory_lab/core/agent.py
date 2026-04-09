from langchain_community.llms import Ollama 
from core.memory_engine import SemanticMemory, EpisodicMemory
from utils.prompts import MEMORY_DECISION_PROMPT

class MemoryAgent:
    def __init__(self):
        self.llm = Ollama(model="llama3.1")
        self.semantic_memory = SemanticMemory()
        self.episodic_memory = EpisodicMemory()

    
    def handle_input(self, user_input):
        # 1. Decide memory type
        decision = self.llm.invoke(
            MEMORY_DECISION_PROMPT.format(user_input=user_input)
        ).strip()

        print(f"\n--- [MEMORY DECISION]: {decision} ---")

        # 2. Store accordingly
        if decision.startswith("SEMANTIC:"):
            fact = decision.replace("SEMANTIC:", "").strip()
            self.semantic_memory.save(fact)
            print(f"--- [SAVED TO SEMANTIC]: {fact}")

        elif decision.startswith("EPISODIC:"):
            event = decision.replace("EPISODIC:", "").strip()
            self.episodic_memory.save_event(event)
            print(f"--- [SAVED TO EPISODIC]: {event}")

        # 3. Retrieve both memories
        semantic_context = self.semantic_memory.search(user_input)
        episodic_context = self.episodic_memory.search(user_input)

        semantic_str = "\n".join(semantic_context) if semantic_context else "None"
        episodic_str = "\n".join(episodic_context) if episodic_context else "None"

        print(f"\n--- [SEMANTIC CONTEXT]: {semantic_str}")
        print(f"--- [EPISODIC CONTEXT]: {episodic_str}\n")

        # 4. Final reasoning
        final_prompt = f"""
            You are an intelligent assistant.
            Semantic Memory (Facts):
            {semantic_str}
            Episodic Memory (Past Events):
            {episodic_str}
            User Input:
            {user_input}
            Respond intelligently using BOTH types of memory.
        """

        return self.llm.invoke(final_prompt)