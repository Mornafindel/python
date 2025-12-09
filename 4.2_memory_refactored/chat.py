from api import call_zhipu_api
from roles import get_role_prompt, get_break_rules

def chat_once(history, user_input):
    """一次对话交互"""
    history.append({"role": "user", "content": user_input})
    result = call_zhipu_api(history)
    ai_reply = result["choices"][0]["message"]["content"]
    history.append({"role": "assistant", "content": ai_reply})
    return ai_reply
