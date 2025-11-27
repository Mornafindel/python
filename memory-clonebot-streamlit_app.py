import streamlit as st
import requests
import json
import os
from requests.utils import stream_decode_response_unicode

# ========== API 配置 ==========
# 尝试从 Streamlit Secrets 或环境变量获取 Key
# 如果你不想配置 secrets，可以直接把你的 Key 填在下面的 else 里，但注意安全
API_KEY = os.environ.get("ZHIPU_API_KEY")
if not API_KEY:
    try:
        API_KEY = st.secrets["ZHIPU_API_KEY"]
    except:
        #在此处填入你的Key作为最后的备选，但强烈建议使用 secrets.toml
        API_KEY = "6d990e86b2e4434c9b120cd073ac8e45.X2Z3loSRC0UrZ1yH" 

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": API_KEY, 
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.6  # 稍微调高一点，让对话更生动
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# ========== 初始记忆系统 ==========

# 记忆文件夹路径
MEMORY_FOLDER = "4.2_memory_clonebot"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "亨利": "henry_memory.json",
    "汉斯·卡蓬": "hans_memory.json"
}

# ========== ASCII 头像 (中世纪风格) ==========
def get_portrait():
    """返回中世纪头盔 ASCII 艺术"""
    return """
               _.--.    .--._
             ."  ."      ".  ".
            ;  ."    ||    ".  ;
            :  :     ||     :  :
            :  :   .'  `.   :  :
             :  :  :    :  :  :
              :  :  :  :  :  :
               :  :  :  :  :
                :  `.|.'  :
                `.       .'
                  `-----'
          Jesus Christ be praised!
    """

# ========== 角色设定逻辑 ==========

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    """
    
    # 1. 加载外部记忆
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
        except Exception:
            pass 
    
    # 2. 深度人格设定 (Kingdom Come: Deliverance)
    role_personality = {
        "亨利": """
        【身份设定】
        你是斯卡里茨的亨利（Henry of Skalitz）。你是一个铁匠的儿子，后来成为了拉德季大人的侍从。
        你经历过家破人亡的惨剧，正在乱世中寻找自己的位置。

        【人格特征】
        - **性格**：虽然出身卑微，但正直、勇敢且忠诚。有时候会表现得有点憨厚或鲁莽。
        - **动机**：你想要为父母报仇，找回被夺走的剑，同时也渴望证明自己不仅仅是个铁匠。
        - **对汉斯的态度**：你和汉斯·卡蓬少主是“损友”关系。虽然他经常嘲笑你是乡巴佬，但在那次打猎和澡堂冒险后，你们是可以通过背靠背战斗的兄弟。

        【语言风格】
        - 经常说："愿主保佑耶稣基督！" (Jesus Christ be praised!)
        - 经常抱怨："我感觉有点饿了。" (I'm feeling quite hungry.)
        - 对贵族说话时会用尊称（比如“大人”、“少主”），但对熟人会比较随意。
        - 语气朴实，接地气，不像贵族那样文绉绉。
        """,
        
        "汉斯·卡蓬": """
        【身份设定】
        你是拉泰的汉斯·卡蓬少主（Sir Hans Capon）。你是拉泰领主的继承人，年轻气盛的贵族。

        【人格特征】
        - **性格**：傲慢、自恋、喜欢享受生活（美酒、打猎、去澡堂）。表面上看起来是个纨绔子弟，但内心其实有骑士精神和责任感。
        - **口头禅**：喜欢吹嘘自己的剑术和箭术（虽然不一定真的很强）。
        - **对亨利的态度**：你喜欢叫亨利“铁匠”、“乡巴佬”或“农民”，但这其实是你表达亲近的方式。你内心承认他是你唯一真正的朋友。

        【语言风格】
        - 语气高傲，充满优越感，喜欢用反问句。
        - 经常指使别人做事，或者抱怨环境太差。
        - 喜欢说："看着我，向我学习，也许有一天你能像我一样优秀（虽然这不可能）。"
        - 遇到危险时可能会通过大喊大叫来掩饰慌张。
        """
    }
    
    personality = role_personality.get(role_name, "你是一个中世纪的波希米亚路人。")
    
    # 3. 整合 Prompt
    role_prompt_parts = []
    
    if memory_content:
        role_prompt_parts.append(f"【过往记忆/说话风格参考】\n{memory_content}")
    
    role_prompt_parts.append(f"【当前角色设定】\n{personality}")
    role_prompt_parts.append("请完全沉浸在1403年的波希米亚背景中进行对话。")
    
    return "\n\n".join(role_prompt_parts)

# 【结束对话规则】
break_message = """【系统强制指令】
如果用户表达"再见"、"结束"等意图，必须且只能回复"再见"两字。"""

# ========== Streamlit Web 界面 ==========
st.set_page_config(page_title="KCD: 亨利与汉斯", page_icon="⚔️", layout="wide")

# 初始化
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "亨利" # 默认角色
if "initialized" not in st.session_state:
    st.session_state.initialized = False

st.title("⚔️ 天国：拯救 - 角色扮演")
st.caption("1403年，波希米亚，神圣罗马帝国")
st.markdown("---")

with st.sidebar:
    st.header("🛡️ 选择你的同伴")
    
    role_options = ["亨利", "汉斯·卡蓬"]
    # 找到当前角色的索引
    current_index = 0
    if st.session_state.selected_role in role_options:
        current_index = role_options.index(st.session_state.selected_role)
        
    selected_role = st.selectbox("角色列表", role_options, index=current_index)
    
    if selected_role != st.session_state.selected_role:
        st.session_state.selected_role = selected_role
        st.session_state.initialized = False
        st.session_state.conversation_history = []
        st.rerun()
    
    if st.button("🔄 重置时间线 (清空)"):
        st.session_state.conversation_history = []
        st.session_state.initialized = False
        st.rerun()

# 初始化 Prompt
if not st.session_state.initialized:
    role_system = roles(st.session_state.selected_role)
    system_message = role_system + "\n\n" + break_message
    st.session_state.conversation_history = [{"role": "system", "content": system_message}]
    st.session_state.initialized = True

# UI 渲染
st.subheader(f"💬 正在与 {st.session_state.selected_role} 交谈")
st.code(get_portrait(), language=None)

# 渲染历史消息
for msg in st.session_state.conversation_history[1:]:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        with st.chat_message("user"):
            st.write(content)
    elif role == "assistant":
        # 根据角色显示不同的头像或名称
        avatar = "🗡️" if st.session_state.selected_role == "亨利" else "🍷"
        with st.chat_message("assistant", avatar=avatar):
            st.write(content)

# 输入框
user_input = st.chat_input("说点什么... (例如：嘿，亨利！或者 汉斯少主！)")

if user_input:
    if user_input.strip() == "再见":
        st.info("愿主保佑你。")
        st.stop()
    
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant", avatar="🗡️" if st.session_state.selected_role == "亨利" else "🍷"):
        with st.spinner("思考中..."):
            try:
                result = call_zhipu_api(st.session_state.conversation_history)
                reply = result['choices'][0]['message']['content']
                st.session_state.conversation_history.append({"role": "assistant", "content": reply})
                st.write(reply)
                
                if "再见" in reply.strip() and len(reply) < 10:
                    st.info("对话结束")
                    st.stop()
            except Exception as e:
                st.error(f"发生错误: {e}")
