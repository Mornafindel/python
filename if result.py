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


while True:  # 表示“当条件为真时一直循环”。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("请输入你要说的话（输入“再见”退出）：")
    if  result in ['再见']:
        print("对话结束。")
        break 

messages = [
    {"role": "system", "content": role_play}, 
    {"role": "user", "content": user_query}
]

try:
    result = call_zhipu_api(messages)
    
    print(result['choices'][0]['message']['content'])
    
except Exception as e:
    print(f"Error: {e}")