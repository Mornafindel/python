def should_exit_by_user(user_input):
    """判断用户是否想要结束对话"""
    return user_input.strip() in ["再见", "结束", "exit", "quit"]

def should_exit_by_ai(ai_reply):
    """判断AI是否想结束"""
    return "再见" == ai_reply.strip()
