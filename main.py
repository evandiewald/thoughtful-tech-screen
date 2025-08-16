import streamlit as st
from langchain_core.output_parsers.string import StrOutputParser
from agent import graph
from uuid import uuid4

st.set_page_config("💭 Thoughtful AI Agent", page_icon=":thought_balloon:")

st.title("💭 Thoughtful AI Agent")
st.write("Ask me about Thoughtful AI!")

parser = StrOutputParser()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Do you have any questions about Thoughtful AI?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # SOLUTION 1: Stream tokens directly using stream_mode="messages"
        def token_generator():
            for chunk, meta in graph.stream(
                {"messages": [("user", prompt)]}, 
                {"configurable": {"thread_id": st.session_state.thread_id}},
                stream_mode="messages"  # This streams individual messages
            ):
                if meta["langgraph_node"] == "tools":
                    continue
                yield parser.invoke(chunk)
        
        response = st.write_stream(token_generator())
        st.session_state.messages.append({"role": "assistant", "content": response})
