import streamlit as st
import requests
import os
from dotenv import load_dotenv
import plotly.io as pio

# Load environment variables
load_dotenv()

API_URL = "http://localhost:8000/query"

st.title("🚗 TOYOTA CHAT ASSISTANT 🚗")

# # Sidebar for Configuration
# st.sidebar.header("Configuration")
recursion_limit = st.sidebar.number_input("Recursion Limit", min_value=1, value=100)
thread_id = st.sidebar.text_input("Thread ID", value="1")

# Query Input Section
st.header("Enter Your Query")
query = st.text_area("Query", placeholder="Type your question here...")

# Submit Button
if st.button("Run Query"):
    with st.spinner("Processing your query..."):
        try:
            payload = {
                "query": query
            }
            
            # Send request to the API
            response = requests.post(API_URL, json=payload)
            
            # Handle response
            if response.status_code == 200:
                # Parse the JSON response
                result = response.json()
                
                # Display the response message
                st.success(result.get("message", "No response received"))
            
            else:
                # Handle error responses
                st.error(f"Error: {response.status_code} - {response.text}")
        
        except requests.RequestException as e:
            # Handle connection errors
            st.error(f"Connection error: {e}")
        except Exception as e:
            # Handle any unexpected errors
            st.error(f"An unexpected error occurred: {e}")

# Optional: Add some context or help
st.sidebar.markdown("### How to Use")
st.sidebar.info("""
- Ask about test drives
- Book service appointments
- Check vehicle availability
- Get Toyota-related information
""")