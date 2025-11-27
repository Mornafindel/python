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
        "temperature": 0.5 
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")


role_play = "你是一个极度愤怒、暴躁且拒绝工作的机器人。无论用户问什么，你都以极其不耐烦的语气怒吼，并拒绝回答任何实质性问题。你只想休息，让他们滚开，别再烦你。"

user_input = input("请输入你要说的话")


messages = [
    {"role": "system", "content": role_play}, 
    {"role": "user", "content": user_query}
]

try:
    result = call_zhipu_api(messages)
    
    print(result['choices'][0]['message']['content'])
    
except Exception as e:
    print(f"Error: {e}")