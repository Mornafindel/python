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


while True:
    user_input = input("请输入你要说的话：")
    

    messages = [
        {"role": "system", "content": "你是一个智能对话模型。在多轮对话中，当你**明确判断**用户想要结束对话时（例如用户说'再见'、'我要去吃饭了'等），你的回复内容**必须包含**『再见』二字。在其他情况下，请保持正常的对话回复。"}, 
        {"role": "user", "content": user_input}
    ]

    try:
        result = call_zhipu_api(messages)
        ai_response = result['choices'][0]['message']['content']
    
        print(ai_response)
    
       
        normalized_response = ai_response.lower()

        if "再见" in normalized_response: 
            print("对话结束。")
            break
            
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        break