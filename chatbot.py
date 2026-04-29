from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="centered",
)

# --- CSS MINIMAL VIOLA ---
st.markdown("""
<style>

/* Background viola uniforme */
.stApp {
    background-color: #6d28d9;
    color: #111111;
}

/* Titolo */
.main-title {
    text-align: center;
    font-size: 2.3rem;
    font-weight: 700;
    color: #111111;
    margin-bottom: 0;
}

/* Sottotitolo */
.subtitle {
    text-align: center;
    color: #111111;
    opacity: 0.8;
    margin-bottom: 2rem;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.85);
    color: #111111;
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 10px;
    border: none;
}

/* Input box */
textarea {
    background-color: rgba(255, 255, 255, 0.9) !important;
    color: #111111 !important;
    border: none !important;
    border-radius: 12px !important;
}

/* Focus input */
textarea:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px #4c1d95 !important;
}

/* Hide sidebar completely */
[data-testid="stSidebar"] {
    display: none;
}

/* Remove top padding clutter */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<p class='main-title'>💬 AI Chatbot</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Simple purple clean UI</p>", unsafe_allow_html=True)

# --- STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SHOW CHAT ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- MODEL ---
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
        with st.spinner("..."):
            response = llm.invoke(
                [{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history]
            )
            assistant_response = response.content
            st.markdown(assistant_response)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )