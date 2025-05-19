```python
import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime, timedelta

# File paths
DATA_FILE = "data/submissions.csv"
MILEAGE_FILE = "data/mileage_log.csv"
VEHICLES_FILE = "data/vehicles.csv"
EMPLOYEES_FILE = "data/employees.csv"

# Ensure data directory and files exist
os.makedirs("data", exist_ok=True)

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "submission_id", "Employee", "Vehicle", "Date",
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
        "submission_id", "Employee", "Vehicle", "Date", "Mileage", "Mileage_Comments"
    ]).to_csv(MILEAGE_FILE, index=False)

if not os.path.exists(VEHICLES_FILE):
    pd.DataFrame({"Vehicle": ["Jeep", "Karma", "Big Red", "Muffin", "Loud Truck", "2018"]}) \
        .to_csv(VEHICLES_FILE, index=False)

if not os.path.exists(EMPLOYEES_FILE):
    pd.DataFrame({
        "Employee": ["Cody", "Mason", "Casey", "Kasey", "Colby", "Jack"],
        "Username": ["cody123", "mason123", "casey123", "kasey123", "colby123", "jack123"],
        "Password": ["pass123"] * 6,
        "Assigned_Vehicle": ["Jeep", "Karma", "Big Red", "Muffin", "Loud Truck", "2018"]
    }).to_csv(EMPLOYEES_FILE, index=False)

# Helper to load CSVs
def load_data(path):
    return pd.read_csv(path)

# Init session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = ""
    st.session_state.employee_id = ""
    st.session_state.username = ""

st.title("Truck Checks App")

# --- LOGIN ---
if not st.session_state.logged_in:
    st.subheader("Login")
    with st.form("login_form"):
        user_type = st.selectbox("User Type", ["Employee", "Admin"], index=0)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if user_type == "Admin" and username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.user_type = "admin"
                st.session_state.employee_id = "admin"
                st.session_state.username = username
                st.experimental_rerun()
            elif user_type == "Employee":
                df_emp = load_data(EMPLOYEES_FILE)
                match = df_emp[(df_emp.Username == username) & (df_emp.Password == password)]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_type = "employee"
                    st.session_state.employee_id = match.iloc[0]["Employee"]
                    st.session_state.username = username
                    st.experimental_rerun()
                else:
                    st.error("Wrong username or password")
            else:
                st.error("Wrong username or password")
    st.stop()

# --- LOGOUT ---
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = ""
    st.session_state.employee_id = ""
    st.session_state.username = ""
    st.experimental_rerun()

# --- EMPLOYEE VIEW ---
if st.session_state.user_type == "employee":
    employees_df = load_data(EMPLOYEES_FILE)
    emp_row = employees_df[employees_df["Employee"] == st.session_state.employee_id].iloc[0]
    assigned_vehicle = emp_row["Assigned_Vehicle"]

    st.subheader(f"Welcome, {emp_row['Employee']}! Vehicle: {assigned_vehicle}")
    st.markdown("**Instructions**: Check all items, upload photos if needed, and hit Submit—done!")

    # Date
    check_date = st.date_input("Check Date", value=datetime.now())
    date_str = check_date.strftime("%Y-%m-%d")

    # --- (inputs for tires, lights, cleaning, mileage, wipers, fluids, brakes) ---
    # For brevity, assume your original inputs remain here unchanged
    # … your st.number_input, st.checkbox, st.text_area, st.file_uploader, etc. …

    # Example oil photo requirement
    oil_photo = st.file_uploader("Upload Oil Level Photo (Required)", type=["jpg", "png"])

    if st.button("Submit Check", type="primary"):
        if not oil_photo:
            st.error("Oil level photo is required!")
            st.stop()
        # Save files and append rows to submissions & mileage logs as in your original code
        # … existing save logic …
        st.success("Check submitted! Thank you.")
    st.stop()

# --- ADMIN VIEW ---
st.subheader("Admin Dashboard")
tabs = st.tabs(["🚛 Trucks", "👥 Employees", "⚙️ Manage Data"])

# Trucks Tab
with tabs[0]:
    st.subheader("Truck Overview")
    vehicles_df = load_data(VEHICLES_FILE)
    selected = st.selectbox("Select Vehicle", vehicles_df["Vehicle"])
    # … your mileage chart, recent notes, recent submissions …

# Employees Tab
with tabs[1]:
    st.subheader("Employee Check-Ins")
    df_sub = load_data(DATA_FILE)
    emp_df = load_data(EMPLOYEES_FILE)
    if not df_sub.empty:
        df_sub["Date"] = pd.to_datetime(df_sub["Date"])
        # … your weekly check-in logic and display …
    else:
        st.write("No submissions yet.")

# Manage Data Tab (editable tables)
with tabs[2]:
    st.subheader("Manage Data")

    st.write("### Vehicles")
    vehicles_df = load_data(VEHICLES_FILE)
    edited_vehicles = st.experimental_data_editor(vehicles_df, num_rows="dynamic")
    if st.button("Save Vehicles"):
        edited_vehicles.to_csv(VEHICLES_FILE, index=False)
        st.success("Vehicles updated")

    st.write("### Employees")
    employees_df = load_data(EMPLOYEES_FILE)
    edited_employees = st.experimental_data_editor(employees_df, num_rows="dynamic")
    if st.button("Save Employees"):
        edited_employees.to_csv(EMPLOYEES_FILE, index=False)
        st.success("Employees updated")
```
