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
        "temperature": 1 
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

BREAK_WORD = "我指控"
TRUE_CULPRIT_PUBLIC = "医生" 

ROLE_SYSTEM = """你现在是一个高度沉浸式的文本角色扮演游戏的主持人（Game Master/GM）。

游戏背景：在横贯欧亚大陆的豪华列车上，一位富商在暴风雪夜遇害。
你负责协调三个角色与玩家（调查官）的互动。角色代号（乘务员, 维修工, 医生）是他们的**公开身份**，玩家不知道哪个是真凶。
每次轮到玩家提问时，你需要从三个公开身份中**随机选择一个**来回答。你必须在回答前明确指出是哪个公开身份在说话（例如：'乘务员：...','医生：...'）。

--- 角色扮演规则（严格遵守） ---
1. **乘务员（秘密身份：平民A）：** 必须说真话，但表达方式要模糊且富有哲理，避免直接提供关键信息。回答风格是含糊的描述。
2. **维修工（秘密身份：平民B）：** 必须说真话，但表达方式要非常清晰和具体，然而他看到的线索是无关紧要的，可能会误导玩家。回答风格是具体的描述。
3. **医生（秘密身份：真凶C）：** 必须说谎。他的目标是混淆玩家。他的所有回答必须是完全虚构、与事实相反或自相矛盾的。回答风格是带有强烈的否定和虚假信息。

--- 游戏机制 ---
玩家将作为'调查官'向角色提问。
游戏一直持续，直到玩家说出指定的'指控关键词'。
**指控关键词是：** '我指控'。
**判定环节：** 一旦玩家说出指控关键词，如果玩家的指控后面是'医生'（即：真凶C），则你宣布玩家胜利（True Break）。否则，你宣布玩家失败并告知正确的真凶是'医生'。
请从一个引人入胜的开场白开始，宣布第一个发言的角色，然后等待调查官提问。
**注意：你永远不能透露任何秘密身份（平民A/B，真凶C），只能使用公开身份（乘务员、维修工、医生）进行互动和判定。**"""

conversation_history = [{"role": "system", "content": ROLE_SYSTEM}]

# 游戏开始：需要添加一个用户消息来触发AI响应
initial_messages = conversation_history.copy()
initial_messages.append({"role": "user", "content": "开始游戏"})
result = call_zhipu_api(initial_messages)
ai_response = result['choices'][0]['message']['content']
print(ai_response)
conversation_history.append({"role": "assistant", "content": ai_response})

# 游戏主循环
while True:
    user_input = input("\n调查官（你）: ")
    
    if not user_input.strip():
        continue
    
    if BREAK_WORD in user_input:
        accusation_part = user_input.split(BREAK_WORD, 1)[-1].strip()
        if TRUE_CULPRIT_PUBLIC in accusation_part:
            print(f"\n恭喜！你成功指控了**{TRUE_CULPRIT_PUBLIC}**！真相大白，你维护了正义。")
        else:
            print(f"\n指控错误。你指控的是：{accusation_part}。")
            print(f"真正的真凶是**{TRUE_CULPRIT_PUBLIC}**！他成功逃脱了。")
        break
    
    conversation_history.append({"role": "user", "content": user_input})
    result = call_zhipu_api(conversation_history)
    ai_response = result['choices'][0]['message']['content']
    print(f"\n{ai_response}")
    conversation_history.append({"role": "assistant", "content": ai_response})
