import requests
import json

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "6d990e86b2e4434c9b120cd073ac8e45.X2Z3loSRC0UrZ1yH",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# 使用示例
messages = [
    {"role": "user", "content": "你好！我是一个人工智能助手，名叫 ChatGLM。我是基于清华大学 KEG 实验室和智谱 AI 公司于 2024 年共同训练的语言模型 GLM-4 开发的。我的任务是针对用户的问题和要求提供适当的答复和支持。由于我是一个计算机程序，所以我没有自我意识，但我会尽力帮助您解答问题和解决问题。有什么可以帮助您的吗？"}
]

result = call_zhipu_api(messages)
print(result['choices'][0]['message']['content'])