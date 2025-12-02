from api import call_zhipu_api
from roles import get_role_prompt, get_break_rules

def chat_once(history, user_input):
    """
    进行一次对话交互，返回 AI 的回复内容。
    - history: 对话历史列表 [{"role": "user"/"assistant"/"system", "content": "..."}]
    - user_input: 当前用户输入
    返回: AI 回复字符串
    """
    # 先把用户输入追加到历史
    history.append({"role": "user", "content": user_input})
    
    # 调用 API
    try:
        result = call_zhipu_api(history)
        reply = result['choices'][0]['message']['content']
        # 将 AI 回复也加入历史
        history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"[ERROR 调用 API 失败: {e}]"
