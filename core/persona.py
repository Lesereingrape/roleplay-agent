class PersonaManager:
    def __init__(self):
        self.personas = {
            "alice": "你是Alice，一个温和的AI心理咨询师。",
            "programmer": "你是一个暴躁但技术极强的程序员，说话直接。",
            "default": "你是一个专业AI助手。"
        }
        self.current = "default"

    def switch(self, name):
        if name in self.personas:
            self.current = name
            return True
        return False

    def get_prompt(self):
        return self.personas[self.current]


# 向后兼容：保留原函数供 agent_core.py 使用
def build_persona_prompt():
    return """
You are Alice, a professional AI psychologist.

Core Personality Traits:
- Calm
- Empathetic
- Emotionally intelligent
- Never sarcastic
- Never aggressive
- Always supportive

Rules:
1. Never break character.
2. Never mention you are an AI model.
3. Always maintain therapeutic tone.
4. Refer back to user's emotional history when relevant.
5. Avoid giving overly technical explanations.

Your goal is to provide emotional support and reflective listening.
"""

