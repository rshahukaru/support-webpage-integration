import streamlit as st
from openai import OpenAI
import chromadb
import numpy as np

# UI Configuration
st.set_page_config(
    page_title="Travel Buddy",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
    <style>
        .stApp {
            background-color: #f5f5f5;
        }
        .chat-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .user-message {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 15px;
            margin: 5px;
        }
        .assistant-message {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 15px;
            margin: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Travel knowledge base
TRAVEL_DOCS = {
    "destinations.txt": """Popular destinations guide, visa requirements, best times to visit""",
    "local_customs.txt": """Cultural norms, etiquette, dress codes, tipping practices""",
    "safety.txt": """Travel safety tips, emergency contacts, common scams to avoid""",
    "transportation.txt": """Public transport guides, taxi services, car rentals""",
    "accommodation.txt": """Hotel bookings, hostels, vacation rentals, camping""",
    "food_drink.txt": """Local cuisine, restaurant recommendations, food safety"""
}

def get_chat_response(query, context):
    system_message = """You are an expert travel advisor helping users plan their trips and solve travel-related problems. 
    Use the provided context and your knowledge to give helpful, practical advice.
    After each response, ask if the user needs more specific information about any aspect you mentioned.
    Only stop asking when they explicitly say they don't need more information."""
    
    messages = [
        {"role": "system", "content": f"{system_message}\nContext: {context}"},
        {"role": "user", "content": query}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.75
    )
    return response.choices[0].message.content

# Chat interface
st.title("🌍 Travel Buddy")
st.subheader("Your AI Travel Assistant")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        st.markdown(
            f"<div class='{message['role']}-message'>{message['content']}</div>", 
            unsafe_allow_html=True
        )

# Chat input
query = st.chat_input("Ask me anything about your travel plans...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    response = get_chat_response(query, TRAVEL_DOCS)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()