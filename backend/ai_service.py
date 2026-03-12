import ollama


def summarize_interview(text: str) -> str:
    prompt = f"""
你是资深升学顾问，请总结以下面谈：

输出格式：

1. 核心结论
2. 家长焦虑
3. 学生兴趣
4. 风险点
5. 待办事项

内容：
{text}
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"]
