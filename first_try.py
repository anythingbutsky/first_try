import streamlit as st
import requests
import json

# 1. 页面设置
st.title("🤖 我的第一个 AI 聊天机器人")
st.write("现在我不是复读机了，我是真·AI！")

# 2. 从 Streamlit 的“秘密仓库”读取 API Key
# 这样做是为了安全，不直接把 Key 暴露在代码里
# 我们需要在同级目录下创建一个 .streamlit/secrets.toml 文件
try:
    # DeepSeek 的配置（如果你用智谱，这里要改 URL 和格式）
    API_KEY = st.secrets["DEEPSEEK_API_KEY"]
    API_URL = "https://api.deepseek.com/v1/chat/completions"
except Exception as e:
    st.error("找不到 API Key！请检查 .streamlit/secrets.toml 文件配置。")
    st.stop() # 如果没有 Key，程序停止运行

# 3. 创建（或获取）聊天记录
# Streamlit 有个特性：每次交互都会重新运行整个脚本。
# 用 st.session_state 来存储数据，才不会每次一输入，上面的记录就没了。
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "你是元宝，一个幽默风趣的助手。"}]

# 4. 显示历史聊天记录
for message in st.session_state.messages:
    if message["role"] != "system": # 系统提示词不显示给用户
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. 接收用户输入
prompt = st.chat_input("在这里跟我聊天吧...")

if prompt:
    # 5.1 显示用户的输入
    with st.chat_message("user"):
        st.markdown(prompt)
    # 5.2 把用户输入存进历史记录
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 5.3 调用 AI 接口
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat", # 使用的模型名称
        "messages": st.session_state.messages,
        "stream": False # 先不搞流式，一次返回全部
    }

    # 5.4 发送请求并显示 AI 回复
    with st.chat_message("assistant"):
        with st.spinner("AI 正在思考中..."):
            response = requests.post(API_URL, headers=headers, json=data)
            if response.status_code == 200:
                ai_response = response.json()["choices"][0]["message"]["content"]
                st.markdown(ai_response)
                # 5.5 把 AI 回复也存进历史
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                st.error(f"请求失败：{response.text}")