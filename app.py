import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime, timedelta

# --- File paths ---
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "submissions.csv")
MILEAGE_FILE = os.path.join(DATA_DIR, "mileage_log.csv")
VEHICLES_FILE = os.path.join(DATA_DIR, "vehicles.csv")
EMPLOYEES_FILE = os.path.join(DATA_DIR, "employees.csv")

# --- Ensure data directory and CSVs exist ---
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize files with headers if missing
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "submission_id","Employee","Vehicle","Date",
        # tires
        "Tire_FL_PSI","Tire_FR_PSI","Tire_RL_PSI","Tire_RR_PSI","Tire_Comments",
        # lights
        "Headlights_OK","Taillights_OK","Brake_Lights_OK","Turn_Signals_OK","Lights_Comments",
        # cleaning
        "Exterior_Washed","Interior_Cleaned","Cleaning_Comments",
        # mileage
        "Mileage","Mileage_Comments",
        # wipers
        "Wipers_OK","Wipers_Comments",
        # fluids
        "Oil_Level_OK","Coolant_Level_OK","Brake_Fluid_OK","Fluids_Comments","Oil_Photo",
        # brakes
        "Brakes_OK","Brakes_Comments",
        # photos & notes
        "Photos","Notes"
    ]).to_csv(DATA_FILE, index=False)

if not os.path.exists(MILEAGE_FILE):
    pd.DataFrame(columns=["submission_id","Employee","Vehicle","Date","Mileage","Mileage_Comments"]).to_csv(MILEAGE_FILE, index=False)

if not os.path.exists(VEHICLES_FILE):
    pd.DataFrame({
        "Vehicle": ["Big Red", "Ugly duckling", "Jeep", "2018", "Black Shoes", "Ranger Danger", "2015", "Pest truck", "Loud Truck", "Karma"]
    }).to_csv(VEHICLES_FILE, index=False)

if not os.path.exists(EMPLOYEES_FILE):
    pd.DataFrame({
        "Employee": ["Cody", "Mason", "Damon", "Colby", "Jake", "Jack", "Kasey", "Hayden", "Casey"],
        "Username": ["Cody", "Mason", "Damon", "Colby", "Jake", "Jack", "Kasey", "Hayden", "Casey"],
        "Password": ["password", "password", "password", "password", "password", "password", "password", "password", "password"],
        "Assigned_Vehicle": ["Big Red", "Ugly duckling", "Jeep", "2018", "Black Shoes", "Ranger Danger", "2015", "Pest truck", "Loud Truck"],
        "Credit_Card": ["None", "Card #2", "Card #3", "None", "None", "None", "None", "None", "None"]
    }).to_csv(EMPLOYEES_FILE, index=False)

# --- Helper functions ---
def load_data(path):
    return pd.read_csv(path)

def save_data(df, path):
    df.to_csv(path, index=False)

# --- Session state defaults ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = ""
    st.session_state.username = ""
    st.session_state.employee_id = ""

# --- Title ---
st.title("Truck Checks App")

