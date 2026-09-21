tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

def execute_tool(name, arguments):
    if name == "get_weather":
        return f"{arguments['city']} today is sunny."
