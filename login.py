import streamlit as st
import re
import csv
import os

# File to store user credentials
USER_CSV = "users.csv"

# Function to validate email
def validate_email(email):
    return re.match(r"[^@]+@gmail\.com", email)

# Function to validate password
def validate_password(password):
    return re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password)

# Function to check if email exists in CSV
def email_exists(email):
    if os.path.exists(USER_CSV):
        with open(USER_CSV, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email:
                    return True
    return False

# Function to add a new user to CSV
def add_user_to_csv(email, password):
    with open(USER_CSV, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, password])

# Function to validate login credentials from CSV
def validate_login(email, password):
    if os.path.exists(USER_CSV):
        with open(USER_CSV, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email and row[1] == password:
                    return True
    return False

# Initialize session state variables
if 'signed_up' not in st.session_state:
    st.session_state.signed_up = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.title("User Authentication App")

# Sign-Up and Login logic
if not st.session_state.signed_up:
    # Sign-Up process
    st.subheader("Create a New Account")

    email = st.text_input("Email (Only Gmail)", placeholder="Enter your Gmail")
    password = st.text_input("Password", type="password", placeholder="Enter a strong password")

    if st.button("Sign Up"):
        if not validate_email(email):
            st.error("Invalid email. Please use a Gmail address.")
        elif not validate_password(password):
            st.error("Password must be at least 8 characters long, contain letters, numbers, and symbols.")
        elif email_exists(email):
            st.error("This email is already registered. Please use another one.")
        else:
            add_user_to_csv(email, password)
            st.success("You have successfully signed up!")
            st.session_state.signed_up = True  # Set state to indicate sign-up is complete
            st.info("Now, please login.")

if st.session_state.signed_up and not st.session_state.logged_in:
    # Login process
    st.subheader("Login to Your Account")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if validate_login(email, password):
            st.success("Logged in successfully!")
            st.session_state.logged_in = True  # Set state to indicate login is successful
        else:
            st.error("Invalid email or password")

if st.session_state.logged_in:
    st.subheader("Welcome!")
    st.write("You are now logged in.")
