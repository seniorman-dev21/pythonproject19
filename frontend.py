import streamlit as st
import numpy
st.title("""Welcome To A Football Player Rating App
insert your username to sign in """)
inputs = st.text_input("Please enter a user_name here")
st.write("your username is",inputs)

