import streamlit as st
import mysql.connector
from mysql.connector import Error
import datetime


# Function to create a connection to the MySQL database
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Correct MySQL host for local machine
            user="root",  # Replace with your MySQL username
            password="H@nzalah12345",  # Replace with your MySQL password
            database="lost_and_found"
        )
        st.success("Connected to the database successfully!")
    except Error as e:
        st.error(f"Error: '{e}'")
    return connection


# Function to insert a new lost item
def insert_lost_item(connection, user_id, item_name, item_description, item_image, date_lost, location_lost,
                     contact_info):
    cursor = connection.cursor()
    query = """
    INSERT INTO lost_items (user_id, item_name, item_description, item_image, date_lost, location_lost, contact_info)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, item_name, item_description, item_image, date_lost, location_lost, contact_info))
    connection.commit()


# Function to insert a new found item
def insert_found_item(connection, user_id, item_name, item_description, item_image, date_found, location_found,
                      contact_info):
    cursor = connection.cursor()
    query = """
    INSERT INTO found_items (user_id, item_name, item_description, item_image, date_found, location_found, contact_info)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, item_name, item_description, item_image, date_found, location_found, contact_info))
    connection.commit()


# Function to claim a lost item
def claim_lost_item(connection, item_id, email):
    cursor = connection.cursor()
    # Verify email and get user_id
    cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    if not user:
        st.error("Invalid email. Please register first.")
        return

    claimed_by = user[0]

    # Get the item details
    cursor.execute("SELECT * FROM lost_items WHERE item_id = %s", (item_id,))
    item = cursor.fetchone()
    if item:
        query = """
        INSERT INTO claimed_items (user_id, item_name, item_description, item_image, date_lost, location_lost, contact_info, claimed_by, claim_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
        item[1], item[2], item[3], item[4], item[5], item[6], item[7], claimed_by, datetime.date.today()))
        connection.commit()
        # Delete the item from lost_items
        cursor.execute("DELETE FROM lost_items WHERE item_id = %s", (item_id,))
        connection.commit()
        st.success(f"Item ID {item_id} has been successfully claimed and removed from lost items.")


# Streamlit app layout
st.title("Lost and Found Application")

connection = create_connection()

if connection is not None:
    option = st.sidebar.selectbox("Choose an action",
                                  ["Report a Lost Item", "View Lost Items", "Report a Found Item", "View Found Items"])

    if option == "Report a Lost Item":
        st.header("Report a Lost Item")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        item_name = st.text_input("Item Name")
        item_description = st.text_area("Item Description")
        item_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        date_lost = st.date_input("Date Lost", datetime.date.today())
        location_lost = st.text_input("Location Lost")
        contact_info = st.text_input("Contact Information")

        if st.button("Submit"):
            if username and email and password and item_name and item_description and item_image and location_lost and contact_info:
                # Check if user exists or insert a new user
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                if user is None:
                    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                                   (username, email, password))
                    connection.commit()
                    user_id = cursor.lastrowid
                else:
                    user_id = user[0]

                # Insert lost item
                insert_lost_item(connection, user_id, item_name, item_description, item_image.read(), date_lost,
                                 location_lost, contact_info)
                st.success("Lost item reported successfully!")
            else:
                st.error("Please fill out all fields.")

    elif option == "View Lost Items":
        st.header("Lost Items")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT item_id, item_name, item_description, item_image, date_lost, location_lost, contact_info FROM lost_items")
        items = cursor.fetchall()
        for item in items:
            st.subheader(item[1])
            st.write(f"Description: {item[2]}")
            st.write(f"Date Lost: {item[4]}")
            st.write(f"Location Lost: {item[5]}")
            st.write(f"Contact Info: {item[6]}")
            st.image(item[3], width=300)
            email = st.text_input(f"Email to Claim Item ID {item[0]}", key=f"email_{item[0]}")
            if st.button(f"Claim Item ID {item[0]}", key=f"claim_{item[0]}"):
                claim_lost_item(connection, item[0], email)

    elif option == "Report a Found Item":
        st.header("Report a Found Item")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        item_name = st.text_input("Item Name")
        item_description = st.text_area("Item Description")
        item_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        date_found = st.date_input("Date Found", datetime.date.today())
        location_found = st.text_input("Location Found")
        contact_info = st.text_input("Contact Information")

        if st.button("Submit"):
            if username and email and password and item_name and item_description and item_image and location_found and contact_info:
                # Check if user exists or insert a new user
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                if user is None:
                    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                                   (username, email, password))
                    connection.commit()
                    user_id = cursor.lastrowid
                else:
                    user_id = user[0]

                # Insert found item
                insert_found_item(connection, user_id, item_name, item_description, item_image.read(), date_found,
                                  location_found, contact_info)
                st.success("Found item reported successfully!")
            else:
                st.error("Please fill out all fields.")

    elif option == "View Found Items":
        st.header("Found Items")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT item_id, item_name, item_description, item_image, date_found, location_found, contact_info FROM found_items")
        items = cursor.fetchall()
        for item in items:
            st.subheader(item[1])
            st.write(f"Description: {item[2]}")
            st.write(f"Date Found: {item[4]}")
            st.write(f"Location Found: {item[5]}")
            st.write(f"Contact Info: {item[6]}")
            st.image(item[3], width=300)

    connection.close()
else:
    st.error("Failed to connect to the database.")
