import streamlit as st
import pandas as pd

# Load datasets
groundwater = pd.read_csv("groundwater.csv")
rainfall = pd.read_csv("rainfall.csv")
quality = pd.read_csv("water_quality.csv")
usage = pd.read_csv("usage.csv")
population = pd.read_csv("population_stress.csv")

st.title("INGRES Chatbot Prototype")
st.write("Chat with the system about groundwater, rainfall, water quality, usage, or population stress.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to generate bot response
def get_response(query: str) -> str:
    q = query.lower()
    response = ""

    if "water level" in q:
        for _, row in groundwater.iterrows():
            if row['District'].lower() in q:
                response = f"Groundwater level in {row['District']} is {row['Water_Level_m']} m."
    elif "rainfall" in q:
        for _, row in rainfall.iterrows():
            if row['District'].lower() in q:
                response = f"Rainfall in {row['District']} is {row['Rainfall_mm']} mm."
    elif "tds" in q or "quality" in q or "ph" in q:
        for _, row in quality.iterrows():
            if row['District'].lower() in q:
                response = f"Water quality in {row['District']}: pH={row['pH']}, TDS={row['TDS_mg_L']} mg/L."
    elif "extraction" in q or "recharge" in q or "balance" in q:
        for _, row in usage.iterrows():
            if row['District'].lower() in q:
                balance = row['Recharge_MCM'] - row['Extraction_MCM']
                response = f"In {row['District']}, Extraction={row['Extraction_MCM']} MCM, Recharge={row['Recharge_MCM']} MCM, Balance={balance} MCM."
    elif "stress" in q or "population" in q:
        for _, row in population.iterrows():
            if row['District'].lower() in q:
                per_capita = row['Available_Water_MCM']*1e6 / row['Population']
                response = f"Water stress in {row['District']}: Population={row['Population']}, Per Capita Water={per_capita:.2f} L."
    if response == "":
        response = "Sorry, I couldn't find relevant data. Try asking about Jaipur, Ajmer, Kota, or Alwar."

    return response

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
if prompt := st.chat_input("Type your question..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and add bot response
    response = get_response(prompt)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
