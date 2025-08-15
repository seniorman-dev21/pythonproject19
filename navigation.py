import streamlit as st
from pages import page_1, page_2

# Simple in-memory user "database"
users = {"user1": "password1", "user2": "password2"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login(username, password):
    if username in users and users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success(f"Logged in as {username}")
    else:
        st.error("Invalid username or password")

def signup(username, password):
    if username in users:
        st.error("Username already exists")
    else:
        users[username] = password
        st.success("User created, please log in")

if not st.session_state.logged_in:
    st.title("Login or Sign Up")

    option = st.radio("Choose option", ("Login", "Sign Up"))

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if option == "Login":
            login(username, password)
        else:
            signup(username, password)

else:
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    page = st.sidebar.selectbox("Navigate", ["Page 1", "Page 2"])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    if page == "Page 1":
        page_1.run()
    elif page == "Page 2":
        page_2.run()
