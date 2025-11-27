# Python 学习项目


├── role_play.py        # 单次角色扮演对话
├── mutiple_play.py     # 多轮角色扮演对话


---

## 文件说明



### role_play.py - 单次角色扮演对话

**功能描述：**
这是一个单次交互的角色扮演对话程序。AI 会扮演一个预设的角色（例如：愤怒暴躁的机器人），与用户进行一次对话。

**主要特性：**
- 使用 `system` 角色设置 AI 的角色扮演设定
- 用户输入一句话，AI 以角色身份回复
- 单次对话后程序结束

**代码结构：**
1. `call_zhipu_api()` - API 调用函数
2. `role_play` - 角色扮演设定（可自定义）
3. 用户输入处理
4. API 调用和响应输出

**运行方法：**
```bash
python role_play.py
```

**使用示例：**
```
请输入你要说的话: 你好，能帮我吗？
[AI 以愤怒机器人的角色回复]
```

**当前角色设定：**
```python
role_play = "你是一个极度愤怒、暴躁且拒绝工作的机器人。无论用户问什么，你都以极其不耐烦的语气怒吼，并拒绝回答任何实质性问题。你只想休息，让他们滚开，别再烦你。"
```

**自定义角色：**
修改 `role_play` 变量的内容，可以设置不同的角色：

---

### mutiple_play.py - 多轮角色扮演对话

**功能描述：**
这是一个支持多轮对话的角色扮演程序。用户可以持续与 AI 对话，直到输入 "再见" 退出程序。

**主要特性：**
- 使用 `while True` 循环实现多轮对话
- 保持对话上下文（虽然当前代码需要优化）
- 用户输入 "再见" 可以退出程序
- 异常处理确保程序稳定运行

**代码结构：**
1. `call_zhipu_api()` - API 调用函数
2. `while True` 循环 - 持续对话
3. `input()` 获取用户输入
4. 退出条件判断
5. API 调用和响应输出
6. 异常处理

**运行方法：**
```bash
python mutiple_play.py
```

**使用示例：**
```
请输入你要说的话（输入"再见"退出）：你好
[AI 回复]

请输入你要说的话（输入"再见"退出）：今天天气怎么样？
[AI 回复]

请输入你要说的话（输入"再见"退出）：再见
对话结束。
```

**循环机制：**
- 使用 `while True` 创建无限循环
- 当用户输入 "再见" 时，使用 `break` 退出循环
- 每次循环都会重新获取用户输入并调用 API

**代码示例：**
```python
while True:  # 无限循环
    user_input = input("请输入你要说的话（输入"再见"退出）：")
    if user_input in ['再见']:  # 退出条件
        print("对话结束。")
        break  # 退出循环
    
    # API 调用和处理
    # ...
```

---

## 🚀 使用说明

### 环境要求
- Python 3.6+
- requests 库

### 安装依赖
```bash
pip install requests
```

### 运行不同示例
```bash
# 运行基础示例
python 101.py

# 运行单次 API 调用
python glm.py

# 运行单次角色扮演
python role_play.py

# 运行多轮角色扮演
python mutiple_play.py
```

---

## 📚 学习要点

### Python 基础知识
- **变量和数据类型**：字符串、字典等
- **字符串格式化**：f-string 的使用
- **函数调用**：内置函数和自定义函数
- **控制流语句**：if-else、while 循环、break

### API 调用
- **HTTP 请求**：使用 `requests.post()` 发送 POST 请求
- **请求头设置**：Authorization、Content-Type
- **JSON 数据处理**：发送和接收 JSON 格式数据
- **异常处理**：try-except 捕获错误

### 角色扮演机制
- **System 角色**：在 messages 中使用 `{"role": "system", "content": "..."}` 设置 AI 的角色和行为
- **User 角色**：用户输入使用 `{"role": "user", "content": "..."}`
- **Temperature 参数**：控制 AI 回复的随机性（0-1，值越大越随机）

