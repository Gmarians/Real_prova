from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(
    page_title="Colorful AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #1f4037, #99f2c8);
}

/* Header */
h1 {
    color: white;
    text-align: center;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px;
}

/* User message */
[data-testid="stChatMessage"][data-testid*="user"] {
    background-color: #4facfe;
    color: white;
}

/* Assistant message */
[data-testid="stChatMessage"][data-testid*="assistant"] {
    background-color: #43e97b;
    color: black;
}

/* Input box */
textarea {
    border-radius: 10px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2c3e50, #4ca1af);
    color: white;
}

</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("💡 **Powered by Groq**")

# --- HEADER ---
st.markdown(
    "<h1>💬 Colorful AI Chatbot</h1>",
    unsafe_allow_html=True
)

# --- CHAT HISTORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

avatars = {
    "user": "🧑",
    "assistant": "🤖"
}

for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar=avatars[message["role"]]):
        st.markdown(message["content"])

# --- LLM ---
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
)

# --- INPUT ---
user_prompt = st.chat_input("✨ Scrivi qualcosa...")

if user_prompt:
    st.chat_message("user", avatar="🧑").markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("✨ Thinking..."):
            response = llm.invoke(
                [{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history]
            )
            assistant_response = response.content
            st.markdown(assistant_response)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )