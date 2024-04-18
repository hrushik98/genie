from openai import OpenAI
import streamlit as st

st.title("Genie")

client = OpenAI(api_key=st.secrets['api_key'])

option = st.sidebar.selectbox("Choose the model", ["chat", "user persona"])

if option == "chat":
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
        prompt2 = prompt + "You have to answer in this way: "+ str(st.session_state["user_persona"])
        st.session_state.messages.append({"role": "user", "content": prompt2})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
    

if option == "user persona":
    user_persona = st.text_area("Enter the user persona")
    if st.button("Set user persona") and user_persona:
        st.session_state["user_persona"] = user_persona
        st.success("User persona set successfully")
    if "user_persona" in st.session_state:
        st.write(st.session_state["user_persona"])
    
