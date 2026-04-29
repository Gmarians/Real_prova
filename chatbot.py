import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Carica variabili d'ambiente
load_dotenv()

# Configurazione Pagina
st.set_page_config(
    page_title="Lumina AI",
    page_icon="✨",
    layout="centered",
)

# --- CSS AVANZATO (Design Moderno) ---
st.markdown("""
<style>
    /* Importazione Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%);
    }

    /* Header */
    .header-container {
        text-align: center;
        padding: 2rem 0;
    }
    
    .main-title {
        background: linear-gradient(90deg, #c084fc, #e879f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    /* Container messaggi */
    [data-testid="stChatMessage"] {
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Stile specifico Assistant */
    [data-testid="stChatMessageAssistant"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
    }

    /* Stile specifico User */
    [data-testid="stChatMessageUser"] {
        background-color: rgba(147, 51, 234, 0.2) !important;
        border: 1px solid rgba(147, 51, 234, 0.3);
    }

    /* Input Bar */
    [data-testid="stChatInput"] {
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Nascondi Sidebar e menu inutili */
    [data-testid="stSidebar"], #MainMenu, footer {
        display: none;
    }

    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Lumina AI</h1>
        <p style="color: #d8b4fe; font-size: 1.1rem; opacity: 0.9;">
            L'assistente intelligente dal design minimale.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- INIZIALIZZAZIONE STATO ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- VISUALIZZAZIONE STORICO ---
# Creiamo un container per non far saltare la pagina durante il caricamento
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- LOGICA MODELLO ---
def get_ai_response(history):
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.6, # Un po' più di creatività
            api_key=os.getenv("GROQ_API_KEY")
        )
        # Formattazione per LangChain Groq
        system_msg = ("role", "system", "Sei Lumina, un assistente AI cordiale ed elegante. Rispondi in modo conciso ma utile.")
        messages = [system_msg] + [(m["role"], m["content"]) for m in history]
        
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Ops! Qualcosa è andato storto: {str(e)}"

# --- INPUT UTENTE ---
if prompt := st.chat_input("Chiedimi qualsiasi cosa..."):
    # Aggiungi messaggio utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Genera risposta assistente
    with st.chat_message("assistant"):
        with st.spinner("Lumina sta pensando..."):
            full_response = get_ai_response(st.session_state.messages)
            st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})