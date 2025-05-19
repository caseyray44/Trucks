import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime, timedelta

# Files to store data
DATA_FILE = "data/submissions.csv"
MILEAGE_FILE = "data/mileage_log.csv"
VEHICLES_FILE = "data/vehicles.csv"
EMPLOYEES_FILE = "data/employees.csv"

# Helper to load CSVs
def load_data(path):
    return pd.read_csv(path)

# Ensure data directory and CSVs exist
os.makedirs("data", exist_ok=True)

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "submission_id","Employee","Vehicle","Date",
        "Tire_FL_PSI","Tire_FR_PSI","Tire_RL_PSI","Tire_RR_PSI","Tire_Comments",
        "Headlights_OK","Taillights_OK","Brake_Lights_OK","Turn_Signals_OK","Lights_Comments",
        "Exterior_Washed","Interior_Cleaned","Cleaning_Comments",
        "Mileage","Mileage_Comments",
        "Wipers_OK","Wipers_Comments",
        "Oil_Level_OK","Coolant_Level_OK","Brake_Fluid_OK","Fluids_Comments",
        "Oil_Photo",
        "Brakes_OK","Brakes_Comments",
        "Photos","Notes"
    ]).to_csv(DATA_FILE, index=False)

if not os.path.exists(MILEAGE_FILE):
    pd.DataFrame(columns=["submission_id","Employee","Vehicle","Date","Mileage","Mileage_Comments"]).to_csv(MILEAGE_FILE, index=False)

if not os.path.exists(VEHICLES_FILE):
    pd.DataFrame({"Vehicle": ["Jeep","Karma","Big Red","Muffin","Loud Truck","2018"]}).to_csv(VEHICLES_FILE, index=False)

if not os.path.exists(EMPLOYEES_FILE):
    pd.DataFrame({
        "Employee": ["Cody","Mason","Casey","Kasey","Colby","Jack"],
        "Username": ["cody123","mason123","casey123","kasey123","colby123","jack123"],
        "Password": ["pass123"]*6,
        "Assigned_Vehicle": ["Jeep","Karma","Big Red","Muffin","Loud Truck","2018"]
    }).to_csv(EMPLOYEES_FILE, index=False)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = ""
    st.session_state.employee_id = ""
    st.session_state.username = ""

st.title("Truck Checks App")

# -------------------------
# LOGIN
# -------------------------
if not st.session_state.logged_in:
    st.subheader("Login")
    with st.form("login_form"):
        user_type = st.selectbox("User Type", ["","Employee","Admin"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if user_type == "":
                st.error("Please select a User Type")
            elif user_type == "Admin" and username == "admin" and password == "admin123":
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

# -------------------------
# LOGOUT
# -------------------------
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = ""
    st.session_state.employee_id = ""
    st.session_state.username = ""
    st.experimental_rerun()

# -------------------------
# EMPLOYEE VIEW
# -------------------------
if st.session_state.user_type == "employee":
    df_emp = load_data(EMPLOYEES_FILE)
    emp_row = df_emp[df_emp.Employee == st.session_state.employee_id].iloc[0]
    vehicle = emp_row.Assigned_Vehicle
    st.subheader(f"Welcome, {emp_row.Employee}!")
    st.subheader(f"Vehicle: {vehicle}")
    st.markdown("**Instructions**: Check all items, upload photos if needed, then Submit.")

    # Date
    check_date = st.date_input("Check Date", value=datetime.now())
    date_str = check_date.strftime("%Y-%m-%d")

    # Tires
    st.subheader("Tires")
    tire_fl = st.number_input("Front Left Tire PSI", 0, 100, 30)
    tire_fr = st.number_input("Front Right Tire PSI", 0, 100, 30)
    tire_rl = st.number_input("Rear Left Tire PSI", 0, 100, 30)
    tire_rr = st.number_input("Rear Right Tire PSI", 0, 100, 30)
    tire_comments = st.text_area("Tire Comments")

    # Lights
    st.subheader("Lights")
    headlights = st.checkbox("Headlights OK")
    taillights = st.checkbox("Taillights OK")
    brakes_lights = st.checkbox("Brake Lights OK")
    signals = st.checkbox("Turn Signals OK")
    lights_comments = st.text_area("Lights Comments")

    # Cleaning
    st.subheader("Cleaning")
    exterior = st.checkbox("Exterior Washed")
    interior = st.checkbox("Interior Cleaned")
    clean_comments = st.text_area("Cleaning Comments")

    # Mileage
    st.subheader("Mileage")
    mileage = st.number_input("Current Mileage", 0)
    mile_comments = st.text_area("Mileage Comments")

    # Wipers
    st.subheader("Wipers")
    wipers = st.checkbox("Wipers OK")
    wipers_comments = st.text_area("Wipers Comments")

    # Fluids
    st.subheader("Fluids")
    oil_ok = st.checkbox("Oil Level OK")
    coolant_ok = st.checkbox("Coolant Level OK")
    brake_fluid_ok = st.checkbox("Brake Fluid OK")
    fluid_comments = st.text_area("Fluids Comments")
    oil_photo = st.file_uploader("Upload Oil Photo (Required)", type=["jpg","png"])
    if not oil_photo:
        st.warning("Oil photo required before Submit.")

    # Brakes
    st.subheader("Brakes")
    brakes_ok = st.checkbox("Brakes OK")
    brakes_comments = st.text_area("Brakes Comments")

    # Photos & Notes
    photos = st.file_uploader("Upload Additional Photos (Optional)", accept_multiple_files=True, type=["jpg","png"])
    notes = st.text_area("Notes")

    if st.button("Submit Check"):
        if not oil_photo:
            st.error("Oil photo is required!")
        else:
            os.makedirs("uploads/oil_photos", exist_ok=True)
            photo_path = f"uploads/oil_photos/{oil_photo.name}"
            with open(photo_path, "wb") as f:
                f.write(oil_photo.getbuffer())
            # Save additional
            paths = []
            if photos:
                os.makedirs("uploads/photos", exist_ok=True)
                for p in photos:
                    pth = f"uploads/photos/{p.name}"
                    with open(pth, "wb") as f:
                        f.write(p.getbuffer())
                    paths.append(pth)
            # Write submission
            sid = str(uuid.uuid4())
            df = load_data(DATA_FILE)
            entry = {
                "submission_id": sid,
                "Employee": emp_row.Employee,
                "Vehicle": vehicle,
                "Date": date_str,
                "Tire_FL_PSI": tire_fl,
                "Tire_FR_PSI": tire_fr,
                "Tire_RL_PSI": tire_rl,
                "Tire_RR_PSI": tire_rr,
                "Tire_Comments": tire_comments,
                "Headlights_OK": headlights,
                "Taillights_OK": taillights,
                "Brake_Lights_OK": brakes_lights,
                "Turn_Signals_OK": signals,
                "Lights_Comments": lights_comments,
                "Exterior_Washed": exterior,
                "Interior_Cleaned": interior,
                "Cleaning_Comments": clean_comments,
                "Mileage": mileage,
                "Mileage_Comments": mile_comments,
                "Wipers_OK": wipers,
                "Wipers_Comments": wipers_comments,
                "Oil_Level_OK": oil_ok,
                "Coolant_Level_OK": coolant_ok,
                "Brake_Fluid_OK": brake_fluid_ok,
                "Fluids_Comments": fluid_comments,
                "Oil_Photo": photo_path,
                "Brakes_OK": brakes_ok,
                "Brakes_Comments": brakes_comments,
                "Photos": ",".join(paths) if paths else "None",
                "Notes": notes
            }
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
            df["Date"] = pd.to_datetime(df["Date"])
            df = df[df["Date"] >= datetime.now() - timedelta(days=60)]
            df.to_csv(DATA_FILE, index=False)
            # Mileage log
            mdf = load_data(MILEAGE_FILE)
            mentry = {"submission_id": sid, "Employee": emp_row.Employee, "Vehicle": vehicle, "Date": date_str, "Mileage": mileage, "Mileage_Comments": mile_comments}
            mdf = pd.concat([mdf, pd.DataFrame([mentry])], ignore_index=True)
            mdf["Date"] = pd.to_datetime(mdf["Date"])
            mdf = mdf[mdf["Date"] >= datetime.now() - timedelta(days=365)]
            mdf.to_csv(MILEAGE_FILE, index=False)
            st.success("Submitted!")
    st.stop()

# -------------------------
# ADMIN VIEW
# -------------------------
else:
    st.subheader("Admin Dashboard")
    tabs = st.tabs([
        "Trucks",
        "Employees",
        "Manage Data"
    ])

    # Trucks
    with tabs[0]:
        st.subheader("Truck Overview")
        vdf = load_data(VEHICLES_FILE)
        sel = st.selectbox("Select Vehicle", vdf["Vehicle"])
        # Mileage chart
        kval = load_data(MILEAGE_FILE)
        kval["Date"] = pd.to_datetime(kval["Date"])
        subset = kval[kval["Vehicle"] == sel]
        if not subset.empty:
            st.line_chart(subset.set_index("Date")["Mileage"])
            st.dataframe(subset[["Date","Employee","Mileage","Mileage_Comments"]])
        else:
            st.write("No mileage data.")
        # Recent notes
        sdf = load_data(DATA_FILE)
        sdf["Date"] = pd.to_datetime(sdf["Date"])
        ssub = sdf[sdf["Vehicle"] == sel].sort_values("Date", ascending=False)
        st.write("Recent Notes (2 months)")
        for _, r in ssub.iterrows():
            if pd.notna(r["Notes"]) and r["Date"] >= datetime.now() - timedelta(days=60):
                st.write(f"{r['Date'].date()} - {r['Employee']} - {r['Notes']}")
        # Recent subs
        st.write("Recent Submissions (5)")
        for _, r in ssub.head(5).iterrows():
            with st.expander(f"{r['Employee']} - {r['Date'].date()}"):
                st.write(r.to_dict())
                if st.button("Delete", key=r['submission_id']):
                    dfall = load_data(DATA_FILE)
                    dfall = dfall[dfall['submission_id'] != r['submission_id']]
                    dfall.to_csv(DATA_FILE, index=False)
                    mm = load_data(MILEAGE_FILE)
                    mm = mm[mm['submission_id'] != r['submission_id']]
                    mm.to_csv(MILEAGE_FILE, index=False)
                    st.experimental_rerun()

    # Employees Check-Ins
    with tabs[1]:
        st.subheader("Employee Check-Ins")
        dfc = load_data(DATA_FILE)
        dfc["Date"] = pd.to_datetime(dfc["Date"])
        dfc["Week Start"] = dfc["Date"].dt.to_period("W").apply(lambda p: p.start_time)
        current_ws = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=datetime.now().weekday())
        weeks = sorted(dfc["Week Start"].unique(), reverse=True)
        sel_w = st.selectbox("Select Week", weeks, index=weeks.index(current_ws) if current_ws in weeks else 0, format_func=lambda d: d.date())
        wdf = dfc[(dfc["Date"] >= sel_w) & (dfc["Date"] < sel_w + timedelta(days=7))]
        edf = load_data(EMPLOYEES_FILE)
        rows = []
        for _, e in edf.iterrows():
            sub = wdf[wdf['Employee'] == e['Employee']]
            status = "Submitted" if not sub.empty else "Not Submitted"
            date_sub = sub.iloc[0]['Date'].date() if not sub.empty else "N/A"
            rows.append({"Employee": e['Employee'], "Vehicle": e['Assigned_Vehicle'], "Status": status, "Date": date_sub})
        st.dataframe(pd.DataFrame(rows))

    # Manage Data
    with tabs[2]:
        st.subheader("Manage Data")
        # Vehicles
        vdf = load_data(VEHICLES_FILE)
        st.write("Vehicles")
        st.dataframe(vdf)
        with st.form("add_vehicle"): 
            nv = st.text_input("New Vehicle")
            if st.form_submit_button("Add Vehicle"):
                if nv and nv not in vdf['Vehicle'].values:
                    vdf = pd.concat([vdf, pd.DataFrame({'Vehicle':[nv]})], ignore_index=True)
                    vdf.to_csv(VEHICLES_FILE, index=False)
                    st.experimental_rerun()
                else:
                    st.error("Invalid or duplicate")
        # Edit/Delete
        for idx, row in vdf.iterrows():
            with st.expander(f"Edit/Delete {row['Vehicle']}"):
                c1, c2 = st.columns([2,1])
                with c1:
                    with st.form(f"edit_v_{idx}"):
                        nn = st.text_input("New Name", row['Vehicle'], key=f"nv_{idx}")
                        if st.form_submit_button("Save"):
                            if nn and nn not in vdf['Vehicle'].values:
                                old = row['Vehicle']
                                vdf.at[idx,'Vehicle'] = nn
                                vdf.to_csv(VEHICLES_FILE, index=False)
                                pdf = load_data(EMPLOYEES_FILE)
                                pdf['Assigned_Vehicle'] = pdf['Assigned_Vehicle'].replace(old, nn)
                                pdf.to_csv(EMPLOYEES_FILE, index=False)
                                sd = load_data(DATA_FILE)
                                sd['Vehicle'] = sd['Vehicle'].replace(old, nn)
                                sd.to_csv(DATA_FILE, index=False)
                                ml = load_data(MILEAGE_FILE)
                                ml['Vehicle'] = ml['Vehicle'].replace(old, nn)
                                ml.to_csv(MILEAGE_FILE, index=False)
                                st.experimental_rerun()
                            else:
                                st.error("Invalid or exists")
                with c2:
                    if st.button("Delete", key=f"dv_{idx}"):
                        vdf = vdf.drop(idx)
                        vdf.to_csv(VEHICLES_FILE, index=False)
                        pdf = load_data(EMPLOYEES_FILE)
                        pdf['Assigned_Vehicle'] = pdf['Assigned_Vehicle'].replace(row['Vehicle'], '')
                        pdf.to_csv(EMPLOYEES_FILE, index=False)
                        sd = load_data(DATA_FILE)
                        sd = sd[sd['Vehicle'] != row['Vehicle']]
                        sd.to_csv(DATA_FILE, index=False)
                        ml = load_data(MILEAGE_FILE)
                        ml = ml[ml['Vehicle'] != row['Vehicle']]
                        ml.to_csv(MILEAGE_FILE, index=False)
                        st.experimental_rererun()

        # Employees
        edf = load_data(EMPLOYEES_FILE)
        st.write("Employees")
        st.dataframe(edf)
        with st.form("add_emp"):
            nn = st.text_input("Name")
            un = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            av = [''] + [v for v in load_data(VEHICLES_FILE)['Vehicle'] if v not in edf['Assigned_Vehicle'].values]
            selv = st.selectbox("Vehicle", av)
            if st.form_submit_button("Add Employee"):
                if nn and un and pw and un not in edf['Username'].values:
                    new = {'Employee':nn,'Username':un,'Password':pw,'Assigned_Vehicle':selv}
                    edf = pd.concat([edf,pd.DataFrame([new])], ignore_index=True)
                    edf.to_csv(EMPLOYEES_FILE, index=False)
                    st.experimental_rerun()
                else:
                    st.error("Invalid or duplicate")
        for idx,row in edf.iterrows():
            with st.expander(f"Edit/Delete {row['Employee']}"):
                c1,c2=st.columns([2,1])
                with c1:
                    with st.form(f"edit_emp_{idx}"):
                        name=st.text_input("Name",row['Employee'],key=f'nn_{idx}')
                        usr=st.text_input("Username",row['Username'],key=f'us_{idx}')
                        pwd=st.text_input("Password",row['Password'],type="password",key=f'pw_{idx}')
                        av2=['']+[v for v in load_data(VEHICLES_FILE)['Vehicle'] if v not in edf[edf['Employee']!=row['Employee']]['Assigned_Vehicle'].values]
                        sv=st.selectbox("Vehicle",av2,index=av2.index(row['Assigned_Vehicle']) if row['Assigned_Vehicle'] in av2 else 0,key=f'sv_{idx}')
                        if st.form_submit_button("Save"):
                            if name and usr and pwd and (usr==row['Username'] or usr not in edf['Username'].values):
                                old= row['Employee']
                                edf.at[idx,'Employee']=name
                                edf.at[idx,'Username']=usr
                                edf.at[idx,'Password']=pwd
                                edf.at[idx,'Assigned_Vehicle']=sv
                                edf.to_csv(EMPLOYEES_FILE,index=False)
                                sd=load_data(DATA_FILE)
                                sd['Employee']=sd['Employee'].replace(old,name)
                                sd.to_csv(DATA_FILE,index=False)
                                ml=load_data(MILEAGE_FILE)
                                ml['Employee']=ml['Employee'].replace(old,name)
                                ml.to_csv(MILEAGE_FILE,index=False)
                                st.experimental_rerun()
                            else:
                                st.error("Invalid or duplicate")
                with c2:
                    if st.button("Delete",key=f'de_{idx}'):
                        edf=edf.drop(idx)
                        edf.to_csv(EMPLOYEES_FILE,index=False)
                        sd=load_data(DATA_FILE)
                        sd=sd[sd['Employee']!=row['Employee']]
                        sd.to_csv(DATA_FILE,index=False)
                        ml=load_data(MILEAGE_FILE)
                        ml=ml[ml['Employee']!=row['Employee']]
                        ml.to_csv(MILEAGE_FILE,index=False)
                        st.experimental_rerun()
