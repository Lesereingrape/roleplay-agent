import json

from core.llm import LLM
from core.memory import Memory
from core.persona import PersonaManager
from core.tools import tools, execute_tool

llm = LLM()
memory = Memory()
persona = PersonaManager()

print("Agent started. Type /role name to switch persona.")

while True:
    user_input = input("You: ")

    # 处理命令
    if user_input.startswith("/role"):
        _, role_name = user_input.split()
        if persona.switch(role_name):
            print(f"Switched to {role_name}")
        else:
            print("Role not found")
        continue

    # 构造消息结构
    messages = [
        {"role": "system", "content": persona.get_prompt()}
    ]

    messages += memory.get_recent()
    messages.append({"role": "user", "content": user_input})

    response = llm.generate(messages, tools=tools)

    message = response.choices[0].message

    # 判断是否调用工具
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        result = execute_tool(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )

        messages.append(message)
        messages.append({
            "role": "tool",
            "content": result,
            "tool_call_id": tool_call.id
        })

        final_response = llm.generate(messages)
        output = final_response.choices[0].message.content

    else:
        output = message.content

    print("Agent:", output)

    memory.add("user", user_input)
    memory.add("assistant", output)