# --- Login / Logout ---
def do_login():
    st.subheader("Login")
    with st.form("login_form", clear_on_submit=False):
        user_type = st.selectbox("User Type", ["","Employee","Admin"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if user_type == "Admin" and username == "admin" and password == "admin123":
                st.session_state.update({
                    "logged_in": True,
                    "user_type": "admin",
                    "employee_id": "admin",
                    "username": username
                })
                st.rerun()
            elif user_type == "Employee":
                try:
                    # Force recreate the employees file to ensure clean data
                    emp_data = {
                        "Employee": ["Cody", "Mason", "Damon", "Colby", "Jake", "Jack", "Kasey", "Hayden", "Casey"],
                        "Username": ["Cody", "Mason", "Damon", "Colby", "Jake", "Jack", "Kasey", "Hayden", "Casey"],
                        "Password": ["password", "password", "password", "password", "password", "password", "password", "password", "password"],
                        "Assigned_Vehicle": ["Big Red", "Ugly duckling", "Jeep", "2018", "Black Shoes", "Ranger Danger", "2015", "Pest truck", "Loud Truck"],
                        "Credit_Card": ["None", "Card #2", "Card #3", "None", "None", "None", "None", "None", "None"]
                    }
                    emp_df = pd.DataFrame(emp_data)
                    save_data(emp_df, EMPLOYEES_FILE)
                    
                    # Now load and process
                    emp_df = load_data(EMPLOYEES_FILE)
                    
                    # Clean the data
                    emp_df["Username"] = emp_df["Username"].astype(str).str.strip()
                    emp_df["Password"] = emp_df["Password"].astype(str).str.strip()
                    
                    usr = username.strip()
                    pwd = password.strip()
                    
                    # Case-insensitive username matching
                    match = emp_df[(emp_df["Username"].str.lower() == usr.lower()) & (emp_df["Password"] == pwd)]
                    
                    if not match.empty:
                        st.session_state.update({
                            "logged_in": True,
                            "user_type": "employee",
                            "employee_id": match.iloc[0]["Employee"],
                            "username": usr
                        })
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                except Exception as e:
                    st.error(f"Login error: {str(e)}")
            else:
                st.error("Please select a valid user type and enter credentials.")

def do_logout():
    if st.button("Logout"):
        st.session_state.update({
            "logged_in": False,
            "user_type": "",
            "username": "",
            "employee_id": ""
        })
        st.rerun()

# --- Main ---
if not st.session_state.logged_in:
    do_login()
else:
    do_logout()

    # --- Employee View ---
    if st.session_state.user_type == "employee":
        emp_df = load_data(EMPLOYEES_FILE)
        user_vehicles = emp_df[emp_df["Employee"] == st.session_state.employee_id]["Assigned_Vehicle"].tolist()
        
        st.subheader(f"Welcome, {st.session_state.employee_id}!")
        
        # If employee has multiple vehicles, let them choose
        if len(user_vehicles) > 1:
            vehicle = st.selectbox("Select Vehicle to Check", user_vehicles)
        elif len(user_vehicles) == 1:
            vehicle = user_vehicles[0]
        else:
            st.error("No vehicle assigned to this employee.")
            st.stop()
            
        st.write(f"Vehicle: **{vehicle}**")
        st.markdown("---")

        with st.form("check_form", clear_on_submit=True):
            check_date = st.date_input("Check Date", value=datetime.now())
            date_str = check_date.strftime("%Y-%m-%d")

            st.markdown("#### Tires")
            tire_fl = st.number_input("Front Left PSI", 0, 100, 30)
            tire_fr = st.number_input("Front Right PSI", 0, 100, 30)
            tire_rl = st.number_input("Rear Left PSI", 0, 100, 30)
            tire_rr = st.number_input("Rear Right PSI", 0, 100, 30)
            tire_comments = st.text_area("Tire Comments")

            st.markdown("#### Lights")
            headlights = st.checkbox("Headlights OK")
            taillights = st.checkbox("Taillights OK")
            brake_lights = st.checkbox("Brake Lights OK")
            turn_signals = st.checkbox("Turn Signals OK")
            lights_comments = st.text_area("Lights Comments")

            st.markdown("#### Cleaning")
            exterior = st.checkbox("Exterior Washed")
            interior = st.checkbox("Interior Cleaned")
            cleaning_comments = st.text_area("Cleaning Comments")

            st.markdown("#### Mileage")
            mileage = st.number_input("Current Mileage", 0)
            mileage_comments = st.text_area("Mileage Comments")

            st.markdown("#### Wipers")
            wipers = st.checkbox("Wipers OK")
            wipers_comments = st.text_area("Wipers Comments")

            st.markdown("#### Fluids")
            oil_ok = st.checkbox("Oil Level OK")
            coolant_ok = st.checkbox("Coolant Level OK")
            brake_fluid_ok = st.checkbox("Brake Fluid OK")
            fluids_comments = st.text_area("Fluids Comments")
            oil_photo = st.file_uploader("Upload Oil Photo", type=["jpg","png"])

            st.markdown("#### Brakes")
            brakes_ok = st.checkbox("Brakes OK")
            brakes_comments = st.text_area("Brakes Comments")

            st.markdown("#### Additional Photos & Notes")
            extra_photos = st.file_uploader("Additional Photos", accept_multiple_files=True, type=["jpg","png"])
            notes = st.text_area("Notes")

            if st.form_submit_button("Submit Check"):
                if not oil_photo:
                    st.error("Oil photo is required.")
                else:
                    # Save oil photo
                    os.makedirs("uploads/oil_photos", exist_ok=True)
                    oil_path = f"uploads/oil_photos/{oil_photo.name}"
                    with open(oil_path, "wb") as f:
                        f.write(oil_photo.getbuffer())

                    # Save extra photos
                    photo_paths = []
                    if extra_photos:
                        os.makedirs("uploads/photos", exist_ok=True)
                        for p in extra_photos:
                            pth = f"uploads/photos/{p.name}"
                            with open(pth, "wb") as f:
                                f.write(p.getbuffer())
                            photo_paths.append(pth)

                    # Append submission
                    sid = str(uuid.uuid4())
                    df = load_data(DATA_FILE)
                    entry = {
                        "submission_id": sid,
                        "Employee": st.session_state.employee_id,
                        "Vehicle": vehicle,
                        "Date": date_str,
                        "Tire_FL_PSI": tire_fl,
                        "Tire_FR_PSI": tire_fr,
                        "Tire_RL_PSI": tire_rl,
                        "Tire_RR_PSI": tire_rr,
                        "Tire_Comments": tire_comments,
                        "Headlights_OK": headlights,
                        "Taillights_OK": taillights,
                        "Brake_Lights_OK": brake_lights,
                        "Turn_Signals_OK": turn_signals,
                        "Lights_Comments": lights_comments,
                        "Exterior_Washed": exterior,
                        "Interior_Cleaned": interior,
                        "Cleaning_Comments": cleaning_comments,
                        "Mileage": mileage,
                        "Mileage_Comments": mileage_comments,
                        "Wipers_OK": wipers,
                        "Wipers_Comments": wipers_comments,
                        "Oil_Level_OK": oil_ok,
                        "Coolant_Level_OK": coolant_ok,
                        "Brake_Fluid_OK": brake_fluid_ok,
                        "Fluids_Comments": fluids_comments,
                        "Oil_Photo": oil_path,
                        "Brakes_OK": brakes_ok,
                        "Brakes_Comments": brakes_comments,
                        "Photos": ",".join(photo_paths) if photo_paths else "None",
                        "Notes": notes
                    }
                    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
                    save_data(df, DATA_FILE)

                    # Append mileage
                    mdf = load_data(MILEAGE_FILE)
                    mdf = pd.concat([mdf, pd.DataFrame([{
                        "submission_id": sid,
                        "Employee": st.session_state.employee_id,
                        "Vehicle": vehicle,
                        "Date": date_str,
                        "Mileage": mileage,
                        "Mileage_Comments": mileage_comments
                    }])], ignore_index=True)
                    save_data(mdf, MILEAGE_FILE)

                    st.success("Check submitted!")

    # --- Admin Dashboard ---
    else:
        st.subheader("Admin Dashboard")
        tabs = st.tabs(["🚛 Trucks","👥 Employees","⚙️ Manage Data"])

        # --- Trucks Tab ---
        with tabs[0]:
            st.subheader("Mileage History & Notes")
            vdf = load_data(VEHICLES_FILE)
            sel = st.selectbox("Select Vehicle", vdf["Vehicle"])

            ml = load_data(MILEAGE_FILE)
            if not ml.empty:
                ml["Date"] = pd.to_datetime(ml["Date"])
                hist = ml[ml["Vehicle"] == sel]
                if not hist.empty:
                    st.line_chart(hist.set_index("Date")["Mileage"])
                    st.dataframe(hist[["Date","Employee","Mileage","Mileage_Comments"]])
                else:
                    st.write("No mileage logged for this vehicle.")
            else:
                st.write("No mileage data available.")

            sd = load_data(DATA_FILE)
            if not sd.empty:
                sd["Date"] = pd.to_datetime(sd["Date"])
                rec = sd[sd["Vehicle"] == sel].sort_values("Date", ascending=False)
                st.write("### Recent Notes")
                for _, r in rec.iterrows():
                    if pd.notna(r["Notes"]) and r["Notes"]:
                        st.write(f"{r['Date'].date()} - {r['Employee']} - {r['Notes']}")
            else:
                st.write("No submission data available.")

        # --- Employees Tab ---
        with tabs[1]:
            st.subheader("Employee Check-In Status")
            sd = load_data(DATA_FILE)
            if sd.empty:
                st.write("No submissions yet.")
            else:
                sd["Date"] = pd.to_datetime(sd["Date"])
                sd["Week"] = sd["Date"].dt.isocalendar().week
                week = st.selectbox("Select Week", sorted(sd["Week"].unique(), reverse=True))
                week_df = sd[sd["Week"] == week]

                emp_df = load_data(EMPLOYEES_FILE)
                rows = []
                for _, emp_row in emp_df.iterrows():
                    emp = emp_row["Employee"]
                    vehicle = emp_row["Assigned_Vehicle"]
                    sub = week_df[(week_df["Employee"] == emp) & (week_df["Vehicle"] == vehicle)]
                    rows.append({
                        "Employee": emp,
                        "Vehicle": vehicle,
                        "Submitted": "✅" if not sub.empty else "❌",
                        "Date": sub.iloc[0]["Date"].date() if not sub.empty else "N/A"
                    })
                st.dataframe(pd.DataFrame(rows))

        # --- Manage Data Tab ---
        with tabs[2]:
            st.subheader("Manage Vehicles & Employees")
            # Vehicles
            st.markdown("#### Vehicles")
            vdf = load_data(VEHICLES_FILE)
            new_v = st.text_input("Add New Vehicle", key="new_vehicle")
            if st.button("Add Vehicle") and new_v and new_v not in vdf["Vehicle"].values:
                vdf = pd.concat([vdf, pd.DataFrame([{"Vehicle": new_v}])], ignore_index=True)
                save_data(vdf, VEHICLES_FILE)
                st.rerun()
            for idx, row in vdf.iterrows():
                col1, col2 = st.columns([3,1])
                col1.write(row["Vehicle"])
                if col2.button("Delete", key=f"del_v_{idx}"):
                    vdf = vdf.drop(idx)
                    save_data(vdf, VEHICLES_FILE)
                    st.rerun()

            # Employees
            st.markdown("#### Employees")
            edf = load_data(EMPLOYEES_FILE)
            new_e = st.text_input("Add New Employee Name", key="new_emp")
            new_u = st.text_input("Username", key="new_user")
            new_p = st.text_input("Password", type="password", key="new_pass")
            choice = st.selectbox("Assign Vehicle", [""] + vdf["Vehicle"].tolist(), key="new_assign")
            if st.button("Add Employee") and new_e and new_u and new_p and new_u not in edf["Username"].values:
                edf = pd.concat([edf, pd.DataFrame([{
                    "Employee": new_e,
                    "Username": new_u,
                    "Password": new_p,
                    "Assigned_Vehicle": choice
                }])], ignore_index=True)
                save_data(edf, EMPLOYEES_FILE)
                st.rerun()
            
            st.dataframe(edf)
            
            for idx, row in edf.iterrows():
                col1, col2 = st.columns([3,1])
                col1.write(f"{row['Employee']} - {row['Username']} ({row['Assigned_Vehicle']})")
                if col2.button("Delete", key=f"del_e_{idx}"):
                    edf = edf.drop(idx)
                    save_data(edf, EMPLOYEES_FILE)
                    st.rerun()
