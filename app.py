import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime, timedelta
import altair as alt

# Files to store data
DATA_FILE = "data/submissions.csv"
MILEAGE_FILE = "data/mileage_log.csv"
VEHICLES_FILE = "data/vehicles.csv"
EMPLOYEES_FILE = "data/employees.csv"

def load_data(file_path):
    return pd.read_csv(file_path)

# Ensure CSV files exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "submission_id",
        "Employee", "Vehicle", "Date",
        "Tire_FL_PSI", "Tire_FR_PSI", "Tire_RL_PSI", "Tire_RR_PSI", "Tire_Comments",
        "Headlights_OK", "Taillights_OK", "Brake_Lights_OK", "Turn_Signals_OK", "Lights_Comments",
        "Exterior_Washed", "Interior_Cleaned", "Cleaning_Comments",
        "Mileage", "Mileage_Comments",
        "Wipers_OK", "Wipers_Comments",
        "Oil_Level_OK", "Coolant_Level_OK", "Brake_Fluid_OK", "Fluids_Comments",
        "Oil_Photo",
        "Brakes_OK", "Brakes_Comments",
        "Photos", "Notes"
    ]).to_csv(DATA_FILE, index=False)

if not os.path.exists(MILEAGE_FILE):
    pd.DataFrame(columns=[
        "submission_id",
        "Employee", "Vehicle", "Date", 
        "Mileage", "Mileage_Comments"
    ]).to_csv(MILEAGE_FILE, index=False)

if not os.path.exists(VEHICLES_FILE):
    pd.DataFrame({"Vehicle": ["Jeep", "Karma", "Big Red", "Muffin", "Loud Truck", "2018"]}).to_csv(VEHICLES_FILE, index=False)

if not os.path.exists(EMPLOYEES_FILE):
    pd.DataFrame({
        "Employee": ["Cody", "Mason", "Casey", "Kasey", "Colby", "Jack"],
        "Username": ["cody123", "mason123", "casey123", "kasey123", "colby123", "jack123"],
        "Password": ["pass123", "pass123", "pass123", "pass123", "pass123", "pass123"],
        "Assigned_Vehicle": ["Jeep", "Karma", "Big Red", "Muffin", "Loud Truck", "2018"]
    }).to_csv(EMPLOYEES_FILE, index=False)

# Initialize session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.employee_id = ""
    st.session_state.user_type = ""
    st.session_state.username = ""

st.title("Truck Checks App")

# --------------------------------
# LOGIN LOGIC
# --------------------------------
if not st.session_state.logged_in:
    st.subheader("Login")
    with st.form(key="login_form"):
        user_type = st.selectbox("User Type", ["", "Employee", "Admin"], index=0, help="Select whether you are an Employee or Admin")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.form_submit_button("Login"):
            if not user_type:
                st.error("Please select a User Type")
            elif user_type == "Admin" and username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.employee_id = "admin"
                st.session_state.user_type = "admin"
                st.session_state.username = username
                st.rerun()
            elif user_type == "Employee":
                employees_df = load_data(EMPLOYEES_FILE)
                user_match = employees_df[
                    (employees_df["Username"] == username) &
                    (employees_df["Password"] == password)
                ]
                if not user_match.empty:
                    st.session_state.logged_in = True
                    st.session_state.employee_id = user_match.iloc[0]["Employee"]
                    st.session_state.user_type = "employee"
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Wrong username or password")
            else:
                st.error("Wrong username or password")
