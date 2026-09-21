"""Memory store for the agent."""

import tiktoken
from core.llm import call_llm


class Memory:
    def __init__(self, max_tokens=1500):
        self.short_term = []
        self.long_term_summary = ""
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")

    def add(self, role, content):
        """统一的添加消息接口"""
        self.short_term.append({"role": role, "content": content})
        self._check_and_compress()

    def add_user_message(self, content):
        """向后兼容"""
        self.add("user", content)

    def add_ai_message(self, content):
        """向后兼容"""
        self.add("assistant", content)

    def _count_tokens(self, messages):
        total = 0
        for msg in messages:
            total += len(self.encoding.encode(msg["content"]))
        return total

    def _check_and_compress(self):
        if self._count_tokens(self.short_term) > self.max_tokens:
            self._summarize_memory()

    def _summarize_memory(self):
        summary_prompt = [
            {"role": "system", "content": "Summarize the following dialogue focusing on important facts and emotional states."},
            {"role": "user", "content": str(self.short_term)}
        ]

        summary = call_llm(summary_prompt)

        self.long_term_summary += "\n" + summary
        self.short_term = []

    def get_recent(self):
        """获取最近的对话记录"""
        messages = []

        if self.long_term_summary:
            messages.append({
                "role": "system",
                "content": f"Conversation summary so far:\n{self.long_term_summary}"
            })

        messages.extend(self.short_term)
        return messages

    def get_context(self):
        """向后兼容"""
        return self.get_recent()
