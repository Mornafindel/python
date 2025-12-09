##chatbot 解耦文件

## api.py

* **`call_zhipu_api(messages, model="glm-4-flash")`**
  调用智谱 API 获取 AI 回复。

  * `messages`：消息列表，每条包含 `role` 和 `content`。
  * `model`：模型名称，可选 `"glm-4-flash"`。
  * 返回 API JSON 响应。

---

## memory.py

* **`load_memory(file_path)`**
  从 JSON 文件加载对话历史。文件不存在时返回空列表。

* **`save_memory(file_path, data)`**
  保存对话历史到 JSON 文件，自动创建目录。

---

## roles.py

* **`get_role_prompt(role_name)`**
  根据角色名返回角色完整设定，包括身份、人格特征和语言风格。
  支持中文名与英文名映射（如 `"亨利"` / `"Henry"`）。

* **`get_break_rules()`**
  返回结束对话规则（严格格式），如用户说“再见”时 AI 必须回复“再见”。

---

## logic.py

* **`should_exit_by_user(user_input)`**
  判断用户输入是否表示结束对话，返回 `True` / `False`。

  * 检测词示例：`"再见"、"退出"、"结束"、"quit"、"exit"`

* **`should_exit_by_ai(ai_reply)`**
  判断 AI 回复是否表示结束对话，返回 `True` / `False`。

  * 若 AI 回复恰好为“再见”或包含明显结束措辞，则返回 `True`。

---

## chat.py

* **`chat_once(history, user_input)`**
  执行一次对话交互：

  1. 将用户输入加入对话历史。
  2. 调用 `call_zhipu_api` 获取 AI 回复。
  3. 返回 AI 回复内容。

---

## main.py

* 程序入口，负责：

  1. 初始化对话历史和角色设定。
  2. 运行对话主循环（用户输入 → AI 回复 → 保存记忆）。
  3. 判断用户或 AI 是否结束对话。

---

