import requests
import os
from requests.utils import stream_decode_response_unicode

# API Key 可从环境变量读取
API_KEY = os.environ.get("ZHIPU_API_KEY", "your_api_key_here")

def call_zhipu_api(messages, model="glm-4-flash"):
    """
    调用智谱 API 获取 AI 回复
    messages: 对话历史列表 [{"role":"user"/"assistant"/"system","content":"..."}]
    返回 JSON
    """
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.6
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API 调用失败: {response.status_code}, {response.text}")
