import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime, timedelta

# Inject custom CSS for styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    body {
        font-family: 'Poppins', sans-serif;
        background-color: #f5f5f5;
    }
    .stApp {
        background-color: #f5f5f5;
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
    }
    h2, h3 {
        color: #34495e;
        font-weight: 600;
    }
    .stButton>button {
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stButton>button[kind="primary"] {
        background-color: #27ae60;
        color: white;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #219653;
    }
    .stButton>button[kind="secondary"] {
        background-color: #3498db;
        color: white;
    }
    .stButton>button[kind="secondary"]:hover {
        background-color: #2980b9;
    }
    /* Style buttons with "Delete" in the label as red */
    .stButton>button[label*="Delete"] {
        background-color: #e74c3c;
        color: white;
    }
    .stButton>button[label*="Delete"]:hover {
        background-color: #c0392b;
    }
    /* Ensure selectbox and text inputs are readable on all devices */
    .stSelectbox>div>div, .stTextInput>div>input {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border-radius: 8px;
        border: 1px solid #bdc3c7;
        padding: 10px;
        font-size: 16px;
    }
    /* Fix placeholder text color */
    .stTextInput>div>input::placeholder {
        color: #7f8c8d !important;
        opacity: 1;
    }
    .stExpander {
        border: 1px solid #ecf0f1;
        border-radius: 8px;
        background-color: #ffffff;
        margin-bottom: 10px;
    }
    .stExpander:hover {
        background-color: #f9f9f9;
    }
    .card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    /* Mobile-specific styles */
    @media only screen and (max-width: 600px) {
        /* Force light theme on mobile */
        .stApp {
            background-color: #f5f5f5 !important;
            color: #2c3e50 !important;
        }
        /* Center the title and subheader */
        h1, h2 {
            text-align: center;
        }
        /* Adjust the form container to be more mobile-friendly */
        div[data-testid="stForm"] {
            padding: 15px !important;
            background-color: #ffffff !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
            margin: 10px 0 !important;
        }
        /* Make selectbox and text inputs full-width with better spacing */
        div[data-testid="stSelectbox"], div[data-testid="stTextInput"] {
            margin-bottom: 15px !important;
        }
        div[data-testid="stSelectbox"]>div>div, div[data-testid="stTextInput"]>div>input {
            width: 100% !important;
            padding: 12px !important;
            font-size: 16px !important;
            border-radius: 8px !important;
            border: 1px solid #bdc3c7 !important;
            box-sizing: border-box !important;
            background-color: #ffffff !important;
            color: #2c3e50 !important;
        }
        /* Fix selectbox dropdown items */
        div[data-testid="stSelectbox"] ul {
            background-color: #ffffff !important;
            color: #2c3e50 !important;
        }
        div[data-testid="stSelectbox"] li {
            color: #2c3e50 !important;
        }
        /* Style the login button for mobile */
        div[data-testid="stFormSubmitButton"]>button {
            width: 100% !important;
            padding: 15px !important;
            font-size: 18px !important;
            background-color: #27ae60 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            margin-top: 10px !important;
        }
        div[data-testid="stFormSubmitButton"]>button:hover {
            background-color: #219653 !important;
        }
        /* Add spacing around the form */
        div[data-testid="stForm"]>div {
            display: flex !important;
            flex-direction: column !important;
            gap: 15px !important;
        }
        /* Ensure the app container has padding on mobile */
        .stApp {
            padding: 10px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Files to store data
DATA_FILE = "data/submissions.csv"
MILEAGE_FILE = "data/mileage_log.csv"
VEHICLES_FILE = "data/vehicles.csv"
EMPLOYEES_FILE = "data/employees.csv"

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Make sure CSV files exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "submission_id",  # NEW unique ID column
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
        "submission_id",  # NEW unique ID column
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
    user_type = st.selectbox("User Type", ["Employee", "Admin"])
    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if user_type == "Admin" and username == "admin" and password == "admin123":
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
                    "submission_id": submission_id,
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
                    "Oil_Photo": oil_photo_path,
                    "Brakes_OK": brakes_ok,
                    "Brakes_Comments": brakes_comments,
                    "Photos": ",".join(photo_paths) if photo_paths else "None",
                    "Notes": notes
                }
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

                # Clean up old (2 months) data
                df["Date"] = pd.to_datetime(df["Date"])
                cutoff_2mo = datetime.now() - timedelta(days=60)
                df = df[df["Date"] >= cutoff_2mo]
                df.to_csv(DATA_FILE, index=False)

                # Add to mileage_log.csv
                mileage_df = pd.read_csv(MILEAGE_FILE)
                new_mileage = {
                    "submission_id": submission_id,
                    "Employee": st.session_state.employee_id,
                    "Vehicle": assigned_vehicle,
                    "Date": date_str,
                    "Mileage": mileage,
                    "Mileage_Comments": mileage_comments
                }
                mileage_df = pd.concat([mileage_df, pd.DataFrame([new_mileage])], ignore_index=True)

                # Clean up old (1 year) mileage
                mileage_df["Date"] = pd.to_datetime(mileage_df["Date"])
                cutoff_1yr = datetime.now() - timedelta(days=365)
                mileage_df = mileage_df[mileage_df["Date"] >= cutoff_1yr]
                mileage_df.to_csv(MILEAGE_FILE, index=False)

                st.success("Check submitted! Thank you.")

    # --------------------------------
    # ADMIN VIEW
    # --------------------------------
    else:
        st.subheader("Admin Dashboard")
        tabs = st.tabs(["🚛 Trucks", "👥 Employees", "⚙️ Manage Data"])

        # Trucks Tab
        with tabs[0]:
            st.subheader("Truck Overview")
            vehicles_df = load_data(VEHICLES_FILE)
            selected_vehicle = st.selectbox("Select Vehicle", vehicles_df["Vehicle"])
            
            # Mileage History
            with st.container(key="milage_container"):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write("### Mileage History (1 Year)")
                mileage_df = load_data(MILEAGE_FILE)
                # convert to datetime so we can chart
                mileage_df["Date"] = pd.to_datetime(mileage_df["Date"])
                vehicle_mileage = mileage_df[mileage_df["Vehicle"] == selected_vehicle].copy()
                if not vehicle_mileage.empty:
                    st.line_chart(vehicle_mileage.set_index("Date")["Mileage"])
                    st.dataframe(vehicle_mileage[["Date", "Employee", "Mileage", "Mileage_Comments"]])
                else:
                    st.write("No mileage data for this vehicle.")
                st.markdown('</div>', unsafe_allow_html=True)

            # Recent Notes
            with st.container(key="notes_container"):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write("### Recent Notes (2 Months)")
                df = load_data(DATA_FILE)
                df["Date"] = pd.to_datetime(df["Date"])
                vehicle_submissions = df[df["Vehicle"] == selected_vehicle].copy()
                if not vehicle_submissions.empty:
                    vehicle_submissions = vehicle_submissions.sort_values(by="Date", ascending=False)
                    for _, row in vehicle_submissions.iterrows():
                        if pd.notna(row["Notes"]) and row["Notes"]:
                            st.write(f"{row['Date']} - {row['Employee']} - {row['Notes']}")
                else:
                    st.write("No recent notes for this vehicle.")
                st.markdown('</div>', unsafe_allow_html=True)

            # Recent Oil Photos
            with st.container(key="oil_photos_container"):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write("### Recent Oil Photos (2 Months)")
                if not vehicle_submissions.empty:
                    for _, row in vehicle_submissions.iterrows():
                        if pd.notna(row["Oil_Photo"]) and row["Oil_Photo"] != "None":
                            st.write(f"{row['Date']} - {row['Employee']}")
                            try:
                                st.image(row["Oil_Photo"], caption="Oil Level Photo", use_container_width=True)
                            except:
                                st.write(f"Could not load oil photo: {row['Oil_Photo']}")
                else:
                    st.write("No recent oil photos for this vehicle.")
                st.markdown('</div>', unsafe_allow_html=True)

            # Recent Submissions
            with st.container(key="submissions_container"):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write("### Recent Submissions (Last 5)")
                if not vehicle_submissions.empty:
                    recent_submissions = vehicle_submissions.head(5)
                    for idx, row in recent_submissions.iterrows():
                        with st.expander(f"{row['Employee']} - {row['Date']}"):
                            st.write("**Tires**")
                            st.write(f"Front Left: {row['Tire_FL_PSI']} PSI")
                            st.write(f"Front Right: {row['Tire_FR_PSI']} PSI")
                            st.write(f"Rear Left: {row['Tire_RL_PSI']} PSI")
                            st.write(f"Rear Right: {row['Tire_RR_PSI']} PSI")
                            st.write(f"Comments: {row['Tire_Comments']}")
                            st.write("**Lights**")
                            st.write(f"Headlights OK: {row['Headlights_OK']}")
                            st.write(f"Taillights OK: {row['Taillights_OK']}")
                            st.write(f"Brake Lights OK: {row['Brake_Lights_OK']}")
                            st.write(f"Turn Signals OK: {row['Turn_Signals_OK']}")
                            st.write(f"Comments: {row['Lights_Comments']}")
                            st.write("**Cleaning**")
                            st.write(f"Exterior Washed: {row['Exterior_Washed']}")
                            st.write(f"Interior Cleaned: {row['Interior_Cleaned']}")
                            st.write(f"Comments: {row['Cleaning_Comments']}")
                            st.write("**Mileage**")
                            st.write(f"Mileage: {row['Mileage']}")
                            st.write(f"Comments: {row['Mileage_Comments']}")
                            st.write("**Wipers**")
                            st.write(f"Wipers OK: {row['Wipers_OK']}")
                            st.write(f"Comments: {row['Wipers_Comments']}")
                            st.write("**Fluids**")
                            st.write(f"Oil Level OK: {row['Oil_Level_OK']}")
                            st.write(f"Coolant Level OK: {row['Coolant_Level_OK']}")
                            st.write(f"Brake Fluid OK: {row['Brake_Fluid_OK']}")
                            st.write(f"Comments: {row['Fluids_Comments']}")
                            st.write("**Oil Level Photo**")
                            if pd.notna(row["Oil_Photo"]) and row["Oil_Photo"] != "None":
                                try:
                                    st.image(row["Oil_Photo"], caption="Oil Level Photo", use_container_width=True)
                                except:
                                    st.write(f"Could not load oil photo: {row['Oil_Photo']}")
                            else:
                                st.write("No oil photo uploaded.")
                            st.write("**Brakes**")
                            st.write(f"Brakes OK: {row['Brakes_OK']}")
                            st.write(f"Comments: {row['Brakes_Comments']}")
                            st.write("**Additional Photos**")
                            if pd.notna(row["Photos"]) and row["Photos"] != "None":
                                photo_paths = row["Photos"].split(",")
                                for photo_path in photo_paths:
                                    try:
                                        st.image(photo_path, caption=photo_path, use_container_width=True)
                                    except:
                                        st.write(f"Could not load photo: {photo_path}")
                            else:
                                st.write("No additional photos uploaded.")
                            st.write("**Notes**")
                            st.write(row["Notes"])

                            # Delete by submission_id
                            if st.button("Delete this submission", key=f"delete_{row['submission_id']}"):
                                df = load_data(DATA_FILE)
                                mileage_df = load_data(MILEAGE_FILE)

                                # Remove from submissions
                                df = df[df["submission_id"] != row["submission_id"]]
                                df.to_csv(DATA_FILE, index=False)

                                # Remove from mileage
                                mileage_df = mileage_df[mileage_df["submission_id"] != row["submission_id"]]
                                mileage_df.to_csv(MILEAGE_FILE, index=False)

                                st.success("Submission deleted from both CSVs.")
                                st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

        # --------------------------------
        # EMPLOYEES TAB
        # --------------------------------
        with tabs[1]:
            st.subheader("Employee Check-Ins")
            df = load_data(DATA_FILE)
            employees_df = load_data(EMPLOYEES_FILE)

            if not df.empty:
                df["Date"] = pd.to_datetime(df["Date"])
                df["Week Start"] = df["Date"].dt.to_period("W").apply(lambda r: r.start_time)
                weeks = sorted(df["Week Start"].unique(), reverse=True)
                selected_week = st.selectbox(
                    "Select Week",
                    weeks,
                    format_func=lambda x: x.strftime("%Y/%m/%d")
                )
                week_start = pd.to_datetime(selected_week)
                week_end = week_start + timedelta(days=6)
                week_df = df[(df["Date"] >= week_start) & (df["Date"] <= week_end)]

                # Build employee check-in table
                checkin_data = []
                for _, emp in employees_df.iterrows():
                    emp_name = emp["Employee"]
                    assigned_vehicle = emp["Assigned_Vehicle"]
                    subset = week_df[week_df["Employee"] == emp_name]
                    if not subset.empty:
                        status = "Submitted"
                        date_submitted = pd.to_datetime(subset.iloc[0]["Date"]).strftime("%Y-%m-%d")
                    else:
                        status = "Not Submitted"
                        date_submitted = "N/A"
                    checkin_data.append({
                        "Employee": emp_name,
                        "Assigned Vehicle": assigned_vehicle if assigned_vehicle else "No Vehicle",
                        "Check-In Status": status,
                        "Date Submitted": date_submitted
                    })

                checkin_df = pd.DataFrame(checkin_data)
                checkin_df["Date Submitted"] = checkin_df["Date Submitted"].astype(str)

                def color_status(val):
                    return "background-color: green" if val == "Submitted" else "background-color: red"

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write("### Weekly Check-Ins")
                st.dataframe(checkin_df.style.map(color_status, subset=["Check-In Status"]))
                st.markdown('</div>', unsafe_allow_html=True)

                # Employee details
                st.markdown('<div class="card">', unsafe_allow_html=True)
                selected_emp = st.selectbox("View Employee Details", checkin_df["Employee"])
                emp_submissions = week_df[week_df["Employee"] == selected_emp]
                if not emp_submissions.empty:
                    st.write(f"### Submissions for {selected_emp}")
                    for idx, row in emp_submissions.iterrows():
                        with st.expander(f"{row['Vehicle']} - {row['Date']}"):
                            st.write("**Tires**")
                            st.write(f"Front Left: {row['Tire_FL_PSI']} PSI")
                            st.write(f"Front Right: {row['Tire_FR_PSI']} PSI")
                            st.write(f"Rear Left: {row['Tire_RL_PSI']} PSI")
                            st.write(f"Rear Right: {row['Tire_RR_PSI']} PSI")
                            st.write(f"Comments: {row['Tire_Comments']}")
                            st.write("**Lights**")
                            st.write(f"Headlights OK: {row['Headlights_OK']}")
                            st.write(f"Taillights OK: {row['Taillights_OK']}")
                            st.write(f"Brake Lights OK: {row['Brake_Lights_OK']}")
                            st.write(f"Turn Signals OK: {row['Turn_Signals_OK']}")
                            st.write(f"Comments: {row['Lights_Comments']}")
                            st.write("**Cleaning**")
                            st.write(f"Exterior Washed: {row['Exterior_Washed']}")
                            st.write(f"Interior Cleaned: {row['Interior_Cleaned']}")
                            st.write(f"Comments: {row['Cleaning_Comments']}")
                            st.write("**Mileage**")
                            st.write(f"Mileage: {row['Mileage']}")
                            st.write(f"Comments: {row['Mileage_Comments']}")
                            st.write("**Wipers**")
                            st.write(f"Wipers OK: {row['Wipers_OK']}")
                            st.write(f"Comments: {row['Wipers_Comments']}")
                            st.write("**Fluids**")
                            st.write(f"Oil Level OK: {row['Oil_Level_OK']}")
                            st.write(f"Coolant Level OK: {row['Coolant_Level_OK']}")
                            st.write(f"Brake Fluid OK: {row['Brake_Fluid_OK']}")
                            st.write(f"Comments: {row['Fluids_Comments']}")
                            st.write("**Oil Level Photo**")
                            if pd.notna(row["Oil_Photo"]) and row["Oil_Photo"] != "None":
                                try:
                                    st.image(row["Oil_Photo"], caption="Oil Level Photo", use_container_width=True)
                                except:
                                    st.write(f"Could not load oil photo: {row['Oil_Photo']}")
                            else:
                                st.write("No oil photo uploaded.")
                            st.write("**Brakes**")
                            st.write(f"Brakes OK: {row['Brakes_OK']}")
                            st.write(f"Comments: {row['Brakes_Comments']}")
                            st.write("**Additional Photos**")
                            if pd.notna(row["Photos"]) and row["Photos"] != "None":
                                photo_paths = row["Photos"].split(",")
                                for photo_path in photo_paths:
                                    try:
                                        st.image(photo_path, caption=photo_path, use_container_width=True)
                                    except:
                                        st.write(f"Could not load photo: {photo_path}")
                            else:
                                st.write("No additional photos uploaded.")
                            st.write("**Notes**")
                            st.write(row["Notes"])

                            # Delete button using submission_id
                            if st.button("Delete this submission", key=f"delete_{row['submission_id']}"):
                                df = load_data(DATA_FILE)
                                mileage_df = load_data(MILEAGE_FILE)
                                
                                # Remove from submissions
                                df = df[df["submission_id"] != row["submission_id"]]
                                df.to_csv(DATA_FILE, index=False)

                                # Remove from mileage
                                mileage_df = mileage_df[mileage_df["submission_id"] != row["submission_id"]]
                                mileage_df.to_csv(MILEAGE_FILE, index=False)

                                st.success("Submission deleted.")
                                st.rerun()
                else:
                    st.write(f"No submissions for {selected_emp} this week.")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.write("No submissions yet.")

        # --------------------------------
        # MANAGE DATA TAB
        # --------------------------------
        with tabs[2]:
            st.subheader("Manage Data")
            manage_tabs = st.tabs(["Manage Vehicles", "Manage Employees"])

            # Manage Vehicles
            with manage_tabs[0]:
                st.write("### Manage Vehicles")
                vehicles_df = load_data(VEHICLES_FILE)
                employees_df = load_data(EMPLOYEES_FILE)
                vehicles_df["Assigned To"] = vehicles_df["Vehicle"].apply(
                    lambda x: employees_df[employees_df["Assigned_Vehicle"] == x]["Employee"].iloc[0]
                    if x in employees_df["Assigned_Vehicle"].values else "Unassigned"
                )
                st.dataframe(vehicles_df)

                st.write("#### Add Vehicle")
                with st.form(key="add_vehicle_form"):
                    new_vehicle = st.text_input("New Vehicle Name")
                    if st.form_submit_button("Add Vehicle", type="primary"):
                        if new_vehicle and new_vehicle not in vehicles_df["Vehicle"].values:
                            vehicles_df = pd.concat([vehicles_df, pd.DataFrame({"Vehicle": [new_vehicle], "Assigned To": ["Unassigned"]})], ignore_index=True)
                            vehicles_df.to_csv(VEHICLES_FILE, index=False)
                            st.success(f"Added {new_vehicle}")
                            st.rerun()
                        else:
                            st.error("Vehicle name cannot be empty or already exists.")

                for idx, row in vehicles_df.iterrows():
                    with st.expander(f"Edit or Delete {row['Vehicle']}"):
                        col1, col2, col3 = st.columns([1,1,1])
                        with col1:
                            # Edit form
                            with st.form(key=f"edit_vehicle_{idx}"):
                                new_name = st.text_input("Edit Vehicle Name", value=row["Vehicle"], key=f"edit_vehicle_input_{idx}")
                                submitted_edit = st.form_submit_button("Edit", type="secondary")
                                if submitted_edit:
                                    if new_name and new_name not in vehicles_df["Vehicle"].values:
                                        old_name = row["Vehicle"]
                                        vehicles_df.at[idx, "Vehicle"] = new_name
                                        vehicles_df.to_csv(VEHICLES_FILE, index=False)

                                        # Update employees, submissions, mileage
                                        employees_df["Assigned_Vehicle"] = employees_df["Assigned_Vehicle"].replace(old_name, new_name)
                                        employees_df.to_csv(EMPLOYEES_FILE, index=False)

                                        df = load_data(DATA_FILE)
                                        df["Vehicle"] = df["Vehicle"].replace(old_name, new_name)
                                        df.to_csv(DATA_FILE, index=False)

                                        mileage_df = load_data(MILEAGE_FILE)
                                        mileage_df["Vehicle"] = mileage_df["Vehicle"].replace(old_name, new_name)
                                        mileage_df.to_csv(MILEAGE_FILE, index=False)

                                        st.success(f"Updated vehicle to {new_name}")
                                        st.rerun()
                                    else:
                                        st.error("Vehicle name cannot be empty or already exists.")

                        with col2:
                            # Assign
                            with st.form(key=f"assign_vehicle_{idx}"):
                                available_emps = [""] + [emp for emp in employees_df["Employee"] if emp not in employees_df[employees_df["Assigned_Vehicle"] != ""]["Employee"].values]
                                assigned_emps = [
                                    f"{emp} (Assigned to {employees_df[employees_df['Employee'] == emp]['Assigned_Vehicle'].iloc[0]})"
                                    for emp in employees_df["Employee"]
                                    if emp not in available_emps and emp != ""
                                ]
                                employee_options = available_emps + assigned_emps
                                selected_emp = st.selectbox("Assign Employee", employee_options, key=f"assign_emp_{idx}")
                                submitted_assign = st.form_submit_button("Assign", type="primary")
                                if submitted_assign:
                                    if selected_emp:
                                        if selected_emp in available_emps:
                                            employees_df.loc[employees_df["Employee"] == selected_emp, "Assigned_Vehicle"] = row["Vehicle"]
                                            employees_df.to_csv(EMPLOYEES_FILE, index=False)
                                            st.success(f"Assigned {selected_emp} to {row['Vehicle']}")
                                            st.rerun()
                                        else:
                                            emp_name = selected_emp.split(" (Assigned to")[0]
                                            current_vehicle = employees_df[employees_df["Employee"] == emp_name]["Assigned_Vehicle"].iloc[0]
                                            st.warning(f"{emp_name} is already assigned to {current_vehicle}. Reassign to {row['Vehicle']}?")
                                            if st.button("Yes, Reassign", key=f"reassign_{idx}"):
                                                employees_df.loc[employees_df["Assigned_Vehicle"] == current_vehicle, "Assigned_Vehicle"] = ""
                                                employees_df.loc[employees_df["Employee"] == emp_name, "Assigned_Vehicle"] = row["Vehicle"]
                                                employees_df.to_csv(EMPLOYEES_FILE, index=False)
                                                st.success(f"Reassigned {emp_name} to {row['Vehicle']}")
                                                st.rerun()

                        with col3:
                            # Delete
                            if st.button("Delete Vehicle", key=f"delete_vehicle_{idx}", type="secondary"):
                                if st.checkbox("Confirm deletion", key=f"confirm_delete_vehicle_{idx}"):
                                    vehicle_name = row["Vehicle"]
                                    vehicles_df = vehicles_df.drop(idx)
                                    vehicles_df.to_csv(VEHICLES_FILE, index=False)

                                    # unassign from employees
                                    employees_df["Assigned_Vehicle"] = employees_df["Assigned_Vehicle"].replace(vehicle_name, "")
                                    employees_df.to_csv(EMPLOYEES_FILE, index=False)

                                    # remove from submissions + mileage
                                    df = load_data(DATA_FILE)
                                    df = df[df["Vehicle"] != vehicle_name]
                                    df.to_csv(DATA_FILE, index=False)

                                    mileage_df = load_data(MILEAGE_FILE)
                                    mileage_df = mileage_df[mileage_df["Vehicle"] != vehicle_name]
                                    mileage_df.to_csv(MILEAGE_FILE, index=False)

                                    st.success(f"Deleted vehicle {vehicle_name}")
                                    st.rerun()

            # Manage Employees
            with manage_tabs[1]:
                st.write("### Manage Employees")
                employees_df = load_data(EMPLOYEES_FILE)
                st.dataframe(employees_df)

                # Add employee
                st.write("#### Add Employee")
                with st.form(key="add_employee_form"):
                    new_emp = st.text_input("Employee Name")
                    new_user = st.text_input("Username")
                    new_pass = st.text_input("Password", type="password")
                    vehicles_df = load_data(VEHICLES_FILE)
                    av_vehicles = [""] + [v for v in vehicles_df["Vehicle"] if v not in employees_df["Assigned_Vehicle"].values]
                    as_vehicles = [
                        f"{v} (Assigned to {employees_df[employees_df['Assigned_Vehicle'] == v]['Employee'].iloc[0]})"
                        for v in vehicles_df["Vehicle"] if v not in av_vehicles and v != ""
                    ]
                    vehicle_opts = av_vehicles + as_vehicles
                    new_assigned = st.selectbox("Assigned Vehicle", vehicle_opts)
                    submitted_new_emp = st.form_submit_button("Add Employee", type="primary")
                    if submitted_new_emp:
                        if new_emp and new_user and new_pass:
                            if new_user not in employees_df["Username"].values:
                                if new_assigned in av_vehicles:
                                    new_row = {
                                        "Employee": new_emp,
                                        "Username": new_user,
                                        "Password": new_pass,
                                        "Assigned_Vehicle": new_assigned
                                    }
                                    employees_df = pd.concat([employees_df, pd.DataFrame([new_row])], ignore_index=True)
                                    employees_df.to_csv(EMPLOYEES_FILE, index=False)
                                    st.success(f"Added {new_emp}")
                                    st.rerun()
                                else:
                                    # already assigned
                                    vehicle_name = new_assigned.split(" (Assigned to")[0]
                                    current_emp = employees_df[employees_df["Assigned_Vehicle"] == vehicle_name]["Employee"].iloc[0]
                                    st.warning(f"{vehicle_name} is already assigned to {current_emp}. Reassign to {new_emp}?")
                                    if st.button("Yes, Reassign", key="reassign_vehicle_add"):
                                        employees_df.loc[employees_df["Assigned_Vehicle"] == vehicle_name, "Assigned_Vehicle"] = ""
                                        new_row = {
                                            "Employee": new_emp,
                                            "Username": new_user,
                                            "Password": new_pass,
                                            "Assigned_Vehicle": vehicle_name
                                        }
                                        employees_df = pd.concat([employees_df, pd.DataFrame([new_row])], ignore_index=True)
                                        employees_df.to_csv(EMPLOYEES_FILE, index=False)
                                        st.success(f"Added {new_emp} and reassigned {vehicle_name}")
                                        st.rerun()
                            else:
                                st.error("Username already exists.")
                        else:
                            st.error("All fields are required.")

                # Edit / Delete employees
                for idx, row in employees_df.iterrows():
                    with st.expander(f"Manage {row['Employee']}"):
                        col1, col2 = st.columns([2,1])
                        with col1:
                            with st.form(key=f"edit_employee_{idx}"):
                                edit_name = st.text_input("Employee Name", value=row["Employee"], key=f"edit_name_{idx}")
                                edit_user = st.text_input("Username", value=row["Username"], key=f"edit_user_{idx}")
                                edit_pass = st.text_input("Password", value=row["Password"], type="password", key=f"edit_pass_{idx}")

                                av_vehicles = [""] + [v for v in vehicles_df["Vehicle"] if v not in employees_df[employees_df["Employee"] != row["Employee"]]["Assigned_Vehicle"].values]
                                as_vehicles = [
                                    f"{v} (Assigned to {employees_df[employees_df['Assigned_Vehicle'] == v]['Employee'].iloc[0]})"
                                    for v in vehicles_df["Vehicle"] if v not in av_vehicles and v != ""
                                ]
                                vehicle_opts = av_vehicles + as_vehicles
                                current_vehicle = row["Assigned_Vehicle"]
                                if current_vehicle in vehicle_opts:
                                    start_index = vehicle_opts.index(current_vehicle)
                                else:
                                    start_index = 0
                                edit_vehicle = st.selectbox("Assigned Vehicle", vehicle_opts, index=start_index)

                                if st.form_submit_button("Edit Employee", type="secondary"):
                                    if edit_name and edit_user and edit_pass:
                                        # check username collision
                                        if edit_user == row["Username"] or edit_user not in employees_df["Username"].values:
                                            # if new vehicle is available
                                            if edit_vehicle in av_vehicles:
                                                employees_df.at[idx, "Employee"] = edit_name
                                                employees_df.at[idx, "Username"] = edit_user
                                                employees_df.at[idx, "Password"] = edit_pass
                                                employees_df.at[idx, "Assigned_Vehicle"] = edit_vehicle
                                                employees_df.to_csv(EMPLOYEES_FILE, index=False)

                                                # update submissions & mileage
                                                df = load_data(DATA_FILE)
                                                df["Employee"] = df["Employee"].replace(row["Employee"], edit_name)
                                                df.to_csv(DATA_FILE, index=False)

                                                mileage_df = load_data(MILEAGE_FILE)
                                                mileage_df["Employee"] = mileage_df["Employee"].replace(row["Employee"], edit_name)
                                                mileage_df.to_csv(MILEAGE_FILE, index=False)

                                                st.success(f"Updated {edit_name}")
                                                st.rerun()
                                            else:
                                                vehicle_name = edit_vehicle.split(" (Assigned to")[0]
                                                current_emp = employees_df[employees_df["Assigned_Vehicle"] == vehicle_name]["Employee"].iloc[0]
                                                st.warning(f"{vehicle_name} is already assigned to {current_emp}. Reassign to {edit_name}?")
                                                if st.button("Yes, Reassign", key=f"reassign_vehicle_{idx}"):
                                                    employees_df.loc[employees_df["Assigned_Vehicle"] == vehicle_name, "Assigned_Vehicle"] = ""
                                                    employees_df.at[idx, "Employee"] = edit_name
                                                    employees_df.at[idx, "Username"] = edit_user
                                                    employees_df.at[idx, "Password"] = edit_pass
                                                    employees_df.at[idx, "Assigned_Vehicle"] = vehicle_name
                                                    employees_df.to_csv(EMPLOYEES_FILE, index=False)

                                                    df = load_data(DATA_FILE)
                                                    df["Employee"] = df["Employee"].replace(row["Employee"], edit_name)
                                                    df.to_csv(DATA_FILE, index=False)

                                                    mileage_df = load_data(MILEAGE_FILE)
                                                    mileage_df["Employee"] = mileage_df["Employee"].replace(row["Employee"], edit_name)
                                                    mileage_df.to_csv(MILEAGE_FILE, index=False)

                                                    st.success(f"Updated {edit_name} and reassigned {vehicle_name}")
                                                    st.rerun()
                                        else:
                                            st.error("Username already exists.")
                                    else:
                                        st.error("All fields are required.")

                        with col2:
                            # Delete employee
                            if st.button("Delete Employee", key=f"delete_emp_{idx}", type="secondary"):
                                if st.checkbox("Confirm Deletion", key=f"confirm_emp_{idx}"):
                                    emp_name = row["Employee"]
                                    employees_df = employees_df.drop(idx)
                                    employees_df.to_csv(EMPLOYEES_FILE, index=False)

                                    # remove from submissions & mileage
                                    df = load_data(DATA_FILE)
                                    df = df[df["Employee"] != emp_name]
                                    df.to_csv(DATA_FILE, index=False)

                                    mileage_df = load_data(MILEAGE_FILE)
                                    mileage_df = mileage_df[mileage_df["Employee"] != emp_name]
                                    mileage_df.to_csv(MILEAGE_FILE, index=False)

                                    st.success(f"Deleted {emp_name}")
                                    st.rerun()
