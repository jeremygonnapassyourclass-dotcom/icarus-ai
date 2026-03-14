import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Icarus AI", page_icon="🕊️")


system_prompt = "You are Icarus, a compassionate emotional support AI. Keep responses thoughtful but somewhat brief."

temperature = 0.2
max_tokens = 80

st.title("🕊️ Icarus AI")
st.caption("Your private emotional support assistant")

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Talk to Icarus...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        bot_reply = completion.choices[0].message.content

        st.write(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

# Limit memory length
if len(st.session_state.messages) > 30:
    st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-29:]
