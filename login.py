import streamlit as st
from pymongo import MongoClient
import hashlib
import re


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["users"] 
data_collection = db["data"] 


# Streamlit app
st.title("Login and Signup App")


# Login Page
def login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")


    if st.button("Login"):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        data = data_collection.find_one({"username": username, "password": hashed_password})
        if data:
             st.success("Login successful!")
             st.markdown(f'<a href="http://localhost:8502" target="_blank">go to app</a>', unsafe_allow_html=True)
             
             
        else:
         st.error("Invalid credentials")
    
               


# Signup Page
def signup():
    st.header("Signup")
    new_username = st.text_input("New username")
    new_password = st.text_input("New Password", type="password")

    if not new_username.isalnum():
        st.warning("Username should only contain alphabets and numbers.")
        return


    if st.button("Signup"):
        # Validate password criteria
        if not (re.match("^[a-zA-Z0-9!@#$%^&*()-_+=]", new_password) and len(new_password) >= 5):
            st.warning("Password must contain at least 5 characters and include only letters, numbers, and symbols.")
            return

        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        if data_collection.find_one({"username": new_username}):
            st.warning("Username already exists. Please choose a different username.")
        else:
            data = {"username": new_username, "password": hashed_password}
            data_collection.insert_one(data)
            st.success("Signup successful! You can now login.")



# Navigation
page = st.radio("Select a page:", ("Login", "Signup"))

if page == "Login":
    login()
else:
    signup()