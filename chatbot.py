from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv()

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="centered",
)

# --- DARK THEME CSS ---
st.markdown("""
<style>

/* Background scuro */
.stApp {
    background-color: #0f0f0f;
    color: #e5e5e5;
}

/* Centrare tutto il contenuto */
.block-container {
    max-width: 700px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-top: 2rem !important;
}

/* Titolo */
.main-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0;
}

/* Sottotitolo */
.subtitle {
    text-align: center;
    color: #bbbbbb;
    margin-bottom: 2rem;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #1c1c1c;
    color: #e5e5e5;
    padding: 14px 18px;
    border-radius: 14px;
    margin-bottom: 10px;
    border: 1px solid #2a2a2a;
}

/* Input box */
textarea {
    background-color: #1c1c1c !important;
    color: #ffffff !important;
    border: 1px solid #333333 !important;
    border-radius: 12px !important;
}

/* Focus input */
textarea:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px #6d28d9 !important;
}

/* Hide sidebar */
[data-testid="stSidebar"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<p class='main-title'>💬 AI Chatbot</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Dark mode minimal UI</p>", unsafe_allow_html=True)

# --- STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SHOW CHAT HISTORY ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- MODEL ---
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)

# --- USER INPUT ---
user_prompt = st.chat_input("Scrivi un messaggio...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("assistant"):
        with st.spinner("Sto pensando..."):
            response = llm.invoke(
                [{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history]
            )
            assistant_response = response.content
            st.markdown(assistant_response)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )
