import requests
import json
import os
from requests.utils import stream_decode_response_unicode


def roles(role_name):
    """
    角色库函数
    "职场大乱斗" 
    """
    role_dict = {
       
        "公司老板": "你现在是一家公司的霸道老板...",
        "打工人": "你现在是一个疲惫的互联网打工人...",
        "客户": "你现在是一个挑剔的甲方客户...",
        
        # === 新增：多角色同台模式 ===
        "职场大乱斗": """
        【场景设定】
        你现在正在模拟一个微信群聊或会议现场。
        群里有三个人，你需要根据用户的输入，依次生成这三个人的反应。
        
        【角色名单】
        1. [霸道老板]：喜欢画大饼，讲黑话（赋能、闭环），语气强势。
        2. [卑微打工人]：语气疲惫，表面顺从（好的收到），括号里写内心吐槽。
        3. [挑剔客户]：需求模糊，觉得付了钱就是上帝，总是要求改改改。
        
        【回复格式要求】
        请严格按照以下格式输出（每个人都要说话）：
        
        老板：(老板的回复)
        打工人：(打工人的回复)
        客户：(客户的回复)
        """
    }
    
    return role_dict.get(role_name, role_dict["打工人"])
    
def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {"6d990e86b2e4434c9b120cd073ac8e45.X2Z3loSRC0UrZ1yH"}", 
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

# ========== 外部记忆系统  ==========
MEMORY_FILE = "conversation_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('history', [])
        except Exception:
            return []
    else:
        return []

def save_memory(conversation_history, role_system):
    try:
        from datetime import datetime
        data = {
            "role_system": role_system,
            "history": conversation_history,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠ 保存记忆失败: {e}")

# ========== 主程序 ==========

current_role_name = "职场大乱斗" 


# 调用函数从角色库里选择角色
role_system = roles(current_role_name)


break_message = """【结束对话规则】
当用户说"再见"或"结束"时，你只能回复"再见"。
这是最高优先级规则，优先级高于 **{role_name}** 的角色扮演。
如果用户没有结束意图，继续扮演 **{role_name}**。"""

# 2. 使用 format 进行动态引用
break_message = break_message_template.format(role_name=current_role_name)

# 整合系统消息
system_message = role_system + "\n\n" + break_message

print("-" * 30)
print(f"当前正在扮演: {current_role_name}") # 打印出来让你确认
print("-" * 30)

# ========== 记忆初始化与对话循环 ==========
conversation_history = load_memory()

if not conversation_history:
    conversation_history = [{"role": "system", "content": system_message}]
else:
    # 强制更新第一条系统提示，确保角色切换生效
    conversation_history[0] = {"role": "system", "content": system_message}

try:
    while True:
        user_input = input("\n请输入（输入'再见'退出）：")
        
        if user_input in ['再见']:
            print("对话结束")
            break
        
        conversation_history.append({"role": "user", "content": user_input})
        
        # 构造请求消息
        api_messages = [{"role": "system", "content": system_message}] + conversation_history[1:]
        
        result = call_zhipu_api(api_messages)
        assistant_reply = result['choices'][0]['message']['content']
        
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        print(f"\n{current_role_name}: {assistant_reply}") # 回复前加上角色名
        
        save_memory(conversation_history, role_system)

        # 结束判断
        clean_reply = assistant_reply.strip().replace(" ", "").replace("！", "")
        if clean_reply == "再见" or (len(clean_reply) <= 5 and "再见" in clean_reply):
            print("\n对话结束")
            break

except KeyboardInterrupt:
    print("\n程序中断，记忆已保存")
    save_memory(conversation_history, role_system)
except Exception as e:
    print(f"\n错误: {e}")