from datetime import datetime
from memory import load_memory, save_memory
from roles import get_role_prompt, get_break_rules
from logic import should_exit_by_user, should_exit_by_ai
from chat import chat_once

# 全局配置
MEMORY_FILE = "3.1_memory_101/conversation_memory.json"
ROLE = "Henry"  # 你可以改成 Hans

def main():
    history = load_memory(MEMORY_FILE)

    if len(history) == 0:
        system_msg = get_role_prompt(ROLE) + "\n" + get_break_rules()
        history.append({"role": "system", "content": system_msg})

    print(f"🛡️ 正在与 {ROLE} 对话中…（输入 再见 即可结束）\n")

    while True:
        user_input = input("你：")
        if should_exit_by_user(user_input):
            print("（已结束）")
            break

        ai_reply = chat_once(history, user_input)
        print(f"{ROLE}：{ai_reply}")

        if should_exit_by_ai(ai_reply):
            print("（AI结束）")
            break

    save_memory(MEMORY_FILE, history)
    print("记忆已保存。")

if __name__ == "__main__":
    main()