else:
    # --------------------------------
    # LOGOUT BUTTON
    # --------------------------------
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.employee_id = ""
        st.session_state.user_type = ""
        st.session_state.username = ""
        st.rerun()

    # --------------------------------
    # EMPLOYEE VIEW
    # --------------------------------
    if st.session_state.user_type == "employee":
        employees_df = load_data(EMPLOYEES_FILE)
        emp_row = employees_df[employees_df["Employee"] == st.session_state.employee_id].iloc[0]
        assigned_vehicle = emp_row["Assigned_Vehicle"]
        
        st.subheader(f"Welcome, {st.session_state.employee_id}!")
        st.subheader(f"Vehicle: {assigned_vehicle}")
        st.markdown("**Instructions**: Check all items, upload photos if needed, and hit Submit—done!")
        
        check_date = st.date_input("Check Date", value=datetime.now())
        date_str = check_date.strftime("%Y-%m-%d")

        # Tires
        st.subheader("Tires")
        tire_fl_psi = st.number_input("Front Left Tire Pressure (PSI)", min_value=0, max_value=100, value=30)
        tire_fr_psi = st.number_input("Front Right Tire Pressure (PSI)", min_value=0, max_value=100, value=30)
        tire_rl_psi = st.number_input("Rear Left Tire Pressure (PSI)", min_value=0, max_value=100, value=30)
        tire_rr_psi = st.number_input("Rear Right Tire Pressure (PSI)", min_value=0, max_value=100, value=30)
        tire_comments = st.text_area("Tire Comments")

        # Lights
        st.subheader("Lights")
        headlights_ok = st.checkbox("Headlights OK")
        taillights_ok = st.checkbox("Taillights OK")
        brake_lights_ok = st.checkbox("Brake Lights OK")
        turn_signals_ok = st.checkbox("Turn Signals OK")
        lights_comments = st.text_area("Lights Comments")

        # Cleaning
        st.subheader("Cleaning")
        exterior_washed = st.checkbox("Exterior Washed")
        interior_cleaned = st.checkbox("Interior Cleaned")
        cleaning_comments = st.text_area("Cleaning Comments")

        # Mileage
        st.subheader("Mileage")
        mileage = st.number_input("Current Mileage", min_value=0, value=0)
        mileage_comments = st.text_area("Mileage Comments")

        # Wipers
        st.subheader("Wipers")
        wipers_ok = st.checkbox("Windshield Wipers OK")
        wipers_comments = st.text_area("Wipers Comments")

        # Fluids
        st.subheader("Fluids")
        oil_level_ok = st.checkbox("Oil Level OK")
        coolant_level_ok = st.checkbox("Coolant Level OK")
        brake_fluid_ok = st.checkbox("Brake Fluid OK")
        fluids_comments = st.text_area("Fluids Comments")
        oil_photo = st.file_uploader("Upload Oil Level Photo (Required)", type=["jpg", "png"])
        if not oil_photo:
            st.warning("Please upload an oil level photo before submitting.")

        # Brakes
        st.subheader("Brakes")
        brakes_ok = st.checkbox("Brakes OK")
        brakes_comments = st.text_area("Brakes Comments")

        # General Photos
        photos = st.file_uploader("Upload Additional Photos (Optional)", accept_multiple_files=True, type=["jpg", "png"])

        # Notes
        st.subheader("Notes")
        notes = st.text_area("Any issues or thoughts?")

        if st.button("Submit Check", type="primary"):
            if not oil_photo:
                st.error("Oil level photo is required!")
            else:
                # Save oil photo
                oil_photo_path = f"uploads/oil_photos/{oil_photo.name}"
                os.makedirs("uploads/oil_photos", exist_ok=True)
                with open(oil_photo_path, "wb") as f:
                    f.write(oil_photo.getbuffer())

                # Save additional photos
                photo_paths = []
                if photos:
                    for photo in photos:
                        photo_path = f"uploads/photos/{photo.name}"
                        os.makedirs("uploads/photos", exist_ok=True)
                        with open(photo_path, "wb") as f:
                            f.write(photo.getbuffer())
                        photo_paths.append(photo_path)

                # Generate a unique submission_id
                submission_id = str(uuid.uuid4())

                # Add to submissions.csv
                df = pd.read_csv(DATA_FILE)
                new_entry = {
                    "submission_id": submission
