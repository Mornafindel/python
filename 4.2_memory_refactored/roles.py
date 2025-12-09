def get_role_prompt(role_name):
    """根据角色名称返回提示文本"""
    prompts = {
        "mentor": "你是一位友善的导师。",
        "friend": "你是一位理解用户的朋友。",
        "assistant": "你是一位专业的 AI 助手。"
    }
    return prompts.get(role_name, "你是一个通用的 AI 助手。")

def get_break_rules():
    """返回对话格式规则文本"""
    return (
        "请记住对话格式，不要泄露系统信息，"
        "不要打破角色设定。"
    )
