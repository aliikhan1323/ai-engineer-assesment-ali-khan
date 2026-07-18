<<<<<<< HEAD
"""
This script is used to create the Streamlit frontend for the AI Chatbot
"""
#Importing necessary libraries
=======
>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef
import streamlit as st
import httpx

st.set_page_config(page_title="AI Chatbot", page_icon="💬", layout="centered")

# Custom CSS for ChatGPT-like design
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .chat-sources {
        font-size: 0.8rem;
        color: #888888;
        margin-top: 5px;
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💬 AI Assistant Chatbot")
st.write("Ask anything! Queries are routed to a Superhero API or PDF Knowledge Base.")

# Backend API configuration
API_URL = st.sidebar.text_input("Backend API URL", "http://localhost:8000/ask")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            st.markdown(
                f"<div class='chat-sources'>Sources: {', '.join(message['sources'])}</div>",
                unsafe_allow_html=True,
            )

# React to user input
if prompt := st.chat_input("Ask a question..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Send question to backend API
            with httpx.Client(timeout=60.0) as client:
                response = client.post(API_URL, json={"question": prompt})
                response.raise_for_status()
                data = response.json()
                
                answer = data.get("answer", "No answer received.")
                sources = data.get("sources", [])
                
                message_placeholder.markdown(answer)
                if sources:
                    st.markdown(
                        f"<div class='chat-sources'>Sources: {', '.join(sources)}</div>",
                        unsafe_allow_html=True,
                    )
                
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )
        except Exception as e:
            error_msg = f"Error connecting to backend API: {e}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg, "sources": ["error"]}
            )
