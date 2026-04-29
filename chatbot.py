from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# --- CSS PULITO ---
st.markdown("""
<style>

/* Background neutro */
.stApp {
    background-color: #f7f7f8;
}

/* Header */
.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 600;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    margin-top: 0;
    margin-bottom: 2rem;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 85%;
}

/* User */
[data-testid="stChatMessage"][data-testid*="user"] {
    background-color: #2563eb;
    color: white;
    margin-left: auto;
}

/* Assistant */
[data-testid="stChatMessage"][data-testid*="assistant"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
}

/* Input */
textarea {
    border-radius: 10px !important;
    border: 1px solid #d1d5db !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Model**")
    st.caption("llama-3.1-8b-instant")

# --- HEADER ---
st.markdown("<p class='main-title'>💬 AI Chatbot</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask anything</p>", unsafe_allow_html=True)

# --- CHAT HISTORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LLM ---
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)

# --- INPUT ---
user_prompt = st.chat_input("Scrivi un messaggio...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(
                [{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history]
            )
            assistant_response = response.content
            st.markdown(assistant_response)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )