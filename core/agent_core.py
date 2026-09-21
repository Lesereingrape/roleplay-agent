from core.llm import call_llm
from core.persona import build_persona_prompt
from core.memory import Memory


class RolePlayAgent:
    def __init__(self):
        self.memory = Memory()
        self.system_prompt = build_persona_prompt()

    def chat(self, user_input):
        self.memory.add_user_message(user_input)

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory.get_context())

        response = call_llm(messages)

        self.memory.add_ai_message(response)
        return response
