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

# Helper to load CSVs
def load_data(file_path):
    return pd.read_csv(file_path)

# Ensure CSV files exist
ios.makedirs("data", exist_ok=True)

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
        "Password": ["pass123"] * 6,
        "Assigned_Vehicle": ["Jeep", "Karma", "Big Red", "Muffin", "Loud Truck", "2018"]
    }).to_csv(EMPLOYEES_FILE, index=False)

# Initialize session state
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
        user_type = st.selectbox("User Type", ["", "Employee", "Admin"], index=0)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if not user_type:
                st.error("Please select a User Type")
            elif user_type == "Admin" and username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.user_type = "admin"
                st.session_state.employee_id = "admin"
                st.session_state.username = username
                st.rerun()
            elif user_type == "Employee":
                df_emp = load_data(EMPLOYEES_FILE)
                match = df_emp[(df_emp.Username == username) & (df_emp.Password == password)]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_type = "employee"
                    st.session_state.employee_id = match.iloc[0]["Employee"]
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Wrong username or password")
            else:
                st.error("Wrong username or password")
    st.stop()

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

    # Date
    check_date = st.date_input("Check Date", value=datetime.now())
    date_str = check_date.strftime("%Y-%m-%d")

    # Tires
    st.subheader("Tires")
    tire_fl_psi = st.number_input("Front Left Tire Pressure (PSI)", 0, 100, 30)
    tire_fr_psi = st.number_input("Front Right Tire Pressure (PSI)", 0, 100, 30)
    tire_rl_psi = st.number_input("Rear Left Tire Pressure (PSI)", 0, 100, 30)
    tire_rr_psi = st.number_input("Rear Right Tire Pressure (PSI)", 0, 100, 30)
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
    mileage = st.number_input("Current Mileage", 0)
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

    # Additional Photos & Notes
    photos = st.file_uploader("Upload Additional Photos (Optional)", accept_multiple_files=True, type=["jpg", "png"])
    notes = st.text_area("Any issues or thoughts?")

    if st.button("Submit Check", type="primary"):
        if not oil_photo:
            st.error("Oil level photo is required!")
        else:
            # Save oil photo
            os.makedirs("uploads/oil_photos", exist_ok=True)
            oil_path = f"uploads/oil_photos/{oil_photo.name}"
            with open(oil_path, "wb") as f:
                f.write(oil_photo.getbuffer())

            # Save additional photos
            photo_paths = []
            if photos:
                os.makedirs("uploads/photos", exist_ok=True)
                for p in photos:
                    pth = f"uploads/photos/{p.name}"
                    with open(pth, "wb") as f:
                        f.write(p.getbuffer())
                    photo_paths.append(pth)

            # Append to submissions
            sid = str(uuid.uuid4())
            sdf = pd.read_csv(DATA_FILE)
            new_entry = {
                "submission_id": sid,
                "Employee": st.session_state.employee_id,
                "Vehicle": assigned_vehicle,
                "Date": date_str,
                "Tire_FL_PSI": tire_fl_psi,
                "Tire_FR_PSI": tire_fr_psi,
                "Tire_RL_PSI": tire_rl_psi,
                "Tire_RR_PSI": tire_rr_psi,
                "Tire_Comments": tire_comments,
                "Headlights_OK": headlights_ok,
                "Taillights_OK": taillights_ok,
                "Brake_Lights_OK": brake_lights_ok,
                "Turn_Signals_OK": turn_signals_ok,
                "Lights_Comments": lights_comments,
                "Exterior_Washed": exterior_washed,
                "Interior_Cleaned": interior_cleaned,
                "Cleaning_Comments": cleaning_comments,
                "Mileage": mileage,
                "Mileage_Comments": mileage_comments,
                "Wipers_OK": wipers_ok,
                "Wipers_Comments": wipers_comments,
                "Oil_Level_OK": oil_level_ok,
                "Coolant_Level_OK": coolant_level_ok,
                "Brake_Fluid_OK": brake_fluid_ok,
                "Fluids_Comments": fluids_comments,
                "Oil_Photo": oil_path,
                "Brakes_OK": brakes_ok,
                "Brakes_Comments": brakes_comments,
                "Photos": ",".join(photo_paths) if photo_paths else "None",
                "Notes": notes
            }
            sdf = pd.concat([sdf, pd.DataFrame([new_entry])], ignore_index=True)
            sdf["Date"] = pd.to_datetime(sdf["Date"])
            sdf = sdf[sdf["Date"] >= datetime.now() - timedelta(days=60)]
            sdf.to_csv(DATA_FILE, index=False)

            # Append to mileage log
            mdf = pd.read_csv(MILEAGE_FILE)
            ml_entry = {"submission_id": sid, "Employee": st.session_state.employee_id, "Vehicle": assigned_vehicle, "Date": date_str, "Mileage": mileage, "Mileage_Comments": mileage_comments}
            mdf = pd.concat([mdf, pd.DataFrame([ml_entry])], ignore_index=True)
            mdf["Date"] = pd.to_datetime(mdf["Date"])
            mdf = mdf[mdf["Date"] >= datetime.now() - timedelta(days=365)]
            mdf.to_csv(MILEAGE_FILE, index=False)

            st.success("Check submitted! Thank you.")
    st.stop()

# --------------------------------
# ADMIN VIEW
# --------------------------------
else:
    st.subheader("Admin Dashboard")
    tabs = st.tabs([
        "🚛 Trucks",
        "👥 Employees",
        "⚙️ Manage Data"
    ])

    # Trucks Tab
    with tabs[0]:
        st.subheader("Truck Overview")
        vehicles_df = pd.read_csv(VEHICLES_FILE)
        selected = st.selectbox("Select Vehicle", vehicles_df["Vehicle"])
        # Mileage History
        with st.container():
            st.write("### Mileage History (1 Year)")
            ml = pd.read_csv(MILEAGE_FILE)
            ml["Date"] = pd.to_datetime(ml["Date"])
            vm = ml[ml["Vehicle"] == selected]
            if not vm.empty:
                st.line_chart(vm.set_index("Date")["Mileage"])
                st.dataframe(vm[["Date","Employee","Mileage","Mileage_Comments"]])
            else:
                st.write("No data.")

        # Recent Notes
        df_sub = pd.read_csv(DATA_FILE)
        df_sub["Date"] = pd.to_datetime(df_sub["Date"])
        vs = df_sub[df_sub["Vehicle"] == selected].sort_values("Date", ascending=False)
        with st.container():
            st.write("### Recent Notes (2 Months)")
            cutoff = datetime.now() - timedelta(days=60)
            for _, r in vs.iterrows():
                if pd.notna(r["Notes"]) and r["Date"] >= cutoff:
                    st.write(f"{r['Date'].date()} - {r['Employee']} - {r['Notes']}")

        # Recent Submissions
        with st.container():
            st.write("### Recent Submissions (Last 5)")
            for _, r in vs.head(5).iterrows():
                with st.expander(f"{r['Employee']} - {r['Date'].date()}"):
                    st.write(r.to_dict())
                    if st.button("Delete", key=r['submission_id']):
                        dfa = pd.read_csv(DATA_FILE)
                        dfa = dfa[dfa['submission_id'] != r['submission_id']]
                        dfa.to_csv(DATA_FILE, index=False)
                        mla = pd.read_csv(M

