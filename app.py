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

# Ensure data directories and files exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "submission_id","Employee","Vehicle","Date",
        # ... other submission columns ...
    ]).to_csv(DATA_FILE, index=False)
if not os.path.exists(MILEAGE_FILE):
    pd.DataFrame(columns=["submission_id","Employee","Vehicle","Date","Mileage","Mileage_Comments"]).to_csv(MILEAGE_FILE, index=False)
if not os.path.exists(VEHICLES_FILE):
    pd.DataFrame({"Vehicle":["Jeep","Karma","Big Red","Muffin","Loud Truck","2018"]}).to_csv(VEHICLES_FILE, index=False)
if not os.path.exists(EMPLOYEES_FILE):
    pd.DataFrame({
        "Employee":["Cody","Mason","Casey","Kasey","Colby","Jack"],
        "Username":["cody123","mason123","casey123","kasey123","colby123","jack123"],
        "Password":["pass123"]*6,
        "Assigned_Vehicle":["Jeep","Karma","Big Red","Muffin","Loud Truck","2018"]
    }).to_csv(EMPLOYEES_FILE, index=False)

# Load helper
def load_data(path): return pd.read_csv(path)

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.update({"logged_in":False,"employee_id":"","user_type":"","username":""})

st.title("Truck Checks App")

# --- Login ---
if not st.session_state.logged_in:
    st.subheader("Login")
    with st.form("login_form"):
        user_type = st.selectbox("User Type", ["Employee","Admin"], index=0)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if user_type=="Admin" and username=="admin" and password=="admin123":
                st.session_state.update({"logged_in":True,"user_type":"admin","employee_id":"admin","username":"admin"})
                st.experimental_rerun()
            elif user_type=="Employee":
                emp_df = load_data(EMPLOYEES_FILE)
                match = emp_df[(emp_df.Username==username)&(emp_df.Password==password)]
                if not match.empty:
                    st.session_state.update({"logged_in":True,"user_type":"employee","employee_id":match.iloc[0].Employee,"username":username})
                    st.experimental_rerun()
                else: st.error("Wrong credentials")
            else: st.error("Wrong credentials")
    st.stop()

# --- Logout ---
if st.button("Logout"): 
    for k in ["logged_in","employee_id","user_type","username"]: st.session_state[k]=False if k=="logged_in" else ""
    st.experimental_rerun()

# --- Employee View ---
if st.session_state.user_type=="employee":
    emp_df = load_data(EMPLOYEES_FILE)
    emp = emp_df[emp_df.Employee==st.session_state.employee_id].iloc[0]
    vehicle = emp.Assigned_Vehicle
n    st.subheader(f"Welcome, {emp.Employee}! Vehicle: {vehicle}")
    st.markdown("**Check items, upload photo, and Submit**")
    date = st.date_input("Date", value=datetime.now())
    # ... input fields unchanged ...
    oil_photo = st.file_uploader("Upload Oil Photo", type=["jpg","png"])
    if st.button("Submit Check"):
        if not oil_photo: st.error("Oil photo required"); st.stop()
        sid = str(uuid.uuid4())
        df = pd.read_csv(DATA_FILE)
        new = {"submission_id":sid,"Employee":emp.Employee,"Vehicle":vehicle,"Date":date.strftime("%Y-%m-%d")}
        # ... fill other fields ...
        df = pd.concat([df,pd.DataFrame([new])], ignore_index=True)
        df.Date = pd.to_datetime(df.Date)
        df = df[df.Date>=datetime.now()-timedelta(days=60)]
        df.to_csv(DATA_FILE, index=False)
        mdf = pd.read_csv(MILEAGE_FILE)
        mdf = pd.concat([mdf,pd.DataFrame([{"submission_id":sid,"Employee":emp.Employee,"Vehicle":vehicle,"Date":date.strftime("%Y-%m-%d"),"Mileage":0,"Mileage_Comments":""}])], ignore_index=True)
        mdf.Date = pd.to_datetime(mdf.Date)
        mdf = mdf[mdf.Date>=datetime.now()-timedelta(days=365)]
        mdf.to_csv(MILEAGE_FILE, index=False)
        st.success("Submitted!")
    st.stop()

# --- Admin View ---
st.subheader("Admin Dashboard")
tabs = st.tabs(["🚛 Trucks","👥 Check-Ins","⚙️ Manage Data"])

# Trucks and Check-Ins tabs unchanged...

# --- Manage Data Tab ---
with tabs[2]:
    st.subheader("Manage Data")
    st.write("### Vehicles")
    vehicles_df = pd.read_csv(VEHICLES_FILE)
    edited_vehicles = st.experimental_data_editor(vehicles_df, key="vehicles_editor")
    if st.button("Save Vehicles"):
        edited_vehicles.to_csv(VEHICLES_FILE, index=False)
        st.success("Vehicles saved")
        st.experimental_rerun()

    st.write("### Employees")
    employees_df = pd.read_csv(EMPLOYEES_FILE)
    edited_employees = st.experimental_data_editor(employees_df, key="employees_editor")
    if st.button("Save Employees"):
        edited_employees.to_csv(EMPLOYEES_FILE, index=False)
        st.success("Employees saved")
        st.experimental_rerun()
