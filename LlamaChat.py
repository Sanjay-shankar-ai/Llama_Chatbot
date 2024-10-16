import streamlit as st
import os
from langchain_groq import ChatGroq

# Initialize ChatGroq with the API key and model
llm = ChatGroq(
    temperature=0, 
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama-3.1-70b-versatile"
)

st. set_page_config(layout="wide")

# Streamlit App Title
st.title("Get Your Queries Resolved")
st.caption("Powered by Llama 3.1")

# Initialize session state to store past interactions
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Function to get response from LLM
def get_response(conversation_history):
    if conversation_history:
        # Join the conversation history into a single string
        full_conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        response = llm.invoke(full_conversation)
        return response.content  # Access the content attribute

# User input field
user_input = st.text_input("Ask a question about your subject:")

# If there is user input, call the LLM and store the interaction
if user_input:
    with st.spinner("Generating response..."):
        # Append user message to the conversation
        st.session_state['conversation'].append({"role": "user", "content": user_input})
        
        # Get AI response using the full conversation history
        response = get_response(st.session_state['conversation'])

        # Append AI response to the conversation
        st.session_state['conversation'].append({"role": "ai", "content": response})

# Display chat history with formatted chat bubbles
for message in st.session_state['conversation']:
    if message["role"] == "user":
        st.markdown(
            f"""
            <div style='background-color: #DCF8C6; color: black; padding: 10px; border-radius: 15px; margin-left: 80px; max-width: 100%;'>
            <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    elif message["role"] == "ai":
        st.markdown(
            f"""
            <div style='background-color: #E3F2FD; color: black; padding: 10px; border-radius: 15px; margin: 10px; max-width: 100%; margin-left: auto;'>
            <strong>AI:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)

# Add JavaScript for auto-scrolling
st.markdown(
    """
    <script>
    const chatContainer = document.querySelector('div[data-baseweb="container"]');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    </script>
    """,
    unsafe_allow_html=True
)
