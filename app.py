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
    pd.DataFrame({"Vehicle":["Jeep","Karma","Big Red","Muffin","Loud Truck","2018"]}).to_csv(VEHICLES_FILE, index=False)

if not os.path.exists(EMPLOYEES_FILE):
    pd.DataFrame({
        "Employee":["Cody","Mason","Casey","Kasey","Colby","Jack"],
        "Username":["cody123","mason123","casey123","kasey123","colby123","jack123"],
        "Password":["pass123"]*6,
        "Assigned_Vehicle":["Jeep","Karma","Big Red","Muffin","Loud Truck","2018"]
    }).to_csv(EMPLOYEES_FILE, index=False)

# Helper to load CSVs
def load_data(path):
    return pd.read_csv(path)

# Initialize session state
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
        user_type = st.selectbox("User Type", ["Employee","Admin"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if user_type=="Admin" and username=="admin" and password=="admin123":
                st.session_state.logged_in=True
                st.session_state.user_type="admin"
                st.session_state.employee_id="admin"
                st.session_state.username=username
                st.experimental_rerun()
            elif user_type=="Employee":
                emp_df = load_data(EMPLOYEES_FILE)
                match = emp_df[(emp_df.Username==username)&(emp_df.Password==password)]
                if not match.empty:
                    st.session_state.logged_in=True
                    st.session_state.user_type="employee"
                    st.session_state.employee_id=match.iloc[0]["Employee"]
                    st.session_state.username=username
                    st.experimental_rerun()
                else:
                    st.error("Wrong username or password")
            else:
                st.error("Wrong username or password")
    st.stop()

# --- LOGOUT ---
if st.button("Logout"):
    st.session_state.logged_in=False
    st.session_state.user_type=""
    st.session_state.employee_id=""
    st.session_state.username=""
    st.experimental_rerun()

# --- EMPLOYEE VIEW ---
if st.session_state.user_type=="employee":
    emp_df = load_data(EMPLOYEES_FILE)
    emp_row = emp_df[emp_df["Employee"]==st.session_state.employee_id].iloc[0]
    assigned_vehicle = emp_row["Assigned_Vehicle"]
    st.subheader(f"Welcome, {emp_row['Employee']}! Vehicle: {assigned_vehicle}")
    st.markdown("**Instructions**: Check all items, upload photos if needed, and hit Submit—done!")
    # Date
    check_date = st.date_input("Check Date", value=datetime.now())
    date_str = check_date.strftime("%Y-%m-%d")
    # Tires
    tire_fl_psi = st.number_input("Front Left Tire Pressure (PSI)",0,100,30)
    tire_fr_psi = st.number_input("Front Right Tire Pressure (PSI)",0,100,30)
    tire_rl_psi = st.number_input("Rear Left Tire Pressure (PSI)",0,100,30)
    tire_rr_psi = st.number_input("Rear Right Tire Pressure (PSI)",0,100,30)
    tire_comments = st.text_area("Tire Comments")
    # Lights
    st.subheader("Lights")
    headlights_ok=st.checkbox("Headlights OK")
    taillights_ok=st.checkbox("Taillights OK")
    brake_lights_ok=st.checkbox("Brake Lights OK")
    turn_signals_ok=st.checkbox("Turn Signals OK")
    lights_comments=st.text_area("Lights Comments")
    # Cleaning
    st.subheader("Cleaning")
    exterior_washed=st.checkbox("Exterior Washed")
    interior_cleaned=st.checkbox("Interior Cleaned")
    cleaning_comments=st.text_area("Cleaning Comments")
    # Mileage
    st.subheader("Mileage")
    mileage=st.number_input("Current Mileage",0)
    mileage_comments=st.text_area("Mileage Comments")
    # Wipers
    st.subheader("Wipers")
    wipers_ok=st.checkbox("Windshield Wipers OK")
    wipers_comments=st.text_area("Wipers Comments")
    # Fluids
    st.subheader("Fluids")
    oil_level_ok=st.checkbox("Oil Level OK")
    coolant_level_ok=st.checkbox("Coolant Level OK")
    brake_fluid_ok=st.checkbox("Brake Fluid OK")
    fluids_comments=st.text_area("Fluids Comments")
    oil_photo=st.file_uploader("Upload Oil Level Photo (Required)",type=["jpg","png"])
    # Brakes
    st.subheader("Brakes")
    brakes_ok=st.checkbox("Brakes OK")
    brakes_comments=st.text_area("Brakes Comments")
    # Additional
    photos=st.file_uploader("Upload Additional Photos (Optional)",accept_multiple_files=True,type=["jpg","png"])
    notes=st.text_area("Notes")
    if st.button("Submit Check"):
        if not oil_photo:
            st.error("Oil level photo is required!")
        else:
            submission_id=str(uuid.uuid4())
            df=pd.read_csv(DATA_FILE)
            entry={
                "submission_id":submission_id,
                "Employee":emp_row['Employee'],"Vehicle":assigned_vehicle,"Date":date_str,
                "Tire_FL_PSI":tire_fl_psi,"Tire_FR_PSI":tire_fr_psi,
                "Tire_RL_PSI":tire_rl_psi,"Tire_RR_PSI":tire_rr_psi,
                "Tire_Comments":tire_comments,
                "Headlights_OK":headlights_ok,"Taillights_OK":taillights_ok,
                "Brake_Lights_OK":brake_lights_ok,"Turn_Signals_OK":turn_signals_ok,
                "Lights_Comments":lights_comments,
                "Exterior_Washed":exterior_washed,"Interior_Cleaned":interior_cleaned,
                "Cleaning_Comments":cleaning_comments,
                "Mileage":mileage,"Mileage_Comments":mileage_comments,
                "Wipers_OK":wipers_ok,"Wipers_Comments":wipers_comments,
                "Oil_Level_OK":oil_level_ok,"Coolant_Level_OK":coolant_level_ok,
                "Brake_Fluid_OK":brake_fluid_ok,"Fluids_Comments":fluids_comments,
                "Oil_Photo":"uploads/oil_photos/"+oil_photo.name,
                "Brakes_OK":brakes_ok,"Brakes_Comments":brakes_comments,
                "Photos":",".join(["uploads/photos/"+p.name for p in photos]) if photos else "None",
                "Notes":notes
            }
            os.makedirs("uploads/oil_photos",exist_ok=True)
            with open("uploads/oil_photos/"+oil_photo.name,"wb") as f: f.write(oil_photo.getbuffer())
            if photos:
                os.makedirs("uploads/photos",exist_ok=True)
                for p in photos:
                    with open("uploads/photos/"+p.name,"wb") as f: f.write(p.getbuffer())
            df=pd.concat([df,pd.DataFrame([entry])],ignore_index=True)
            df.Date=pd.to_datetime(df.Date)
            df=df[df.Date>=datetime.now()-timedelta(days=60)]
            df.to_csv(DATA_FILE,index=False)
            mdf=pd.read_csv(MILEAGE_FILE)
            mdf=pd.concat([mdf,pd.DataFrame([{
                "submission_id":submission_id,"Employee":emp_row['Employee'],
                "Vehicle":assigned_vehicle,"Date":date_str,
                "Mileage":mileage,"Mileage_Comments":mileage_comments
            }])],ignore_index=True)
            mdf.Date=pd.to_datetime(mdf.Date)
            mdf=mdf[mdf.Date>=datetime.now()-timedelta(days=365)]
            mdf.to_csv(MILEAGE_FILE,index=False)
            st.success("Check submitted! Thank you.")
    st.stop()

# --- ADMIN VIEW ---
st.subheader("Admin Dashboard")
tabs=st.tabs(["🚛 Trucks","👥 Employees","⚙️ Manage Data"])

# Trucks Tab
with tabs[0]:
    st.subheader("Truck Overview")
    vehicles_df=load_data(VEHICLES_FILE)
    selected=st.selectbox("Select Vehicle",vehicles_df["Vehicle"])
    with st.container():
        st.write("### Mileage History (1 Year)")
        mdf=load_data(MILEAGE_FILE)
        mdf.Date=pd.to_datetime(mdf.Date)
        vm=mdf[mdf.Vehicle==selected]
        if not vm.empty:
            st.line_chart(vm.set_index("Date")["Mileage"])
            st.dataframe(vm[["Date","Employee","Mileage","Mileage_Comments"]])
        else: st.write("No mileage data.")
    df_sub=pd.read_csv(DATA_FILE); df_sub.Date=pd.to_datetime(df_sub.Date)
    vs=df_sub[df_sub.Vehicle==selected].sort_values("Date",ascending=False)
    with st.container():
        st.write("### Recent Notes (2 Months)")
        cutoff=datetime.now()-timedelta(days=60)
        for _,r in vs[vs.Date>=cutoff].iterrows():
            if r.Notes: st.write(f"{r.Date.date()} - {r.Employee} - {r.Notes}")
    with st.container():
        st.write("### Recent Submissions (Last 5)")
        for _,r in vs.head(5).iterrows():
            with st.expander(f"{r.Employee} - {r.Date.date()}"):
                # display fields
                st.write(r.to_dict())
                if st.button("Delete",key=r.submission_id):
                    dfa=pd.read_csv(DATA_FILE); dfa=dfa[dfa.submission_id!=r.submission_id]; dfa.to_csv(DATA_FILE,index=False)
                    mfa=pd.read_csv(MILEAGE_FILE); mfa=mfa[mfa.submission_id!=r.submission_id]; mfa.to_csv(MILEAGE_FILE,index=False)
                    st.experimental_rerun()

# Employees Tab
with tabs[1]:
    st.subheader("Employee Check-Ins")
    df_sub=load_data(DATA_FILE); emp_df=load_data(EMPLOYEES_FILE)
    if not df_sub.empty:
        df_sub.Date=pd.to_datetime(df_sub.Date)
        df_sub["Week Start"]=df_sub.Date.dt.to_period("W").apply(lambda r:r.start_time)
        ws=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)-timedelta(days=datetime.now().weekday())
        weeks=sorted(df_sub["Week Start"].unique(),reverse=True)
        sel=st.selectbox("Select Week",weeks,index=weeks.index(ws) if ws in weeks else 0,format_func=lambda x:x.date())
        wdf=df_sub[(df_sub.Date>=sel)&(df_sub.Date<sel+timedelta(days=7))]
        rows=[]
        for _,e in emp_df.iterrows():
            sub=wdf[wdf.Employee==e.Employee]
            rows.append({"Employee":e.Employee,"Vehicle":e.Assigned_Vehicle,
                         "Status":"Submitted" if not sub.empty else "Not Submitted",
                         "Date":sub.iloc[0].Date.date() if not sub.empty else "N/A"})
        table=pd.DataFrame(rows)
        st.dataframe(table)
    else: st.write("No submissions yet.")

# Manage Data Tab
with tabs[2]:
    st.subheader("Manage Data")
    mtabs=st.tabs(["Manage Vehicles","Manage Employees"])
    with mtabs[0]:
        st.write("### Manage Vehicles")
        vdf=load_data(VEHICLES_FILE)
        st.dataframe(vdf)
        with st.form("add_vehicle"): new_v=st.text_input("New Vehicle Name");
            if st.form_submit_button("Add Vehicle"):
                if new_v and new_v not in vdf.Vehicle.values:
                    vdf=pd.concat([vdf,pd.DataFrame({"Vehicle":[new_v]})],ignore_index=True)
                    vdf.to_csv(VEHICLES_FILE,index=False); st.success(f"Added {new_v}"); st.experimental_rerun()
                else: st.error("Invalid or duplicate name")
        for idx,row in vdf.iterrows():
            with st.expander(f"Edit/Delete {row.Vehicle}"):
                col1,col2,col3=st.columns(3)
                with col1:
                    with st.form(f"edit_v_{idx}"):
                        nm=st.text_input("Name",value=row.Vehicle,key=f"e_v_{idx}")
                        if st.form_submit_button("Save"):
                            if nm and nm not in vdf.Vehicle.values:
                                old=row.Vehicle; vdf.at[idx,"Vehicle"]=nm; vdf.to_csv(VEHICLES_FILE,index=False)
                                edf=load_data(EMPLOYEES_FILE); edf.Assigned_Vehicle=edf.Assigned_Vehicle.replace(old,nm); edf.to_csv(EMPLOYEES_FILE,index=False)
                                sdf=load_data(DATA_FILE); sdf.Vehicle=sdf.Vehicle.replace(old,nm); sdf.to_csv(DATA_FILE,index=False)
                                mdf=load_data(MILEAGE_FILE); mdf.Vehicle=mdf.Vehicle.replace(old,nm); mdf.to_csv(MILEAGE_FILE,index=False)
                                st.success("Updated"); st.experimental_rerun()
                            else: st.error("Invalid or duplicate")
                with col2:
                    with st.form(f"assign_v_{idx}"):
                        edf=load_data(EMPLOYEES_FILE)
                        avail=[""]+[e for e in edf.Employee if e not in edf.Assigned_Vehicle.values]
                        sel=st.selectbox("Assign to",avail,key=f"a_v_{idx}")
                        if st.form_submit_button("Assign") and sel:
                            edf.loc[edf.Employee==sel,"Assigned_Vehicle"]=row.Vehicle; edf.to_csv(EMPLOYEES_FILE,index=False)
                            st.success("Assigned"); st.experimental_rerun()
                with col3:
                    if st.button("Delete",key=f"d_v_{idx}"):
                        vdf=vdf.drop(idx); vdf.to_csv(VEHICLES_FILE,index=False)
                        edf=load_data(EMPLOYEES_FILE); edf.Assigned_Vehicle=edf.Assigned_Vehicle.replace(row.Vehicle,""); edf.to_csv(EMPLOYEES_FILE,index=False)
                        sdf=load_data(DATA_FILE); sdf=sdf[sdf.Vehicle!=row.Vehicle]; sdf.to_csv(DATA_FILE,index=False)
                        mdf=load_data(MILEAGE_FILE); mdf=mdf[mdf.Vehicle!=row.Vehicle]; mdf.to_csv(MILEAGE_FILE,index=False)
                        st.success("Deleted"); st.experimental_rerun()
    with mtabs[1]:
        st.write("### Manage Employees")
        edf=load_data(EMPLOYEES_FILE)
        st.dataframe(edf)
        with st.form("add_emp"): 
            ne=st.text_input("Name"); un=st.text_input("Username"); pw=st.text_input("Password",type="password")
            vdf=load_data(VEHICLES_FILE); avail=[""]+[v for v in vdf.Vehicle if v not in edf.Assigned_Vehicle.values]
            av_sel=st.selectbox("Vehicle",avail)
            if st.form_submit_button("Add Employee"):
                if ne and un and pw and un not in edf.Username.values:
                    edf=pd.concat([edf,pd.DataFrame([{"Employee":ne,"Username":un,"Password":pw,"Assigned_Vehicle":av_sel}])],ignore_index=True)
                    edf.to_csv(EMPLOYEES_FILE,index=False); st.success("Added"); st.experimental_rerun()
                else: st.error("Invalid or duplicate")
        for idx,row in edf.iterrows():
            with st.expander(f"Edit/Delete {row.Employee}"):
                c1,c2=st.columns([2,1])
                with c1:
                    with st.form(f"edit_emp_{idx}"):
                        ne=st.text_input("Name",value=row.Employee,key=f"e_n_{idx}")
                        un=st.text_input("Username",value=row.Username,key=f"e_u_{idx}")
                        pw=st.text_input("Password",value=row.Password,type="password",key=f"e_p_{idx}")
                        avail=[""]+[v for v in load_data(VEHICLES_FILE).Vehicle if v not in edf[edf.Employee!=row.Employee].Assigned_Vehicle.values]
                        asv=st.selectbox("Vehicle",avail,index=avail.index(row.Assigned_Vehicle) if row.Assigned_Vehicle in avail else 0,key=f"e_v2_{idx}")
                        if st.form_submit_button("Save"):
                            if ne and un and pw and (un==row.Username or un not in edf.Username.values):
                                edf.at[idx,"Employee"]=ne; edf.at[idx,"Username"]=un; edf.at[idx,"Password"]=pw; edf.at[idx,"Assigned_Vehicle"]=asv
                                edf.to_csv(EMPLOYEES_FILE,index=False)
                                sdf=load_data(DATA_FILE); sdf.Employee=sdf.Employee.replace(row.Employee,ne); sdf.to_csv(DATA_FILE,index=False)
                                mdf=load_data(MILEAGE_FILE); mdf.Employee=mdf.Employee.replace(row.Employee,ne); mdf.to_csv(MILEAGE_FILE,index=False)
                                st.success("Updated"); st.experimental_rerun()
                            else: st.error("Invalid or duplicate")
                with c2:
                    if st.button("Delete",key=f"d_e_{idx}"):
                        edf=edf.drop(idx); edf.to_csv(EMPLOYEES_FILE,index=False)
                        sdf=load_data(DATA_FILE); sdf=sdf[sdf.Employee!=row.Employee]; sdf.to_csv(DATA_FILE,index=False)
                        mdf=load_data(MILEAGE_FILE); mdf=mdf[mdf.Employee!=row.Employee]; mdf.to_csv(MILEAGE_FILE,index=False)
                        st.success("Deleted"); st.experimental_rerun()