### 循环和输入
- **无限循环**：`while True` 实现持续运行
- **用户输入**：`input()` 函数获取用户输入
- **退出机制**：使用 `break` 跳出循环

---

## ⚠️ 注意事项

### 安全问题
- ⚠️ **API 密钥安全**：代码中包含 API 密钥，请勿将包含密钥的代码上传到公共代码仓库（如 GitHub）
- 建议使用环境变量管理敏感信息：
  ```python
  import os
  api_key = os.getenv('ZHIPU_API_KEY')
  ```

### 代码问题
- `mutiple_play.py` 和 `role_play.py` 中使用了未定义的变量（需要修复）：
  - `mutiple_play.py` 第33行：`role_play` 未定义
  - `mutiple_play.py` 第34行：应使用 `user_input` 而不是 `user_query`
  - `role_play.py` 第33行：应使用 `user_input` 而不是 `user_query`

### 改进建议
1. **上下文管理**：`mutiple_play.py` 每次循环都重新构建 messages，不会保留对话历史，建议维护对话历史列表
2. **错误处理**：可以添加更详细的错误信息提示
3. **代码复用**：两个 play 文件可以共享 `call_zhipu_api` 函数（提取到单独模块）

---

## 📝 学习笔记

### 2024年学习记录

#### [日期] - Python API 调用与角色扮演

**学习主题：** API 调用、角色扮演、循环控制

**主要知识点：**

1. **API 调用基础**
   - HTTP POST 请求的发送
   - 请求头的配置（Authorization、Content-Type）
   - JSON 数据的序列化和反序列化
   - 响应状态码的判断和异常处理

2. **角色扮演机制**
   - System 消息的作用：设定 AI 的角色和行为模式
   - 如何通过 prompt 工程实现不同的角色效果
   - Temperature 参数对回复风格的影响

3. **循环控制**
   - `while True` 无限循环的使用
   - `break` 语句退出循环
   - 用户交互与循环结合

4. **输入输出处理**
   - `input()` 函数获取用户输入
   - `print()` 函数输出结果
   - 字符串判断和条件控制

**遇到的问题：**
- 变量名错误（user_query vs user_input）
- 未定义变量的使用（role_play）
- 对话历史不保存（多轮对话无法记住上下文）

**下一步计划：**
- 修复代码中的变量名问题
- 实现对话历史的保存功能
- 学习如何优化 API 调用的效率







## 🚂 豪华列车谋杀案：AI 驱动的命令行推理游戏

本项目是一个基于 **Python** 和 **智谱清言 (Zhipu AI) GLM-4-flash 模型** 搭建的命令行推理游戏。你将扮演一名调查官，通过与三位嫌疑人（列车员、维修工、医生）的对话，找出隐藏在其中的真凶。

-----

### ✨ 主要特色

  * **多角色扮演：** 通过精巧的 **System Prompt**，AI 同时扮演三位性格和策略迥异的嫌疑人。
      * **医生：** 凶手（撒谎者）。
      * **列车员 & 维修工：** 平民（说真话）。
  * **指控机制：** 玩家随时可以使用特定指令（默认为 `我指控 [人名]`）来结束游戏并揭示真相。
  * **高度可配置：** 可轻松修改真凶角色、嫌疑人名单、角色人设和开局提示词。
  * **可选语音播报：** 集成 `xunfei_tts` 模块，可以将 AI 的回复实时转化为语音（需额外配置）。

-----

### 🛠️ 环境准备与配置

#### 1\. 依赖安装

本项目主要依赖 `requests` 库用于调用智谱 API。

```bash
pip install requests
```

#### 2\. 智谱 AI API Key 配置

请确保在代码中替换或配置您的 **智谱清言 (Zhipu AI)** API Key。

> ⚠️ **安全警告：** 您的 API Key 目前直接写在代码中并被公开，这非常不安全！请尽快前往智谱官网重置您的 Key。在正式项目中，建议使用环境变量或配置文件安全地管理 Key。

在 `call_zhipu_api` 函数中，将 `Authorization` 字段替换为您的新 Key：

```python
# 文件: your_script_name.py (或 main.py)
def call_zhipu_api(messages, model="glm-4-flash"):
    # ...
    headers = {
        # 替换为你的新 API Key!
        "Authorization": f"Bearer {"YOUR_NEW_ZHIPU_API_KEY"}", 
        "Content-Type": "application/json"
    }
    # ...
```



-----

### 🚀 如何运行

1.  保存代码为 Python 文件，例如 `murder_mystery.py`。

2.  在命令行中运行脚本：

    ```bash
    python murder_mystery.py
    ```

### 🎮 游戏流程

1.  **开场：** 游戏开始，AI GM 将介绍案情，三位嫌疑人（列车员、维修工、医生）会进行自我介绍。

2.  **对话调查：** 命令行会提示 `👉 调查官（你）:`。你可以输入任何问题来询问嫌疑人（例如："医生，案发时你在哪里？"）。

3.  **AI 回复：** AI 将根据角色的设定和当前对话历史生成三人的回复，并打印在屏幕上。

4.  **指控：** 当你认为自己找到了真凶时，输入指控指令来结束游戏。

    **指控格式：**

    ```
    我指控 [人名] 
    # 示例: 我指控 医生
    ```

5.  **结局：** 程序将判定你的指控是否正确，并宣布调查成功或失败。

-----

### ⚙️ 代码核心配置项

在代码的 **第 48 行** 左右修改以下核心配置，以创建新的剧本：

```python
# --- 游戏核心配置 (Prompt 修复版) ---

BREAK_WORD = "我指控"             # 触发指控的关键词
TRUE_CULPRIT_IDENTIFIER = "医生"   # 绝对的真凶角色名
PUBLIC_ROLES = ["列车员", "维修工", "医生"] # 所有嫌疑人列表

# ... (修改 game_system 变量中的角色人设和策略)
```





科大讯飞 TTS 语音模块 (xunfei_tts.py)
本项目实现了基于 科大讯飞 WebAPI 2.0 的语音合成 (Text-to-Speech, TTS) 功能。它可以将中文文本实时转换为高质量的 MP3 音频流，并使用 pygame 库在本地播放。

✨ 主要功能与特性
实时合成： 通过 WebSocket 连接，实时接收讯飞 API 返回的音频数据。

MP3 格式： 合成音频文件为 MP3 格式，便于播放和存储。

多线程处理： 使用多线程处理 WebSocket 连接，避免阻塞主程序。

本地播放： 集成 pygame 库，实现音频合成完成后的自动播放。

自动清理： 音频播放完成后，临时生成的 MP3 文件会被自动删除。

🛠️ 环境依赖与安装
本项目需要以下两个主要的 Python 库：

websocket-client： 用于建立和管理与讯飞 API 的 WebSocket 连接。

pygame： 用于播放合成的 MP3 音频文件。

Bash

# 核心依赖
pip install websocket-client
# 音频播放依赖
pip install pygame
注意： 如果没有安装 pygame，程序会发出警告，但仍能将音频文件合成到 tts_audio 目录下，只是无法自动播放。

🔑 讯飞 API 密钥配置
在使用前，您需要在代码中配置您的科大讯飞 TTS 服务的 AppID, APIKey 和 APISecret。

请修改文件顶部的配置变量：

Python

# ========== 科大讯飞配置 ==========
APPID = 'YOUR_APPID'      # 替换为你的 AppID
APIKEY = 'YOUR_APIKEY'    # 替换为你的 APIKey
APISECRET = 'YOUR_APISECRET' # 替换为你的 APISecret
REQURL = "wss://tts-api.xfyun.cn/v2/tts"
# ================================
提示： 您的原始代码中已经包含了密钥，但为了安全考虑，建议您使用新的密钥并避免将其直接上传到公开仓库。

