import streamlit as st
import tensorflow as tf
import pickle
from tensorflow.keras.layers import TextVectorization
import numpy as np
model = tf.keras.models.load_model('toxicity.h5')
load_vectorizer = pickle.load(open("vectorzer_toxic.pkl","rb"))
vectorizer = TextVectorization.from_config(load_vectorizer['config'])
vectorizer.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
vectorizer.set_weights(load_vectorizer['weights'])

def app():
    st.title("Give me your point")
    with open('D:/LVTN/app\pages/comment.txt','r') as f:
        comments = f.readlines()
    if comment := st.chat_input(""):
        input_text = vectorizer(comment)
        res = model.predict(np.expand_dims(input_text,0))
        if res[0][0] > 0.7:
            st.error("Your comment contains toxic words, please try again with better word")
        else:
            st.success("you comment is valid")
            with open('D:/LVTN/app\pages/comment.txt', 'a') as f:
                f.write(comment+'\n')
    for i in comments:
        st.text(i)
    
