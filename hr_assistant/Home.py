import streamlit as st
from dotenv import load_dotenv
from helpers import add_policies, cache_load_policies, create_chatbot, tidy_title
import streamlit.components.v1 as components
import time

# ------------------------
# Page setup
# ------------------------
load_dotenv()
st.set_page_config(page_title="HR Assistant Demo", layout="wide")

# ------------------------
# Session state
# ------------------------
if "message_history" not in st.session_state:
    st.session_state.message_history = []

if "show_thinking_cog" not in st.session_state:
    st.session_state.show_thinking_cog = False

# ------------------------
# Sidebar controls
# ------------------------
st.sidebar.header("Airey Settings")
theme = st.sidebar.selectbox("Theme", ["Default", "Mint", "Slate", "AireLogic"])
pause_animation = st.sidebar.checkbox("Pause animations", value=False)

# ------------------------
# Theme definitions
# ------------------------
THEMES = {
    "Default": {"bg": "#f6f8fa", "text": "#111", "accent": "#16a34a", "background_cogs": False},
    "Mint": {"bg": "#ecfdf5", "text": "#064e3b", "accent": "#10b981", "background_cogs": False},
    "Slate": {"bg": "#0f172a", "text": "#e5e7eb", "accent": "#22c55e", "background_cogs": False},
    "AireLogic": {"bg": "#ecfdf5", "text": "#052e16", "accent": "#16a34a", "background_cogs": True},
}

t = THEMES[theme]

# ------------------------
# CSS
# ------------------------
def render_css():
    st.markdown(f"""
    <style>
    :root {{
        --airey-bg: {t['bg']};
        --airey-text: {t['text']};
        --airey-accent: {t['accent']};
    }}

    @keyframes bounce {{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-12px);}}}}
    @keyframes rotate {{from{{transform:rotate(0deg);}}to{{transform:rotate(360deg);}}}}

    .airey-box {{
        display:flex; gap:14px; padding:14px; border-radius:14px;
        background:var(--airey-bg); color:var(--airey-text); margin-bottom:16px; position:relative;
    }}
    .airey-box::after {{
        content:""; position:absolute; left:-10px; top:24px;
        border-width:10px; border-style:solid; border-color:transparent var(--airey-bg) transparent transparent;
    }}
    .airey-cog {{
        font-size:52px; color: #16a34a;
        {"animation: bounce 1.6s infinite;" if not pause_animation else ""}
    }}
    .airey-cog-thinking {{
        font-size:56px; color: #16a34a;
        {"animation: rotate 1.5s linear infinite;" if not pause_animation and st.session_state.show_thinking_cog else ""}
    }}
    .airey-fixed {{
        position:fixed; right:18px; bottom:18px; font-size:56px; color: #16a34a;
        {"animation: rotate 1.5s linear infinite;" if not pause_animation and st.session_state.show_thinking_cog else ""}
        opacity:0.9; z-index:1000;
    }}

    {"body::before {content:'⚙️ ⚙️ ⚙️ ⚙️ ⚙️'; position:fixed; inset:0; font-size:120px; opacity:0.04; animation: rotate 40s linear infinite; pointer-events:none;}" if t["background_cogs"] and not pause_animation else ""}
    </style>
    """, unsafe_allow_html=True)

render_css()

# ------------------------
# Airey UI
# ------------------------
def airey_welcome():
    st.markdown("""
        <div class="airey-box">
            <div class="airey-cog">⚙️</div>
            <div>
                <b>Hi, I’m Airey</b> 👋<br/>
                I help you understand HR policies.
            </div>
        </div>
    """, unsafe_allow_html=True)

# ------------------------
# Chatbot setup
# ------------------------
hr_policy_chatbot = create_chatbot("hr_policies")
policies, original_policies = cache_load_policies("./Policies")
add_policies(hr_policy_chatbot, policies)

# ------------------------
# Layout
# ------------------------
st.header("HR helper PoC")
policies_col, chat_col = st.columns([3,2])

with policies_col:
    st.subheader("Policies")
    for name, text in original_policies.items():
        with st.expander(f"{tidy_title(name)} Policy"):
            st.write(text)

with chat_col:
    st.subheader("Ask virtual HR assistant")

    if not st.session_state.message_history:
        airey_welcome()

    # Container for chat messages
    chat_container = st.container()

    # Ask input at bottom
    prompt = st.chat_input("Ask")

    # Display chat history: each user question stays above its answer
    for role, msg in st.session_state.message_history:
        with chat_container:
            st.chat_message(role).write(msg)

    if prompt:
        # Append user question first
        st.session_state.message_history.append(("user", prompt))
        with chat_container:
            st.chat_message("user").write(prompt)

        # ------------------------
        # Show rotating cog while thinking
        # ------------------------
        st.session_state.show_thinking_cog = True
        render_css()
        typing_placeholder = st.empty()
        typing_placeholder.markdown(
            '<div class="airey-fixed">⚙️</div>',  # spins in place at bottom-right
            unsafe_allow_html=True
        )
        components.html("<script>window.scrollTo(0, document.body.scrollHeight);</script>", height=0)

        try:
            # Rotate cog for 5 seconds
            time.sleep(5)

            # Get chatbot response
            response = hr_policy_chatbot.ask(prompt)
        except Exception as e:
            response = "⚠️ Sorry, something went wrong."
        finally:
            # Stop rotation immediately
            st.session_state.show_thinking_cog = False
            render_css()
            typing_placeholder.empty()

        # Display assistant message
        st.session_state.message_history.append(("assistant", response))
        with chat_container:
            st.chat_message("assistant").write(response)
        components.html("<script>window.scrollTo(0, document.body.scrollHeight);</script>", height=0)