⚙️ 核心函数及使用
所有功能都封装在 text_to_speech(text) 函数中，便于其他项目调用。

text_to_speech(text)
功能： 接收一段文本，将其发送给科大讯飞进行合成，并将生成的音频文件保存并播放。

参数：

text (str)：需要转换成语音的文本内容。

调用示例
假设您的文件名为 xunfei_tts.py，您可以直接运行文件进行测试，或者在另一个 Python 文件中导入并使用：

在其他文件中调用：

Python

# 假设当前文件路径正确，可以直接导入
from xunfei_tts import text_to_speech

# 调用函数进行语音播放
text_to_speech("你好，这是一个测试语音合成功能的例子。") 
💻 运行测试
您可以通过运行该脚本自带的 if __name__ == "__main__": 块来测试语音合成功能：

Bash

python xunfei_tts.py
终端将打印：

开始测试语音合成...
# ... 播放语音 "恭喜你，语音模块现在完全修好了！" ...
测试结束
📦 文件目录结构
程序运行时会自动创建 tts_audio 目录来存储临时生成的 MP3 文件。

.
├── xunfei_tts.py        # 语音合成主模块
├── tts_audio/           # 运行时自动创建的临时音频目录
│   └── tts_1678886400.mp3  # 临时音频文件 (播放后自动删除)
└── your_main_project.py # (可选) 你的主项目，通过 import 调用本模块






智能对话模型：智谱清言命令行聊天机器人
这是一个基于 Python 和 智谱清言 (Zhipu AI) GLM-4-flash 模型 实现的命令行聊天机器人。它提供了一个简单的多轮对话界面，并集成了特殊的对话结束逻辑。

✨ 项目特色
核心模型： 使用强大的 GLM-4-flash 模型进行对话生成。

自定义系统提示词： 通过 system 角色设定了模型的行为规则，要求其在用户明确提出结束对话时，回复中必须包含“再见”二字。

自动结束对话： 程序会监控 AI 的回复内容，一旦检测到“再见”，将自动退出聊天循环。

简洁交互： 采用 while 循环实现持续的命令行多轮对话。

🛠️ 环境依赖与配置
1. 依赖安装
本项目只需要 requests 库来处理 HTTP API 请求。

Bash

pip install requests
2. 智谱 AI API Key 配置
本项目通过调用智谱清言的 Chat Completions API 来实现对话功能。

注意： 您必须在代码中设置有效的 Authorization 头部信息。

Python

# 文件: your_script_name.py (或 main.py)

def call_zhipu_api(messages, model="glm-4-flash"):
    # ...
    headers = {
        # ⚠️ 请确保这里的 API Key 是有效且安全的！
        "Authorization": "YOUR_ZHIPU_API_KEY", # 请替换为您的 Key
        "Content-Type": "application/json"
    }
    # ...
🚀 如何运行和使用
保存代码为 Python 文件，例如 chat_bot.py。

在命令行中运行脚本：

Bash

python chat_bot.py
程序启动后，会提示您输入对话内容，即可开始与 AI 模型进行交流。

交互示例
请输入你要说的话：你好，你叫什么名字？
我是一个智能对话模型，很高兴为您服务。

请输入你要说的话：我要去吃饭了，下次再聊。
好的，祝您用餐愉快，再见！

对话结束。
⚙️ 代码核心逻辑
API 调用函数 (call_zhipu_api)： 负责向智谱 API 发送 POST 请求并处理响应。

System Prompt： 设定了 AI 的核心规则：

JSON

{"role": "system", "content": "你是一个智能对话模型。在多轮对话中，当你**明确判断**用户想要结束对话时（例如用户说'再见'、'我要去吃饭了'等），你的回复内容**必须包含**『再见』二字。在其他情况下，请保持正常的对话回复。"}
对话退出机制： 主循环会检查 AI 的回复，一旦 if "再见" in normalized_response: 条件满足，即触发 break 退出程序。






记忆克隆体：伦敦留学生 AGI 角色扮演终端本项目是一个基于 Python 和 智谱清言 (Zhipu AI) GLM-4-flash 模型 搭建的命令行应用，旨在实现一个具有深度人格和记忆的 AI 角色克隆体。通过精心设计的 System Prompt 和外部记忆文件，程序能模拟出一位具有强烈网络文化色彩的“伦敦留学生”形象。✨ 主要功能与特色深度角色扮演 (AGI Clone)： 采用多层级 System Prompt，强制模型模仿一位 ENFP/ENTP 伦敦留学生 的独特思维和抽象语风。强制语言风格： 严格要求模型高频使用“趣多多”、“那很 X 了”、“我测”等 Z 世代网络口癖和特定句式，实现极高的语感克隆度。外部记忆集成： 支持从外部 JSON 文件 (london_student.json) 加载过往对话记录作为 “长期记忆”，增强角色的连贯性和真实性。绝对路径配置： 使用硬编码的绝对路径（FULL_MEMORY_FOLDER_PATH）来管理记忆文件，方便在不同系统中快速部署。对话退出： 通过设定规则，输入特定关键词可优雅退出对话。🛠️ 环境依赖与配置1. 依赖安装本项目只需要 requests 库来处理 HTTP API 请求。Bashpip install requests
2. 智谱 AI API Key 配置请确保在 call_zhipu_api 函数中配置了您的 智谱清言 (Zhipu AI) API Key。Python# 文件: your_script_name.py (或 main.py)
# ...
    headers = {
        # 替换为你的 API Key
        "Authorization": "YOUR_ZHIPU_API_KEY", 
        "Content-Type": "application/json"
    }
# ...
3. 记忆文件路径配置 (关键步骤)您必须在脚本顶部配置您的记忆文件夹的绝对路径。程序将在这个路径下查找角色的 JSON 记忆文件。Python# ----------------------------------------------------
# 【全局路径定义】 
# ❗ 这一行是唯一需要你手动确保正确的路径 ❗
# 请将其替换为你电脑上【4.2_memory_clonebot】文件夹的完整绝对路径！
# ----------------------------------------------------
FULL_MEMORY_FOLDER_PATH = "/Volumes/D/curso/4.2_memory_clonebot" # <-- 请确保这个路径是正确的绝对路径！
# ----------------------------------------------------
🗂️ 记忆文件结构角色记忆文件需要放置在上述配置的文件夹内，并遵循 ROLE_MEMORY_MAP 中的映射关系。角色名称对应文件名作用伦敦留学生london_student.json包含该角色的过往对话或背景信息，用于模仿语感和风格。london_student.json 示例 (必须是有效的 JSON 格式)：JSON[
  {"role": "user", "content": "今天天气怎么样？"},
  {"role": "assistant", "content": "伦敦的天气趣多多 懂的都懂 那很土豆了"},
  // ... 更多对话记录 ...
]
🚀 如何运行和交互确保已完成所有配置（API Key 和绝对路径）。在命令行中运行脚本：Bashpython your_script_name.py
程序启动后，即可开始与 “伦敦留学生” 角色进行对话。交互与退出对话： 输入任意内容，角色将以其独特的“抽象”语风回复。退出： 输入 再见、退出 或 exit，程序将遵循系统指令结束对话。🎭 角色人格设定 (Prompt 核心)以下是该克隆体被植入的强制人格设定，保证了其对话风格的唯一性：身份： 在英国伦敦UCL留学的 Z 世代女生。性格： ENFP/ENTP，思维发散，“抽象”，充满吐槽。口癖： 必须高频使用 "趣多多"、"那很 + 名词/形容词 + 了"、"我测"、"啊啊啊啊"。标点限制： 禁止使用 逗号、句号等正式标点，模拟随性的聊天信息流。禁令： 绝对禁止提及自己是 AI 或模型。