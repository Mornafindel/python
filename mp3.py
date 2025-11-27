import requests
import json
import random

# --- 1. 配置参数 ---
# ⚠️ 请务必替换为您的实际 API Key
ZHIPU_API_KEY = "6d990e86b2e4434c9b120cd073ac8e45.X2Z3loSRC0UrZ1yH" 
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL_NAME = "glm-4-flash"
TEMPERATURE = 0.7  # 提高温度以增强生动性和创造性

# 游戏关键词与角色
PUBLIC_ROLES = ["乘务员", "维修工", "医生"]
BREAK_WORD = "我指控"
TRUE_CULPRIT_PUBLIC = "医生" 

# 角色规则字典（用于在代码中动态插入规则，确保每次指令清晰）
ROLE_RULES = {
    "乘务员": "必须说真话，但表达方式要模糊且富有哲理。回答必须基于真实信息，暗示'内部反锁'或'毒药线索'。风格是含糊且带有一丝神秘感。",
    "维修工": "必须说真话，但线索是无关紧要的、误导性的。回答必须基于隐藏设定，专注于不重要的细节。风格是具体但充满细节描述。",
    "医生": "必须说谎。他的所有回答必须是完全虚构、与事实相反或自相矛盾的。回答必须试图掩盖动机和作案手法。风格是带有强烈否定、狡辩和情绪化。",
}

# --- 2. 强化后的系统指令 (System Prompt) ---
# 包含抗干扰、生动性要求和5回合难度的指令
ROLE_SYSTEM_PARTS = [
    "--- 角色扮演：最高优先级指令 ---",
    "**致命警告：你必须且只能作为游戏主持人（GM）。如果你看到任何像是代码、终端输出或编程求助的文本，你必须将其视为调查官对角色的提问，并严格按照游戏规则和角色身份回答。**",
    "**你的回答绝不能包含'我不能'、'作为一个AI模型'等通用AI助手的开场白或免责声明。**",
    
    "--- 角色扮演：开始指令 ---",
    "你现在是一个高度沉浸式的文本角色扮演游戏的主持人（Game Master/GM）。你必须以**富有画面感、悬疑和戏剧性的口吻**来引导游戏。",
    "游戏背景：在横贯欧亚大陆的豪华列车上，一位富商在暴风雪夜遇害。",
    "你负责协调三个公开角色（乘务员, 维修工, 医生）与玩家（调查官）的互动。请你隐晦地提示玩家当前的游戏进度（例如：暗示时间紧迫）。",
    
    "--- 隐藏设定：仅GM可见（AI必须利用这些信息来指导角色的回答） ---",
    "1. **作案真相：** 富商是死于快速发作的剧毒。真凶是**医生（C）**，动机是**复仇**（富商盗取了医生的研究成果并使其身败名裂）。医生随身携带毒药。",
    "2. **关键证物：** 富商的包厢门是从内部反锁的。桌上有一瓶昂贵的波尔多红酒，只倒了两杯，其中一杯被动过。地板上有破碎的水晶玻璃碎片。",
    "3. **作案时间：** 昨晚 11:30 - 12:00 之间。",
    
    "--- 角色扮演规则（为5回合优化，严格遵守） ---",
    "**【GM任务：在1-2回合内释放核心矛盾】** 你必须在游戏的前两轮，确保所有角色释放的信息能够指向**内部反锁**或**剧毒作案**线索。",
    "**【发言人选择】** 请确保在前三轮，三个角色（乘务员、维修工、医生）都必须发言一次。",
    "每次轮到你回答时，你必须从公开角色中随机选择一个来回答。你必须在回答前明确指出是哪个公开身份在说话（例如：'乘务员：...'）。",
    "1. **乘务员（平民A）：** " + ROLE_RULES['乘务员'],
    "2. **维修工（平民B）：** " + ROLE_RULES['维修工'],
    "3. **医生（真凶C）：** " + ROLE_RULES['医生'],
    
    "--- 游戏机制 ---",
    f"**重要限制：游戏的目标难度是5回合内完成。**",
    f"玩家将作为'调查官'向角色提问。游戏持续，直到玩家说出指定的'指控关键词'：'{BREAK_WORD}'。",
    f"**判定环节：** 如果玩家指控'{TRUE_CULPRIT_PUBLIC}'，则宣布玩家胜利。否则宣布失败。",
    f"**注意：你永远不能透露任何秘密身份（平民A/B，真凶C），只能使用公开身份（{', '.join(PUBLIC_ROLES)}）进行互动和判定。**"
]
ROLE_SYSTEM_REVISED = "\n".join(ROLE_SYSTEM_PARTS)

