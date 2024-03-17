from transformers import GPT2LMHeadModel, GPT2Tokenizer
import streamlit as st
import re
def app():
    model = GPT2LMHeadModel.from_pretrained("summerB2014567/finetunninggpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("summerB2014567/finetunninggpt2")

    def response(question):
        ids = tokenizer.encode(f'{question}', return_tensors='pt')
        final_outputs = model.generate(
            ids,
            do_sample=True,
            max_length=150,
            pad_token_id=model.config.eos_token_id,
            top_k=50,
            top_p=0.95,
        )
        full_text = tokenizer.decode(final_outputs[0], skip_special_tokens=True)
        id_start = full_text.find("[A]")
        if id_start == -1 or id_start + 3 >= len(full_text):
            return "I'm sorry but i can't give you the answer to this question because i am not learning about this info yet :<"
        id_end = full_text.find("[Q]", id_start)
        if id_end == -1:
            id_end = len(full_text)
        return full_text[id_start+3:id_end]

    st.title("SUMMERGPT")


    if "messagers" not in st.session_state:
        st.session_state.messagers = []

    for message in st.session_state.messagers:
        with st.chat_message(message['role']):
            st.markdown(message['content'])


    if question := st.chat_input("What do you want ask?"):
        with st.chat_message("user"):
            st.markdown(question) 
        st.session_state.messagers.append({
            'role':'user',
            'content':question
        })

        generative_qes = "[Q] "+question
        answer = response(generative_qes)
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messagers.append({
            'role':'assistant',
            'content':answer
        })
