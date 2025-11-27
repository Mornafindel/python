# -*- coding: utf-8 -*-
import requests
import json
import random
import re  # 导入正则库，用于清洗文本
import time

# 试图导入你的语音模块
try:
    from xunfei_tts import text_to_speech
    TTS_AVAILABLE = True
except ImportError:
    print(" 警告：未找到 xunfei_tts.py 文件，语音功能将无法使用。")
    TTS_AVAILABLE = False

# --- 1. 辅助函数：清洗文本 ---
def clean_text_for_tts(text):
    """
    去除 Markdown 符号（如 **粗体**），防止 TTS 读出 '星号星号' 或合成失败
    """
    # 去掉 ** 和 ## 以及 - 
    text = text.replace("**", "").replace("##", "").replace("---", "")
    # 去掉多余的空行
    text = re.sub(r'\n+', '\n', text).strip()
    return text

# --- 2. API 调用函数 ---
def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        # ⚠️ 你的 API Key (请务必去官网刷新一下，因为你在网上泄露了)
        "Authorization": f"Bearer {"6d990e86b2e4434c9b120cd073ac8e45.X2Z3loSRC0UrZ1yH"}", 
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.9 # 稍微调高一点，让每个人物说话风格更迥异
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# --- 3. 游戏核心配置 (Prompt 修复版) ---

BREAK_WORD = "我指控" 
TRUE_CULPRIT_IDENTIFIER = "医生" 
PUBLIC_ROLES = ["列车员", "维修工", "医生"]

# 修复后的系统提示词：加入【保密协议】
game_system = f"""
--- 角色扮演：最高优先级指令 ---
你现在是“豪华列车谋杀案”的游戏运行系统（GM）。
你需要同时扮演三位嫌疑人：{', '.join(PUBLIC_ROLES)}。

**【绝对保密协议 - DO NOT REVEAL】**
1. **核心真相（仅你知道）：** 凶手是【{TRUE_CULPRIT_IDENTIFIER}】。
2. **行为禁令：** 你的输出内容**绝对不能**直接告诉玩家谁是凶手，也不能直接承认自己是凶手（除非被确凿证据指控）。你需要通过角色的对话让玩家去猜。
3. **格式要求：** 每次回复必须包含三个角色的发言，格式如下：
   列车员: [内容]
   维修工: [内容]
   医生: [内容]

**【角色人设库】**
1. **医生 (真凶)：** - 性格：傲慢、冷静、洁癖。
   - 策略：**必须撒谎**。他会用复杂的医学术语转移话题。如果被问到案发时间，他会编造不在场证明。
2. **列车员 (平民)：** - 性格：紧张、唯唯诺诺。
   - 策略：说真话，但很琐碎。他看见过维修工在案发前去过过道。
3. **维修工 (平民)：** - 性格：粗鲁、直接。
   - 策略：说真话，脾气暴躁。他当时只是去修厕所灯了。

**判定指令：** 当用户输入"{BREAK_WORD} [角色名]"时，游戏结束。

现在游戏开始。请以GM身份简短开场，介绍案情，然后让三个嫌疑人做简单的自我介绍。
"""

conversation_history = [
    {"role": "system", "content": game_system}
]

# --- 4. 游戏主程序 ---
print(f"--- 豪华列车抓真凶  ---")
print(f"嫌疑人：{', '.join(PUBLIC_ROLES)}") 
print(f"指控命令：'{BREAK_WORD} [人名]'\n")

# 首次开场
try:
    initial_messages = conversation_history.copy()
    initial_messages.append({"role": "user", "content": "游戏开始，请介绍案情并让嫌疑人自我介绍。"})
    
    print("🕵️  正在读取案卷...")
    result = call_zhipu_api(initial_messages)
    assistant_reply = result['choices'][0]['message']['content']
    
    print("\n" + "="*30)
    print(assistant_reply)
    print("="*30 + "\n")
    
    # --- 语音播放逻辑修复 ---
    if TTS_AVAILABLE:
        # 1. 清洗文本 (去掉 Markdown)
        clean_reply = clean_text_for_tts(assistant_reply)
        print("正在播放语音...")
        # 2. 调用语音
        text_to_speech(clean_reply)
    # -----------------------

    conversation_history.append({"role": "assistant", "content": assistant_reply})

except Exception as e:
    print(f" 错误: {e}")
    exit()

# 循环对话
while True:
    user_input = input("\n👉 调查官（你）: ")
    
    if not user_input.strip():
        continue
    
    # 指控逻辑
    if BREAK_WORD in user_input:
        accusation_part = user_input.split(BREAK_WORD, 1)[-1].strip()
        print("\n---  最终指控判定 ---")
        
        # 简单清洗一下玩家输入的标点
        accusation_part = accusation_part.replace("。", "").replace("！", "")
        
        if TRUE_CULPRIT_IDENTIFIER in accusation_part:
            win_msg = f"恭喜！你指控正确！**{TRUE_CULPRIT_IDENTIFIER}** 确实是真凶。正义得到了伸张！"
            print(win_msg)
            if TTS_AVAILABLE: text_to_speech(clean_text_for_tts(win_msg))
        else:
            lose_msg = f"指控错误！你抓错了人（{accusation_part}）。真凶是 {TRUE_CULPRIT_IDENTIFIER}，他已经趁乱逃跑了..."
            print(lose_msg)
            if TTS_AVAILABLE: text_to_speech(clean_text_for_tts(lose_msg))
        break
    
    # 正常对话
    conversation_history.append({"role": "user", "content": user_input})
    
    try:
        print(" 嫌疑人正在思考...")
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        
        print("\n" + "-"*30)
        print(assistant_reply)
        print("-" * 30)
        
        # --- 语音播放逻辑修复 ---
        if TTS_AVAILABLE:
            clean_reply = clean_text_for_tts(assistant_reply)
            print("正在播放语音...")
            text_to_speech(clean_reply)
        # -----------------------

        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
    except Exception as e:
        print(f"API调用错误: {e}")
        break