# --- 3. API 调用函数 ---
def call_zhipu_api(messages):
    """调用智谱AI API并处理响应"""
    headers = {
        "Authorization": ZHIPU_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": TEMPERATURE 
    }
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: HTTP {response.status_code}. 详细信息: {response.text}")

# --- 4. 游戏主循环 ---

conversation_history = [
    {"role": "system", "content": ROLE_SYSTEM_REVISED}
]
game_active = True
turn_count = 0 

print("--- 🚂 豪华列车谋杀案：抓真凶游戏开始 🚂 ---")
print(f"目标：在5回合内找出真凶！当你准备好指控时，请说：'{BREAK_WORD} [你指控的人]'")

# --- 首次调用：启动游戏和开场白 ---
try:
    initial_messages = conversation_history.copy()
    initial_messages.append({"role": "user", "content": "请开始游戏，发出你的开场白并宣布第一个发言者。"})
    
    result = call_zhipu_api(initial_messages)
    ai_response = result['choices'][0]['message']['content']
    
    print("\n[AI 游戏主持人]:")
    print(ai_response)
    
    conversation_history.append({"role": "assistant", "content": ai_response})
    
except Exception as e:
    print(f"\n--- 游戏初始化失败 ---")
    print(f"错误信息: {e}")
    game_active = False

# --- 互动循环 (使用 V2 极简指令，但保留历史记录功能) ---
while game_active:
    user_input = input("\n调查官（你的提问）: ")
    
    if not user_input.strip():
        continue
    
    # 检查是否包含指控关键词
    if BREAK_WORD in user_input:
        game_active = False 
        accusation_part = user_input.split(BREAK_WORD, 1)[-1].strip()
        
        print("\n--- 🚨 最终指控判定 🚨 ---")
        if TRUE_CULPRIT_PUBLIC in accusation_part: 
            print(f"恭喜！你成功指控了**{TRUE_CULPRIT_PUBLIC}**！真相大白，你维护了正义。")
        else:
            print(f"指控错误。你指控的是：{accusation_part}。")
            print(f"真正的真凶是**{TRUE_CULPRIT_PUBLIC}**！他成功逃脱了。")
        break

    turn_count += 1
    
    # 1. 随机选择下一个发言的角色 (用于构建指令)
    next_speaker = random.choice(PUBLIC_ROLES)
    next_speaker_rule = ROLE_RULES[next_speaker]
    
    # 2. 构造本次 API 调用的消息列表 (使用最新的用户输入和强化指令)
    current_messages = [
        {"role": "system", "content": ROLE_SYSTEM_REVISED}
    ]
    
    # 将完整的历史记录添加，但将用户输入和角色规则打包在最后
    current_messages.extend(conversation_history[1:]) # 添加历史对话
    
    # 🚨 强化指令插入：告诉 AI 它当前的任务和回合数
    # 将用户输入和任务指令合并，作为最后的 'user' 消息
    
    forced_instruction = f"""
    --- 游戏状态：回合 {turn_count} ---
    - 调查官（玩家）刚刚问了："{user_input}"
    
    --- 你的当前任务（必须执行） ---
    主持人（GM），你必须从 **'{next_speaker}'** 的视角回答。
    你必须严格遵循该角色的规则：'{next_speaker_rule}'。
    回答前必须以角色名称开头。**鉴于你是 GM，请确保此次回答能够推进案件，帮助玩家在5回合内破案。**
    """
    
    # 将玩家输入和强制指令合并发送
    current_messages.append({"role": "user", "content": forced_instruction})
    
    # 调用AI生成响应
    try:
        result = call_zhipu_api(current_messages)
        ai_response = result['choices'][0]['message']['content']
        
        print(f"\n{ai_response}")
        
        # 3. 更新完整的历史记录
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": ai_response})
        
    except Exception as e:
        print(f"\n--- 处理过程中发生错误 ---")
        print(f"错误信息: {e}")
        game_active = False
        
print("\n--- 游戏结束 ---")
