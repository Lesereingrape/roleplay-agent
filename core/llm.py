import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLM:
    def __init__(self, model="moonshot-v1-8k", temperature=0.7):
        self.client = OpenAI(
            api_key=os.getenv("MOONSHOT_API_KEY"),
            base_url="https://api.moonshot.cn/v1"
        )
        self.model = model
        self.temperature = temperature

    def generate(self, messages, tools=None):
        """生成回复，支持工具调用"""
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        if tools:
            params["tools"] = tools
        
        return self.client.chat.completions.create(**params)


# 向后兼容的函数
def call_llm(messages, model="moonshot-v1-8k"):
    llm = LLM(model=model)
    response = llm.generate(messages)
    return response.choices[0].message.content
