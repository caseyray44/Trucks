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
ios.makedirs("data", exist_ok=True)
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
    pd.DataFrame({"Vehicle":["Jeep","Karma","Big Red","Muffin","Loud Truck","2018"]}).to_csv(VEHICLES_FILE,index=False)
if not os.path.exists(EMPLOYEES_FILE):
    pd.DataFrame({
        "Employee":["Cody","Mason","Casey","Kasey","Colby","Jack"],
        "Username":["cody123","mason123","casey123","kasey123","colby123","jack123"],
        "Password":["pass123"]*6,
        "Assigned_Vehicle":["Jeep","Karma","Big Red","Muffin","Loud Truck","2018"]
    }).to_csv(EMPLOYEES_FILE,index=False)

# Initialize session
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False
    st.session_state.user_type=""
    st.session_state.employee_id=""
    st.session_state.username=""

st.title("Truck Checks App")

# ---------------
# LOGIN
# ---------------
if not st.session_state.logged_in:
    st.subheader("Login")
    with st.form("login_form"):
        user_type = st.selectbox("User Type",["","Employee","Admin"],index=0)
        username  = st.text_input("Username")
        password  = st.text_input("Password",type="password")
        if st.form_submit_button("Login"):
            if not user_type:
                st.error("Please select a User Type")
            elif user_type=="Admin" and username=="admin" and password=="admin123":
                st.session_state.logged_in=True
                st.session_state.user_type="admin"
                st.session_state.employee_id="admin"
                st.session_state.username=username
                st.rerun()
            elif user_type=="Employee":
                df_emp=load_data(EMPLOYEES_FILE)
                match=df_emp[(df_emp.Username==username)&(df_emp.Password==password)]
                if not match.empty:
                    st.session_state.logged_in=True
                    st.session_state.user_type="employee"
                    st.session_state.employee_id=match.iloc[0]["Employee"]
                    st.session_state.username=username
                    st.rerun()
                else:
                    st.error("Wrong username or password")
            else:
                st.error("Wrong username or password")
    st.stop()

# ---------------
# LOGOUT
# ---------------
if st.button("Logout"):
    st.session_state.logged_in=False
    st.session_state.user_type=""
    st.session_state.employee_id=""
    st.session_state.username=""
    st.rerun()

# ---------------
# EMPLOYEE VIEW
# ---------------
if st.session_state.user_type=="employee":
    df_emp = load_data(EMPLOYEES_FILE)
    emp_row = df_emp[df_emp.Employee==st.session_state.employee_id].iloc[0]
    vehicle = emp_row.Assigned_Vehicle
    st.subheader(f"Welcome, {emp_row.Employee}!")
    st.subheader(f"Vehicle: {vehicle}")
    st.markdown("**Instructions**: Complete the check and submit.")

    # Date
    check_date = st.date_input("Check Date",value=datetime.now())
    date_str = check_date.strftime("%Y-%m-%d")

    # Tires
    st.subheader("Tires")
    tire_fl = st.number_input("Front Left Tire PSI",0,100,30)
    tire_fr = st.number_input("Front Right Tire PSI",0,100,30)
    tire_rl = st.number_input("Rear Left Tire PSI",0,100,30)
    tire_rr = st.number_input("Rear Right Tire PSI",0,100,30)
    tire_comments=st.text_area("Tire Comments")
    # Lights
    st.subheader("Lights")
    headlights=st.checkbox("Headlights OK")
    taillights=st.checkbox("Taillights OK")
    brake_lights=st.checkbox("Brake Lights OK")
    signals=st.checkbox("Turn Signals OK")
    light_comments=st.text_area("Lights Comments")
    # Cleaning
    st.subheader("Cleaning")
    ext=st.checkbox("Exterior Washed")
    intc=st.checkbox("Interior Cleaned")
    clean_comments=st.text_area("Cleaning Comments")
    # Mileage
    st.subheader("Mileage")
    miles=st.number_input("Current Mileage",0)
    mile_comments=st.text_area("Mileage Comments")
    # Wipers
    st.subheader("Wipers")
    wipers=st.checkbox("Wipers OK")
    wipers_comments=st.text_area("Wipers Comments")
    # Fluids
    st.subheader("Fluids")
    oil_ok=st.checkbox("Oil Level OK")
    coolant_ok=st.checkbox("Coolant Level OK")
    brake_fl_ok=st.checkbox("Brake Fluid OK")
    fluid_comments=st.text_area("Fluids Comments")
    oil_photo=st.file_uploader("Upload Oil Photo (jpg/png)",type=["jpg","png"])
    # Brakes
    st.subheader("Brakes")
    brakes_ok=st.checkbox("Brakes OK")
    brakes_comments=st.text_area("Brakes Comments")
    # Photos & Notes
    photos=st.file_uploader("Additional Photos",accept_multiple_files=True,type=["jpg","png"])
    notes=st.text_area("Notes")

    if st.button("Submit Check"):
        if not oil_photo:
            st.error("Oil photo required!")
        else:
            # Save files
            os.makedirs("uploads/oil_photos",exist_ok=True)
            oil_path=f"uploads/oil_photos/{oil_photo.name}"
            with open(oil_path,"wb") as f: f.write(oil_photo.getbuffer())
            photo_paths=[]
            if photos:
                os.makedirs("uploads/photos",exist_ok=True)
                for p in photos:
                    pth=f"uploads/photos/{p.name}"; photo_paths.append(pth)
                    with open(pth,"wb") as f: f.write(p.getbuffer())
            # Append to CSV
            sid=str(uuid.uuid4())
            sdf=load_data(DATA_FILE)
            entry={
                "submission_id":sid,
                "Employee":emp_row.Employee,
                "Vehicle":vehicle,
                "Date":date_str,
                "Tire_FL_PSI":tire_fl,
                "Tire_FR_PSI":tire_fr,
                "Tire_RL_PSI":tire_rl,
                "Tire_RR_PSI":tire_rr,
                "Tire_Comments":tire_comments,
                "Headlights_OK":headlights,
                "Taillights_OK":taillights,
                "Brake_Lights_OK":brake_lights,
                "Turn_Signals_OK":signals,
                "Lights_Comments":light_comments,
                "Exterior_Washed":ext,
                "Interior_Cleaned":intc,
                "Cleaning_Comments":clean_comments,
                "Mileage":miles,
                "Mileage_Comments":mile_comments,
                "Wipers_OK":wipers,
                "Wipers_Comments":wipers_comments,
                "Oil_Level_OK":oil_ok,
                "Coolant_Level_OK":coolant_ok,
                "Brake_Fluid_OK":brake_fl_ok,
                "Fluids_Comments":fluid_comments,
                "Oil_Photo":oil_path,
                "Brakes_OK":brakes_ok,
                "Brakes_Comments":brakes_comments,
                "Photos":",".join(photo_paths) if photo_paths else "None",
                "Notes":notes
            }
            sdf=pd.concat([sdf,pd.DataFrame([entry])],ignore_index=True)
            sdf.to_csv(DATA_FILE,index=False)
            # Mileage log
            mdf=load_data(MILEAGE_FILE)
            mdf=pd.concat([mdf,pd.DataFrame([{"submission_id":sid,"Employee":emp_row.Employee,"Vehicle":vehicle,"Date":date_str,"Mileage":miles,"Mileage_Comments":mile_comments}])],ignore_index=True)
            mdf.to_csv(MILEAGE_FILE,index=False)
            st.success("Check submitted!")
    st.stop()

# ---------------
# ADMIN VIEW
# ---------------
else:
    st.subheader("Admin Dashboard")
    tabs=st.tabs([
        "🚛 Trucks",
        "👥 Employees",
        "⚙️ Manage Data"
    ])

    # Trucks
    with tabs[0]:
        st.subheader("Truck Overview")
        vdf=load_data(VEHICLES_FILE)
        sel=st.selectbox("Select Vehicle",vdf["Vehicle"])
        ml=load_data(MILEAGE_FILE); ml["Date"]=pd.to_datetime(ml["Date"])
        vm=ml[ml["Vehicle"]==sel]
        if not vm.empty:
            st.line_chart(vm.set_index("Date")["Mileage"])
            st.dataframe(vm[["Date","Employee","Mileage","Mileage_Comments"]])
        else:
            st.write("No mileage data.")
        sdf=load_data(DATA_FILE); sdf["Date"]=pd.to_datetime(sdf["Date"])
        vs=sdf[sdf["Vehicle"]==sel].sort_values("Date",ascending=False)
        st.write("Recent Notes (2 months)")
        for _,r in vs.iterrows():
            if pd.notna(r["Notes"]): st.write(f"{r['Date'].date()} - {r['Employee']} - {r['Notes']}")
        st.write("Recent Submissions (5)")
        for _,r in vs.head(5).iterrows():
            with st.expander(f"{r['Employee']} - {r['Date'].date()}"):
                st.write(r.to_dict())
                if st.button("Delete",key=r['submission_id']):
                    dfa=load_data(DATA_FILE)
                    dfa=dfa[dfa['submission_id']!=r['submission_id']]; dfa.to_csv(DATA_FILE,index=False)
                    mla=load_data(MILEAGE_FILE)
                    mla=mla[mla['submission_id']!=r['submission_id']]; mla.to_csv(MILEAGE_FILE,index=False)
                    st.experimental_rerun()

    # Employees Tab
    with tabs[1]:
        st.subheader("Employee Check-Ins")
        dfc=load_data(DATA_FILE); dfc["Date"]=pd.to_datetime(dfc["Date"])
        dfc["Week Start"]=dfc["Date"].dt.to_period("W").apply(lambda p:p.start_time)
        ws=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)-timedelta(days=datetime.now().weekday())
        weeks=sorted(dfc["Week Start"].unique(),reverse=True)
        sel_w=st.selectbox("Select Week",weeks,index=weeks.index(ws) if ws in weeks else 0,format_func=lambda d:d.date())
        wdf=dfc[(dfc["Date"]>=sel_w)&(dfc["Date"]<sel_w+timedelta(days=7))]
        edf=load_data(EMPLOYEES_FILE)
        rows=[]
        for _,e in edf.iterrows():
            sub=wdf[wdf['Employee']==e['Employee']]
            status="Submitted" if not sub.empty else "Not Submitted"
            ds=sub.iloc[0]['Date'].date() if not sub.empty else "N/A"
            rows.append({"Employee":e['Employee'],"Vehicle":e['Assigned_Vehicle'],"Status":status,"Date":ds})
        st.dataframe(pd.DataFrame(rows))

    # Manage Data Tab
    with tabs[2]:
        st.subheader("Manage Data")
        # Vehicles
        vdf=load_data(VEHICLES_FILE)
        st.write("Vehicles")
        st.dataframe(vdf)
        with st.form("add_vehicle"): nv=st.text_input("New Vehicle")
            if st.form_submit_button("Add Vehicle") and nv and nv not in vdf['Vehicle'].values:
                vdf=pd.concat([vdf,pd.DataFrame({'Vehicle':[nv]})],ignore_index=True);vdf.to_csv(VEHICLES_FILE,index=False);st.rerun()
        for idx,row in vdf.iterrows():
            with st.expander(f"Edit/Delete {row['Vehicle']}"):
                c1,c2=st.columns([2,1])
                with c1:
                    with st.form(f"edit_v_{idx}"):
                        nn=st.text_input("Name",row['Vehicle'],key=f'nn{idx}')
                        if st.form_submit_button("Save") and nn and nn not in vdf['Vehicle'].values:
                            old=row['Vehicle'];vdf.at[idx,'Vehicle']=nn;vdf.to_csv(VEHICLES_FILE,index=False)
                            edf=load_data(EMPLOYEES_FILE);edf['Assigned_Vehicle']=edf['Assigned_Vehicle'].replace(old,nn);edf.to_csv(EMPLOYEES_FILE,index=False)
                            sdf=load_data(DATA_FILE);sdf['Vehicle']=sdf['Vehicle'].replace(old,nn);sdf.to_csv(DATA_FILE,index=False)
                            mdf=load_data(MILEAGE_FILE);mdf['Vehicle']=mdf['Vehicle'].replace(old,nn);mdf.to_csv(MILEAGE_FILE,index=False)
                            st.rerun()
                with c2:
                    if st.button("Delete",key=f'dv{idx}'):
                        vdf=vdf.drop(idx);vdf.to_csv(VEHICLES_FILE,index=False)
                        edf=load_data(EMPLOYEES_FILE);edf['Assigned_Vehicle']=edf['Assigned_Vehicle'].replace(row['Vehicle'],"");edf.to_csv(EMPLOYEES_FILE,index=False)
                        sdf=load_data(DATA_FILE);sdf=sdf[sdf['Vehicle']!=row['Vehicle']];sdf.to_csv(DATA_FILE,index=False)
                        mdf=load_data(MILEAGE_FILE);mdf=mdf[mdf['Vehicle']!=row['Vehicle']];mdf.to_csv(MILEAGE_FILE,index=False)
                        st.rerun()
        # Employees
        edf=load_data(EMPLOYEES_FILE);st.write("Employees");st.dataframe(edf)
        with st.form("add_emp"): n=st.text_input("Name");u=st.text_input("Username");p=st.text_input("Password",type="password")
            av=['']+[v for v in load_data(VEHICLES_FILE)['Vehicle'] if v not in edf['Assigned_Vehicle'].values]
            sel=st.selectbox("Vehicle",av)
            if st.form_submit_button("Add Employee") and n and u and p and u not in edf['Username'].values:
                edf=pd.concat([edf,pd.DataFrame([{'Employee':n,'Username':u,'Password':p,'Assigned_Vehicle':sel}])],ignore_index=True);edf.to_csv(EMPLOYEES_FILE,index=False);st.rerun()
        for idx,row in edf.iterrows():
            with st.expander(f"Edit/Delete {row['Employee']}"):
                c1,c2=st.columns([2,1])
                with c1:
                    with st.form(f"edit_e_{idx}"):
                        nn=st.text_input("Name",row['Employee'],key=f'e{idx}')
                        uu=st.text_input("Username",row['Username'],key=f'u{idx}')
                        pp=st.text_input("Password",row['Password'],type="password",key=f'p{idx}')
                        av2=['']+[v for v in load_data(VEHICLES_FILE)['Vehicle'] if v not in edf[edf['Employee']!=row['Employee']]['Assigned_Vehicle'].values]
                        sel2=st.selectbox("Vehicle",av2,index=av2.index(row['Assigned_Vehicle']) if row['Assigned_Vehicle'] in av2 else 0)
                        if st.form_submit_button("Save") and nn and (uu==row['Username'] or uu not in edf['Username'].values):
                            old=row['Employee'];edf.at[idx,'Employee']=nn;edf.at[idx,'Username']=uu;edf.at[idx,'Password']=pp;edf.at[idx,'Assigned_Vehicle']=sel2;edf.to_csv(EMPLOYEES_FILE,index=False)
                            sdf=load_data(DATA_FILE);sdf['Employee']=sdf['Employee'].replace(old,nn);sdf.to_csv(DATA_FILE,index=False)
                            mdf=load_data(MILEAGE_FILE);mdf['Employee']=mdf['Employee'].replace(old,nn);mdf.to_csv(MILEAGE_FILE,index=False)
                            st.rerun()
                with c2:
                    if st.button("Delete",key=f'de{idx}'):
                        edf=edf.drop(idx);edf.to_csv(EMPLOYEES_FILE,index=False)
                        sdf=load_data(DATA_FILE);sdf=sdf[sdf['Employee']!=row['Employee']];sdf.to_csv(DATA_FILE,index=False)
                        mdf=load_data(MILEAGE_FILE);mdf=mdf[mdf['Employee']!=row['Employee']];mdf.to_csv(MILEAGE_FILE,index=False)
                        st.rerun()
