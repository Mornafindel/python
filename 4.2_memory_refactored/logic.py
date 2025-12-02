def should_exit_by_user(user_input):
    """
    判断用户是否想要结束对话，返回 True/False。
    规则：若用户输入包含明确退出词（中文或英文）则返回 True。
    """
    if not isinstance(user_input, str):
        return False
    txt = user_input.strip().lower()
    exit_words = {"再见", "结束", "退出", "quit", "exit", "bye", "goodbye"}
    # 完全匹配或单词出现在输入里都认为是结束意图
    if txt in exit_words:
        return True
    for w in exit_words:
        if w in txt:
            return True
    return False

def should_exit_by_ai(ai_reply):
    """
    判断 AI 的回复是否表示要结束对话，返回 True/False。
    基本规则：若 AI 的回复恰好是“再见”或包含明显结束措辞，则认为 AI 要结束。
    """
    if not isinstance(ai_reply, str):
        return False
    txt = ai_reply.strip()
    if txt == "再见":
        return True
    txt_low = txt.lower()
    if any(k in txt_low for k in ("goodbye", "bye", "再见", "结束", "退出")):
        return True
    return False
