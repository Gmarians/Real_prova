from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# --- DARK THEME CSS SERIO ---
st.markdown("""
<style>

/* Background principale */
.stApp {
    background-color: #0f1117;
    color: #e5e7eb;
}

/* Titolo */
.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 2rem;
}

/* Chat container base */
[data-testid="stChatMessage"] {
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
}

/* USER message */
[data-testid="stChatMessage"]:has(div[data-testid="stMarkdownContainer"]) {
    background-color: #1f2937;
}

/* Assistant message */
[data-testid="stChatMessage"] {
    background-color: #111827;
    border: 1px solid #1f2937;
}

/* Input box */
textarea {
    background-color: #111827 !important;
    color: #e5e7eb !important;
    border: 1px solid #374151 !important;
    border-radius: 10px !important;
}

/* Input focus */
textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: none !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0b0d12;
    border-right: 1px solid #1f2937;
}

/* Button */
.stButton button {
    background-color: #1f2937;
    color: white;
    border: 1px solid #374151;
    border-radius: 8px;
}

.stButton button:hover {
    background-color: #374151;
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
st.markdown("<p class='subtitle'>Dark, minimal, professional UI</p>", unsafe_allow_html=True)

# --- HISTORY ---
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