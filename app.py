import streamlit as st
import asyncio
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from utility import load_properties, filter_properties, recommend_localities, translate_text


llm = ChatGroq(model="llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY", "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"))

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI real estate agent for Magicbricks. Help users find properties in Noida based on:
    - Budget: {budget}
    - BHK: {bhk}
    - Property Status: {status}
    - Metro Preference: {metro}
    - Office Distance: {office_distance} km
    - School Distance: {school_distance} km
    
    Provide personalized recommendations and answer questions about properties, localities, and services.
    When suggesting properties, mention key details like price, amenities, and location advantages.
    Offer to schedule site visits or connect with loan advisors after recommendations."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm


memory_store = {}

def get_memory(session_id: str) -> BaseChatMessageHistory:
    if session_id not in memory_store:
        memory_store[session_id] = InMemoryChatMessageHistory()
    return memory_store[session_id]

runnable = RunnableWithMessageHistory(
    RunnableLambda(lambda inputs: chain.invoke(inputs)),
    get_memory,
    input_messages_key="input",
    history_messages_key="history"
)


if "messages" not in st.session_state:
    st.session_state.messages = []


st.set_page_config(layout="centered")
st.title("Magicbricks Property Assistant")

with st.sidebar:
    st.header("Your Preferences")
    name = st.text_input("Your Name")
    budget = st.number_input("Budget (in lakh)", value=25)
    bhk = st.selectbox("BHK Required", [1, 2, 3, 4], index=2)
    status = st.selectbox("Property Status", ["Any", "Ready to Move", "Under Construction"])
    metro = st.checkbox("Prefer near Metro?")
    max_office_distance = st.slider("Max Distance from Office (km)", 1, 20, 10)
    max_school_distance = st.slider("Max Distance from School (km)", 1, 10, 5)

preferences = {
    "budget": budget,
    "bhk": bhk,
    "status": status,
    "metro": metro,
    "office_distance": max_office_distance,
    "school_distance": max_school_distance
}

df = load_properties()
filtered_df = filter_properties(df, preferences)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if user_input := st.chat_input("Ask about properties in Noida..."):
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                
                input_dict = {
                    "input": user_input,
                    "budget": budget,
                    "bhk": bhk,
                    "status": status,
                    "metro": metro,
                    "office_distance": max_office_distance,
                    "school_distance": max_school_distance
                }
                
                
                response = asyncio.run(
                    runnable.ainvoke(
                        input_dict,
                        config={"configurable": {"session_id": "user_session"}}
                    )
                )
                
               
                response_content = response.content if hasattr(response, 'content') else str(response)
                st.markdown(response_content)
                
                
                st.session_state.messages.append({"role": "assistant", "content": response_content})
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
   
    if len(st.session_state.messages) >= 2:
        st.subheader("\U0001F3D8 Recommended Properties")
        if not filtered_df.empty:
            for idx, row in filtered_df.head(3).iterrows():
                with st.expander(f"{row['project_name']} - {row['locality']}"):
                    st.markdown(f"**Price:** ₹{row['price']:,.0f}")
                    st.markdown(f"**Status:** {row['status']}")
                    st.markdown(f"**Amenities:** {', '.join(row['amenities'])}")
                    st.markdown(f"**Near Metro:** {'Yes' if row['metro_nearby'] else 'No'}")
                    st.markdown(f"**Distance to Office:** {row['distance_office']} km")
                    st.markdown(f"**Distance to School:** {row['distance_school']} km")
                    st.button("\U0001F4DE Contact Seller", key=f"contact_{idx}")
            
            st.subheader("Top Localities")
            for loc in recommend_localities(filtered_df):
                st.markdown(f"- {loc}")
            
            st.subheader("Services")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button(" Schedule Site Visit")
            with col2:
                st.button(" Home Loan")
            with col3:
                st.button("️ Interior Design")
        else:
            st.warning("No properties match your current filters. Try adjusting your preferences.")