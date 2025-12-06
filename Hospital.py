import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password",
            database="hospital",
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def execute(self, query, params=None):
        """Executes SELECT / INSERT / UPDATE / DELETE queries."""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        q = query.strip().lower()
        if q.startswith("insert") or q.startswith("update") or q.startswith("delete"):
            self.conn.commit()

        return self.cursor
class UserService:
    def __init__(self):
        self.db = Database()

    def authenticate(self, username, password):
        q = """
        SELECT * FROM users 
        WHERE username=%s AND password=%s
        """
        cur = self.db.execute(q, (username, password))
        return cur.fetchone()

class PatientService:
    def __init__(self):
        self.db = Database()

    def add(self, first, last, gender, dob, phone, city, reg_date):
        q = """
        INSERT INTO patients 
        (First_Name, Last_Name, Gender, Dob, Phone, City, Registration_Date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.db.execute(q, (first, last, gender, dob, phone, city, reg_date))

    def get_all(self):
        return self.db.execute("SELECT * FROM patients ORDER BY Patient_id DESC").fetchall()

    def get_by_id(self, pid):
        return self.db.execute("SELECT * FROM patients WHERE Patient_id=%s", (pid,)).fetchone()

    def update(self, pid, first, last, gender, dob, phone, city, reg_date):
        q = """
        UPDATE patients
        SET First_Name=%s, Last_Name=%s, Gender=%s, Dob=%s,
            Phone=%s, City=%s, Registration_Date=%s
        WHERE Patient_id=%s
        """
        self.db.execute(q, (first, last, gender, dob, phone, city, reg_date, pid))

    def delete(self, pid):
        self.db.execute("DELETE FROM patients WHERE Patient_id=%s", (pid,))

class DepartmentService:
    def __init__(self):
        self.db = Database()

    def add(self, name):
        q = "INSERT INTO Department (Department_name) VALUES (%s)"
        self.db.execute(q, (name,))

    def get_all(self):
        return self.db.execute("SELECT * FROM Department ORDER BY Department_id").fetchall()

    def get_by_id(self, did):
        return self.db.execute("SELECT * FROM Department WHERE Department_id=%s", (did,)).fetchone()

    def update(self, did, name):
        q = "UPDATE Department SET Department_name=%s WHERE Department_id=%s"
        self.db.execute(q, (name, did))

    def delete(self, did):
        self.db.execute("DELETE FROM Department WHERE Department_id=%s", (did,))

class DoctorService:
    def __init__(self):
        self.db = Database()

    def add(self, first, last, phone, spec, dept_id):
        q = """
        INSERT INTO Doctors 
        (First_Name, Last_Name, Phone, Specialization, Department_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.execute(q, (first, last, phone, spec, dept_id))

    def get_all(self):
        q = """
        SELECT d.*, dept.Department_name
        FROM Doctors d
        LEFT JOIN Department dept ON d.Department_id = dept.Department_id
        ORDER BY d.Doctor_id
        """
        return self.db.execute(q).fetchall()

    def get_by_id(self, did):
        return self.db.execute("SELECT * FROM Doctors WHERE Doctor_id=%s", (did,)).fetchone()

    def update(self, did, first, last, phone, spec, dept_id):
        q = """
        UPDATE Doctors
        SET First_Name=%s, Last_Name=%s, Phone=%s,
            Specialization=%s, Department_id=%s
        WHERE Doctor_id=%s
        """
        self.db.execute(q, (first, last, phone, spec, dept_id, did))

    def delete(self, did):
        self.db.execute("DELETE FROM Doctors WHERE Doctor_id=%s", (did,))

class AppointmentService:
    def __init__(self):
        self.db = Database()

    def add(self, pid, did, app_date, status):
        q = """
        INSERT INTO Appointments
        (Patient_id, Doctor_id, Appointment_Date, Appointment_status)
        VALUES (%s, %s, %s, %s)
        """
        self.db.execute(q, (pid, did, app_date, status))

    def get_all(self):
        q = """
        SELECT a.*, p.First_Name AS Patient_First, p.Last_Name AS Patient_Last,
               d.First_Name AS Doctor_First, d.Last_Name AS Doctor_Last
        FROM Appointments a
        JOIN Patients p ON a.Patient_id = p.Patient_id
        JOIN Doctors d ON a.Doctor_id = d.Doctor_id
        ORDER BY a.Appointment_Date DESC
        """
        return self.db.execute(q).fetchall()

    def get_by_id(self, aid):
        return self.db.execute("SELECT * FROM Appointments WHERE Appointment_id=%s", (aid,)).fetchone()

    def update(self, aid, pid, did, app_date, status):
        q = """
        UPDATE Appointments
        SET Patient_id=%s, Doctor_id=%s, Appointment_Date=%s, Appointment_status=%s
        WHERE Appointment_id=%s
        """
        self.db.execute(q, (pid, did, app_date, status, aid))

    def delete(self, aid):
        self.db.execute("DELETE FROM Appointments WHERE Appointment_id=%s", (aid,))

class VisitService:
    def __init__(self):
        self.db = Database()

    def add(self, pid, did, vdate, vtype, diagnosis, ddate):
        q = """
        INSERT INTO Visits 
        (Patient_id, Doctor_id, Visit_Date, Visit_Type, Diagnosis, Discharge_Date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.execute(q, (pid, did, vdate, vtype, diagnosis, ddate))

    def get_all(self):
        q = """
        SELECT v.*, p.First_Name AS Patient_First, p.Last_Name AS Patient_Last,
               d.First_Name AS Doctor_First, d.Last_Name AS Doctor_Last
        FROM Visits v
        JOIN Patients p ON v.Patient_id = p.Patient_id
        JOIN Doctors d ON v.Doctor_id = d.Doctor_id
        ORDER BY v.Visit_Date DESC
        """
        return self.db.execute(q).fetchall()

    def get_by_id(self, vid):
        return self.db.execute("SELECT * FROM Visits WHERE Visit_id=%s", (vid,)).fetchone()

    def update(self, vid, pid, did, vdate, vtype, diagnosis, ddate):
        q = """
        UPDATE Visits
        SET Patient_id=%s, Doctor_id=%s, Visit_Date=%s,
            Visit_Type=%s, Diagnosis=%s, Discharge_Date=%s
        WHERE Visit_id=%s
        """
        self.db.execute(q, (pid, did, vdate, vtype, diagnosis, ddate, vid))

    def delete(self, vid):
        self.db.execute("DELETE FROM Visits WHERE Visit_id=%s", (vid,))

class TreatmentService:
    def __init__(self):
        self.db = Database()

    def add(self, vid, name, category, cost):
        q = """
        INSERT INTO Treatment 
        (Visit_id, Treatment_Name, Treatment_Category, Treatment_Cost)
        VALUES (%s, %s, %s, %s)
        """
        self.db.execute(q, (vid, name, category, cost))

    def get_all(self):
        q = """
        SELECT t.*, v.Patient_id, v.Doctor_id
        FROM Treatment t
        JOIN Visits v ON t.Visit_id = v.Visit_id
        ORDER BY t.Treatment_id DESC
        """
        return self.db.execute(q).fetchall()

    def get_by_id(self, tid):
        return self.db.execute("SELECT * FROM Treatment WHERE Treatment_id=%s", (tid,)).fetchone()

    def update(self, tid, vid, name, category, cost):
        q = """
        UPDATE Treatment
        SET Visit_id=%s, Treatment_Name=%s, Treatment_Category=%s, Treatment_Cost=%s
        WHERE Treatment_id=%s
        """
        self.db.execute(q, (vid, name, category, cost, tid))

    def delete(self, tid):
        self.db.execute("DELETE FROM Treatment WHERE Treatment_id=%s", (tid,))

class BillingService:
    def __init__(self):
        self.db = Database()

    def add(self, vid, bill_date, total, method, status):
        q = """
        INSERT INTO Billing 
        (Visit_id, Bill_Date, Total_Amount, Payment_Method, Payment_Status)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.execute(q, (vid, bill_date, total, method, status))

    def get_all(self):
        q = """
        SELECT b.*, v.Patient_id, v.Doctor_id
        FROM Billing b
        JOIN Visits v ON b.Visit_id = v.Visit_id
        ORDER BY b.Bill_Date DESC
        """
        return self.db.execute(q).fetchall()

    def get_by_id(self, bid):
        return self.db.execute("SELECT * FROM Billing WHERE Bill_id=%s", (bid,)).fetchone()

    def update(self, bid, vid, bill_date, total, method, status):
        q = """
        UPDATE Billing
        SET Visit_id=%s, Bill_Date=%s, Total_Amount=%s,
            Payment_Method=%s, Payment_Status=%s
        WHERE Bill_id=%s
        """
        self.db.execute(q, (vid, bill_date, total, method, status, bid))

    def delete(self, bid):
        self.db.execute("DELETE FROM Billing WHERE Bill_id=%s", (bid,))

class AnalyticsService:
    def __init__(self):
        self.db = Database()

    def counts(self):
        q = """
        SELECT 
            (SELECT COUNT(*) FROM patients) AS patients,
            (SELECT COUNT(*) FROM doctors) AS doctors,
            (SELECT COUNT(*) FROM department) AS departments,
            (SELECT COUNT(*) FROM appointments) AS appointments,
            (SELECT COUNT(*) FROM visits) AS visits,
            (SELECT COUNT(*) FROM treatment) AS treatments,
            (SELECT COUNT(*) FROM billing) AS billing
        """
        return self.db.execute(q).fetchone()

    def yearly_patients(self):
        q = """
        SELECT YEAR(registration_date) AS year, COUNT(*) AS total_patients
        FROM patients
        GROUP BY YEAR(registration_date)
        ORDER BY year;
        """
        return self.db.execute(q).fetchall()

    def diagnosis_cases(self):
        q = """
        SELECT diagnosis, COUNT(*) AS total_cases
        FROM visits
        GROUP BY diagnosis
        ORDER BY total_cases DESC;
        """
        return self.db.execute(q).fetchall()

    def visits_by_type(self):
        q = """
        SELECT visit_type, COUNT(*) AS total_visits
        FROM visits
        GROUP BY visit_type;
        """
        return self.db.execute(q).fetchall()

    def visits_by_department(self):
        q = """
        SELECT d.department_name, COUNT(v.visit_id) AS total_visits
        FROM visits v
        JOIN doctors doc ON v.doctor_id = doc.doctor_id
        JOIN department d ON doc.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY total_visits DESC;
        """
        return self.db.execute(q).fetchall()

    def visits_by_doctor(self):
        q = """
        SELECT doc.first_name, doc.last_name, COUNT(v.visit_id) AS total_visits
        FROM visits v
        JOIN doctors doc ON v.doctor_id = doc.doctor_id
        GROUP BY doc.doctor_id
        ORDER BY total_visits DESC;
        """
        return self.db.execute(q).fetchall()

    def revenue_by_department(self):
        q = """
        SELECT d.department_name, SUM(b.total_amount) AS revenue
        FROM billing b
        JOIN visits v ON b.visit_id = v.visit_id
        JOIN doctors doc ON v.doctor_id = doc.doctor_id
        JOIN department d ON doc.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY revenue DESC;
        """
        return self.db.execute(q).fetchall()

    def avg_revenue(self):
        q = "SELECT ROUND(AVG(total_amount),2) AS avg_revenue FROM billing"
        return self.db.execute(q).fetchone()["avg_revenue"]

    def avg_admission_days(self):
        q = """
        SELECT ROUND(AVG(DATEDIFF(discharge_date, visit_date)),2) AS avg_days
        FROM visits
        WHERE visit_type='Admission';
        """
        return self.db.execute(q).fetchone()["avg_days"]

    def readmission_rate(self):
        q = """
        SELECT 
            COUNT(*) / (SELECT COUNT(*) FROM patients) * 100 AS rate
        FROM (
            SELECT v1.patient_id
            FROM visits v1
            JOIN visits v2 ON v1.patient_id = v2.patient_id 
               AND v2.visit_id > v1.visit_id
               AND DATEDIFF(v2.visit_date, v1.visit_date) <= 30
        ) x;
        """
        return self.db.execute(q).fetchone()["rate"]

def ensure_session():
    if "user" not in st.session_state:
        st.session_state.user = None

def login_view(user_service: UserService):
    st.title("🔐 Hospital Management System")
    st.subheader("Login to Continue")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_btn"):
        user = user_service.authenticate(username, password)
        if user:
            st.session_state.user = {
                "username": user["username"],
                "role": user["role"],
                "patient_id": user.get("patient_id"),
                "doctor_id": user.get("doctor_id")
            }
            st.success(f"Welcome {user['username']} 👋")
            st.rerun()
        else:
            st.error("Invalid login details")

def admin_dashboard(analytics_service):
    st.title("📊 Hospital Analytics Dashboard")

    counts = analytics_service.counts()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Patients", counts["patients"])
    c2.metric("Doctors", counts["doctors"])
    c3.metric("Departments", counts["departments"])
    c4.metric("Visits", counts["visits"])

    c5, c6, c7 = st.columns(3)
    c5.metric("Appointments", counts["appointments"])
    c6.metric("Treatments", counts["treatments"])
    c7.metric("Bills", counts["billing"])

    st.subheader("📈 Yearly Patient Registrations")
    yearly = analytics_service.yearly_patients()
    if yearly:
        df = pd.DataFrame(yearly)
        df = df.set_index("year")
        st.bar_chart(df)
    else:
        st.info("No patient registration data available.")

    st.subheader("🩺 Cases by Diagnosis")
    diag = analytics_service.diagnosis_cases()
    st.dataframe(pd.DataFrame(diag))

    st.subheader("🏥 Visits by Type")
    vtype = analytics_service.visits_by_type()
    if vtype:
        df = pd.DataFrame(vtype).set_index("visit_type")
        st.bar_chart(df)

    st.subheader("🏬 Visits by Department")
    vdept = analytics_service.visits_by_department()
    if vdept:
        df = pd.DataFrame(vdept).set_index("department_name")
        st.bar_chart(df)

    st.subheader("👨‍⚕️ Visits by Doctor")
    vdoc = analytics_service.visits_by_doctor()
    if vdoc:
        df = pd.DataFrame(vdoc)
        df["Doctor"] = df["first_name"] + " " + df["last_name"]
        df = df.set_index("Doctor")["total_visits"]
        st.bar_chart(df)

    st.subheader("💰 Revenue by Department")
    rev = analytics_service.revenue_by_department()
    if rev:
        df = pd.DataFrame(rev).set_index("department_name")["revenue"]
        st.bar_chart(df)

    a, b, c = st.columns(3)
    a.metric("Avg Revenue per Patient", analytics_service.avg_revenue())
    b.metric("Avg Admission Days", analytics_service.avg_admission_days())
    c.metric("Readmission Rate (%)", round(analytics_service.readmission_rate(), 2))

def admin_patients(patient_service):
    st.title("👤 Patient Management")

    tab1, tab2 = st.tabs(["➕ Add Patient", "📋 View / Update / Delete"])

    with tab1:
        first = st.text_input("First Name", key="pat_add_first")
        last = st.text_input("Last Name", key="pat_add_last")
        gender = st.selectbox("Gender", ["Male", "Female", "Others"], key="pat_add_gender")
        dob = st.date_input("Date of Birth", key="pat_add_dob")
        phone = st.text_input("Phone Number", key="pat_add_phone")
        city = st.text_input("City", key="pat_add_city")
        reg_date = st.date_input("Registration Date", value=date.today(), key="pat_add_regdate")

        if st.button("Save Patient", key="pat_add_btn"):
            patient_service.add(first, last, gender, dob, phone, city, reg_date)
            st.success("Patient added successfully ✔")

    with tab2:
        data = patient_service.get_all()
        if not data:
            st.info("No patients found.")
            return

        df = pd.DataFrame(data)
        st.dataframe(df)

        ids = [p["Patient_id"] for p in data]
        sel = st.selectbox("Select Patient ID", ids, key="pat_edit_select")

        record = patient_service.get_by_id(sel)

        first = st.text_input("First Name", record["First_Name"], key=f"pat_edit_first_{sel}")
        last = st.text_input("Last Name", record["Last_Name"], key=f"pat_edit_last_{sel}")
        gender = st.selectbox("Gender", ["Male", "Female", "Others"],
                              index=["Male", "Female", "Others"].index(record["Gender"]),
                              key=f"pat_edit_gender_{sel}")
        dob = st.date_input("Date of Birth", record["Dob"], key=f"pat_edit_dob_{sel}")
        phone = st.text_input("Phone", record["Phone"], key=f"pat_edit_phone_{sel}")
        city = st.text_input("City", record["City"], key=f"pat_edit_city_{sel}")
        reg_date = st.date_input("Reg Date", record["Registration_Date"], key=f"pat_edit_regdate_{sel}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Update", key=f"pat_update_{sel}"):
                patient_service.update(sel, first, last, gender, dob, phone, city, reg_date)
                st.success("Updated ✔")
                st.rerun()

        with c2:
            if st.button("Delete", key=f"pat_delete_{sel}"):
                patient_service.delete(sel)
                st.warning("Deleted ❌")
                st.rerun()

def admin_departments(dept_service):
    st.title("🏬 Department Management")

    tab1, tab2 = st.tabs(["➕ Add Department", "📋 View / Update / Delete"])

    with tab1:
        name = st.text_input("Department Name", key="dept_add_name")
        if st.button("Save", key="dept_add_btn"):
            dept_service.add(name)
            st.success("Department added ✔")

    with tab2:
        data = dept_service.get_all()
        if not data:
            st.info("No departments found.")
            return

        df = pd.DataFrame(data)
        st.dataframe(df)

        ids = [d["Department_id"] for d in data]
        sel = st.selectbox("Select Department ID", ids, key="dept_edit_select")
        record = dept_service.get_by_id(sel)

        name = st.text_input("Department Name", record["Department_name"], key=f"dept_edit_name_{sel}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Update", key=f"dept_update_{sel}"):
                dept_service.update(sel, name)
                st.success("Updated ✔")
                st.rerun()

        with c2:
            if st.button("Delete", key=f"dept_delete_{sel}"):
                dept_service.delete(sel)
                st.warning("Deleted ❌")
                st.rerun()

def admin_doctors(doctor_service, dept_service):
    st.title("👨‍⚕️ Doctor Management")

    tab1, tab2 = st.tabs(["➕ Add Doctor", "📋 View / Update / Delete"])

    with tab1:
        first = st.text_input("First Name", key="doc_add_first")
        last = st.text_input("Last Name", key="doc_add_last")
        phone = st.text_input("Phone", key="doc_add_phone")
        spec = st.text_input("Specialization", key="doc_add_spec")

        depts = dept_service.get_all()
        dept_ids = [d["Department_id"] for d in depts]
        dept_id = st.selectbox("Department", dept_ids, key="doc_add_dept")

        if st.button("Save Doctor", key="doc_add_btn"):
            doctor_service.add(first, last, phone, spec, dept_id)
            st.success("Doctor added ✔")

    with tab2:
        data = doctor_service.get_all()
        if not data:
            st.info("No doctors found.")
            return

        df = pd.DataFrame(data)
        st.dataframe(df)

        ids = [d["Doctor_id"] for d in data]
        sel = st.selectbox("Select Doctor ID", ids, key="doc_edit_select")
        record = doctor_service.get_by_id(sel)

        first = st.text_input("First Name", record["First_Name"], key=f"doc_edit_first_{sel}")
        last = st.text_input("Last Name", record["Last_Name"], key=f"doc_edit_last_{sel}")
        phone = st.text_input("Phone", record["Phone"], key=f"doc_edit_phone_{sel}")
        spec = st.text_input("Specialization", record["Specialization"], key=f"doc_edit_spec_{sel}")

        dept_ids = [d["Department_id"] for d in dept_service.get_all()]
        dept_id = st.selectbox("Department", dept_ids,
                               index=dept_ids.index(record["Department_id"]),
                               key=f"doc_edit_dept_{sel}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Update", key=f"doc_update_{sel}"):
                doctor_service.update(sel, first, last, phone, spec, dept_id)
                st.success("Updated")
                st.rerun()

        with c2:
            if st.button("Delete", key=f"doc_delete_{sel}"):
                doctor_service.delete(sel)
                st.warning("Deleted")
                st.rerun()

def admin_appointments(appt_service, patient_service, doctor_service):
    st.title("📅 Appointment Management")

    tab1, tab2 = st.tabs(["➕ Add Appointment", "📋 View / Update / Delete"])

    pats = patient_service.get_all()
    docs = doctor_service.get_all()
    pat_ids = [p["Patient_id"] for p in pats]
    doc_ids = [d["Doctor_id"] for d in docs]

    with tab1:
        pid = st.selectbox("Patient", pat_ids, key="appt_add_pid")
        did = st.selectbox("Doctor", doc_ids, key="appt_add_did")
        app_date = st.date_input("Appointment Date", key="appt_add_date")
        status = st.selectbox("Status", ["Booked", "Completed", "Cancelled", "No-Show"], key="appt_add_status")

        if st.button("Save Appointment", key="appt_add_btn"):
            appt_service.add(pid, did, app_date, status)
            st.success("Appointment added ✔")

    with tab2:
        data = appt_service.get_all()
        if not data:
            st.info("No appointments found.")
            return

        df = pd.DataFrame(data)
        st.dataframe(df)

        ids = [d["Appointment_id"] for d in data]
        sel = st.selectbox("Select Appointment ID", ids, key="appt_edit_select")
        rec = appt_service.get_by_id(sel)

        pid = st.selectbox("Patient", pat_ids, index=pat_ids.index(rec["Patient_id"]), key=f"appt_edit_pid_{sel}")
        did = st.selectbox("Doctor", doc_ids, index=doc_ids.index(rec["Doctor_id"]), key=f"appt_edit_did_{sel}")
        app_date = st.date_input("Appointment Date", rec["Appointment_Date"], key=f"appt_edit_date_{sel}")
        status = st.selectbox("Status", ["Booked", "Completed", "Cancelled", "No-Show"],
                              index=["Booked", "Completed", "Cancelled", "No-Show"].index(rec["Appointment_status"]),
                              key=f"appt_edit_status_{sel}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Update", key=f"appt_update_{sel}"):
                appt_service.update(sel, pid, did, app_date, status)
                st.success("Updated ✔")
                st.rerun()

        with c2:
            if st.button("Delete", key=f"appt_del_{sel}"):
                appt_service.delete(sel)
                st.warning("Deleted")
                st.rerun()

def admin_visits(visit_service, patient_service, doctor_service):
    st.title("📝 Visit Management")

    tab1, tab2 = st.tabs(["➕ Add Visit", "📋 View / Update / Delete"])

    pats = patient_service.get_all()
    docs = doctor_service.get_all()

    pat_ids = [p["Patient_id"] for p in pats]
    doc_ids = [d["Doctor_id"] for d in docs]

    with tab1:
        pid = st.selectbox("Patient", pat_ids, key="visit_add_pid")
        did = st.selectbox("Doctor", doc_ids, key="visit_add_did")
        vdate = st.date_input("Visit Date", key="visit_add_date")
        vtype = st.selectbox("Visit Type", ["OPD", "Emergency", "Admission"], key="visit_add_type")
        diagnosis = st.text_input("Diagnosis", key="visit_add_diag")
        discharge_date = st.date_input("Discharge Date", key="visit_add_discharge")

        if st.button("Save Visit", key="visit_add_btn"):
            visit_service.add(pid, did, vdate, vtype, diagnosis, discharge_date)
            st.success("Visit added ✔")

    with tab2:
        data = visit_service.get_all()
        if not data:
            st.info("No visit records found.")
            return

        df = pd.DataFrame(data)
        st.dataframe(df)

        ids = [v["Visit_id"] for v in data]
        sel = st.selectbox("Select Visit ID", ids, key="visit_edit_select")
        rec = visit_service.get_by_id(sel)

        pid = st.selectbox("Patient", pat_ids, index=pat_ids.index(rec["Patient_id"]),
                           key=f"visit_edit_pid_{sel}")

        did = st.selectbox("Doctor", doc_ids, index=doc_ids.index(rec["Doctor_id"]),
                           key=f"visit_edit_did_{sel}")

        vdate = st.date_input("Visit Date", rec["Visit_Date"], key=f"visit_edit_date_{sel}")
        vtype = st.selectbox(
            "Visit Type",
            ["OPD", "Emergency", "Admission"],
            index=["OPD", "Emergency", "Admission"].index(rec["Visit_Type"]),
            key=f"visit_edit_type_{sel}"
        )
        diagnosis = st.text_input("Diagnosis", rec["Diagnosis"], key=f"visit_edit_diag_{sel}")
        discharge_date = st.date_input("Discharge Date", rec["Discharge_Date"],
                                       key=f"visit_edit_discharge_{sel}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Update Visit", key=f"visit_update_{sel}"):
                visit_service.update(sel, pid, did, vdate, vtype, diagnosis, discharge_date)
                st.success("Visit updated ✔")
                st.rerun()

        with c2:
            if st.button("Delete Visit", key=f"visit_delete_{sel}"):
                visit_service.delete(sel)
                st.warning("Visit deleted ❌")
                st.rerun()

def admin_treatments(treatment_service, visit_service):
    st.title("💉 Treatment Management")

    tab1, tab2 = st.tabs(["➕ Add Treatment", "📋 View / Update / Delete"])

    visits = visit_service.get_all()
    visit_ids = [v["Visit_id"] for v in visits]

    with tab1:
        vid = st.selectbox("Visit ID", visit_ids, key="treat_add_vid")
        name = st.text_input("Treatment Name", key="treat_add_name")
        category = st.selectbox("Category", ["Test", "Surgery", "Medication", "Therapy"],
                                key="treat_add_category")
        cost = st.number_input("Cost", min_value=0, step=50, key="treat_add_cost")

        if st.button("Save Treatment", key="treat_add_btn"):
            treatment_service.add(vid, name, category, cost)
            st.success("Treatment added ✔")

    with tab2:
        data = treatment_service.get_all()
        if not data:
            st.info("No treatment records found.")
            return

        df = pd.DataFrame(data)
        st.dataframe(df)

        ids = [t["Treatment_id"] for t in data]
        sel = st.selectbox("Select Treatment ID", ids, key="treat_edit_select")
        rec = treatment_service.get_by_id(sel)

        vid = st.selectbox("Visit ID", visit_ids,
                           index=visit_ids.index(rec["Visit_id"]),
                           key=f"treat_edit_vid_{sel}")

        name = st.text_input("Treatment Name", rec["Treatment_Name"],
                             key=f"treat_edit_name_{sel}")

        category = st.selectbox(
            "Category",
            ["Test", "Surgery", "Medication", "Therapy"],
            index=["Test", "Surgery", "Medication", "Therapy"].index(rec["Treatment_Category"]),
            key=f"treat_edit_category_{sel}"
        )

        cost = st.number_input("Cost", min_value=0, value=rec["Treatment_Cost"],
                               key=f"treat_edit_cost_{sel}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Update Treatment", key=f"treat_update_{sel}"):
                treatment_service.update(sel, vid, name, category, cost)
                st.success("Updated ✔")
                st.rerun()

        with c2:
            if st.button("Delete Treatment", key=f"treat_delete_{sel}"):
                treatment_service.delete(sel)
                st.warning("Deleted ❌")
                st.rerun()

def admin_billing(billing_service, visit_service):
    st.title("💳 Billing Management")

    tab1, tab2 = st.tabs(["➕ Add Bill", "📋 View / Update / Delete"])

    visits = visit_service.get_all()
    visit_ids = [v["Visit_id"] for v in visits]

    with tab1:
        vid = st.selectbox("Visit ID", visit_ids, key="bill_add_vid")
        bill_date = st.date_input("Bill Date", value=date.today(), key="bill_add_date")
        total = st.number_input("Total Amount", min_value=0, step=100, key="bill_add_total")
        method = st.selectbox("Payment Method", ["Cash", "Card", "Insurance"], key="bill_add_method")
        status = st.selectbox("Payment Status", ["Paid", "Pending", "Partially Paid"],
                              key="bill_add_status")

        if st.button("Save Bill", key="bill_add_btn"):
            billing_service.add(vid, bill_date, total, method, status)
            st.success("Bill added ✔")

    with tab2:
        data = billing_service.get_all()
        if not data:
            st.info("No billing records found.")
            return

        df = pd.DataFrame(data)
        st.dataframe(df)

        ids = [b["Bill_id"] for b in data]
        sel = st.selectbox("Select Bill ID", ids, key="bill_edit_select")
        rec = billing_service.get_by_id(sel)

        vid = st.selectbox("Visit ID", visit_ids,
                           index=visit_ids.index(rec["Visit_id"]),
                           key=f"bill_edit_vid_{sel}")

        bill_date = st.date_input("Bill Date", rec["Bill_Date"], key=f"bill_edit_date_{sel}")
        total = st.number_input("Total Amount", min_value=0, value=rec["Total_Amount"],
                                key=f"bill_edit_total_{sel}")

        method = st.selectbox(
            "Payment Method",
            ["Cash", "Card", "Insurance"],
            index=["Cash", "Card", "Insurance"].index(rec["Payment_Method"]),
            key=f"bill_edit_method_{sel}"
        )

        status = st.selectbox(
            "Payment Status",
            ["Paid", "Pending", "Partially Paid"],
            index=["Paid", "Pending", "Partially Paid"].index(rec["Payment_Status"]),
            key=f"bill_edit_status_{sel}"
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Update Bill", key=f"bill_update_{sel}"):
                billing_service.update(sel, vid, bill_date, total, method, status)
                st.success("Updated")
                st.rerun()

        with c2:
            if st.button("Delete Bill", key=f"bill_delete_{sel}"):
                billing_service.delete(sel)
                st.warning("Deleted")
                st.rerun()

def patient_portal(choice, user, appt_service, visit_service, billing_service, doctor_service):
    patient_id = user.get("patient_id")
    if not patient_id:
        st.error("No patient linked with this account. Contact Admin.")
        return

    if choice == "Book Appointment":
        st.title("📅 Book Appointment")

        doctors = doctor_service.get_all()
        if not doctors:
            st.info("No doctors available.")
            return

        doc_map = {
            f"{d['First_Name']} {d['Last_Name']} ({d['Specialization']})": d["Doctor_id"]
            for d in doctors
        }

        selected_doc = st.selectbox(
            "Choose Doctor",
            list(doc_map.keys()),
            key="pat_book_doc"
        )
        app_date = st.date_input("Appointment Date", key="pat_book_date")

        if st.button("Book Appointment", key="pat_book_btn"):
            appt_service.add(patient_id, doc_map[selected_doc], app_date, "Booked")
            st.success("Appointment booked successfully ✔")

    elif choice == "My Appointments":
        st.title("📘 My Appointments")

        q = f"""
        SELECT a.*, d.First_Name AS Doctor_First, d.Last_Name AS Doctor_Last
        FROM appointments a
        JOIN doctors d ON a.Doctor_id = d.Doctor_id
        WHERE a.Patient_id = {patient_id}
        ORDER BY a.Appointment_Date DESC
        """

        data = appt_service.db.execute(q).fetchall()
        if data:
            st.dataframe(pd.DataFrame(data))
        else:
            st.info("No appointments yet.")

    elif choice == "My Past Visits":
        st.title("📝 My Visit History")

        q = f"""
        SELECT v.*, d.First_Name AS Doctor_First, d.Last_Name AS Doctor_Last
        FROM visits v
        JOIN doctors d ON v.Doctor_id = d.Doctor_id
        WHERE v.Patient_id = {patient_id}
        ORDER BY v.Visit_Date DESC
        """

        data = visit_service.db.execute(q).fetchall()
        if data:
            st.dataframe(pd.DataFrame(data))
        else:
            st.info("No visit history yet.")

    elif choice == "My Bills":
        st.title("💳 Billing History")

        q = f"""
        SELECT b.*, v.Visit_Date, v.Visit_Type
        FROM billing b
        JOIN visits v ON b.Visit_id = v.Visit_id
        WHERE v.Patient_id = {patient_id}
        ORDER BY b.Bill_Date DESC
        """

        data = billing_service.db.execute(q).fetchall()
        if data:
            st.dataframe(pd.DataFrame(data))
        else:
            st.info("No bills generated yet.")

def doctor_portal(choice, user, appt_service, visit_service, treatment_service):
    doctor_id = user.get("doctor_id")
    if not doctor_id:
        st.error("No doctor linked with this account. Contact Admin.")
        return

    if choice == "My Appointments":
        st.title("📅 My Appointments")

        q = f"""
        SELECT a.*, 
               p.First_Name AS Patient_First, 
               p.Last_Name AS Patient_Last
        FROM appointments a
        JOIN patients p ON a.Patient_id = p.Patient_id
        WHERE a.Doctor_id = {doctor_id}
        ORDER BY a.Appointment_Date DESC
        """

        data = appt_service.db.execute(q).fetchall()
        if data:
            st.dataframe(pd.DataFrame(data))
        else:
            st.info("No appointments found.")

    elif choice == "Patient Visit History":
        st.title("📝 Patient Visit History")

        q = f"""
        SELECT v.*, 
               p.First_Name AS Patient_First, 
               p.Last_Name AS Patient_Last
        FROM visits v
        JOIN patients p ON v.Patient_id = p.Patient_id
        WHERE v.Doctor_id = {doctor_id}
        ORDER BY v.Visit_Date DESC
        """

        data = visit_service.db.execute(q).fetchall()
        if data:
            st.dataframe(pd.DataFrame(data))
        else:
            st.info("No visit history found.")

    elif choice == "Treatments Done":
        st.title("💉 Treatments Performed")

        q = f"""
        SELECT t.*, 
               v.Patient_Id AS Patient_ID
        FROM treatment t
        JOIN visits v ON t.Visit_id = v.Visit_id
        WHERE v.Doctor_id = {doctor_id}
        ORDER BY t.Treatment_id DESC
        """

        data = treatment_service.db.execute(q).fetchall()
        if data:
            st.dataframe(pd.DataFrame(data))
        else:
            st.info("No treatments recorded.")

def main_app():
    user = st.session_state["user"]
    role = user["role"]

    st.sidebar.markdown(f"### 👤 Logged in as: **{user['username']}** ({role})")

    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state["user"] = None
        st.rerun()

    patient_service = PatientService()
    dept_service = DepartmentService()
    doctor_service = DoctorService()
    appt_service = AppointmentService()
    visit_service = VisitService()
    treatment_service = TreatmentService()
    billing_service = BillingService()
    analytics_service = AnalyticsService()

    if role == "Admin":
        menu = [
            "Dashboard / Analytics",
            "Patients",
            "Departments",
            "Doctors",
            "Appointments",
            "Visits",
            "Treatments",
            "Billing"
        ]

    elif role == "Patient":
        menu = [
            "Book Appointment",
            "My Appointments",
            "My Past Visits",
            "My Bills"
        ]

    elif role == "Doctor":
        menu = [
            "My Appointments",
            "Patient Visit History",
            "Treatments Done"
        ]

    choice = st.sidebar.selectbox("Menu", menu, key="menu_selector")

    if role == "Patient":
        patient_portal(
            choice, user,
            appt_service, visit_service,
            billing_service, doctor_service
        )
        return

    if role == "Doctor":
        doctor_portal(
            choice, user,
            appt_service, visit_service,
            treatment_service
        )
        return
    if choice == "Dashboard / Analytics":
        st.title("📊 Hospital Analytics Dashboard")

        stats = analytics_service.counts()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Patients", stats["patients"])
        col2.metric("Doctors", stats["doctors"])
        col3.metric("Departments", stats["departments"])
        col4.metric("Visits", stats["visits"])

        st.subheader("📈 Yearly Patient Registrations")
        yp = analytics_service.yearly_patients()

        if yp:
            df = pd.DataFrame(yp)

            fig, ax = plt.subplots()
            ax.plot(df["year"], df["total_patients"], marker="o")
            ax.set_xlabel("Year")
            ax.set_ylabel("Total Patients")
            ax.set_title("Yearly Patient Count")
            st.pyplot(fig)
        else:
            st.info("No patient registration data available.")

        st.subheader("🩺 Cases by Diagnosis")
        diag = analytics_service.diagnosis_cases()

        if diag:
            df = pd.DataFrame(diag)

            fig, ax = plt.subplots()
            ax.bar(df["diagnosis"], df["total_cases"])
            ax.set_xlabel("Diagnosis")
            ax.set_ylabel("Cases")
            ax.set_title("Diagnosis Counts")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.subheader("🏥 Visits by Type")
        vtype = analytics_service.visits_by_type()

        if vtype:
            df = pd.DataFrame(vtype)

            fig, ax = plt.subplots()
            ax.pie(df["total_visits"], labels=df["visit_type"], autopct="%1.1f%%")
            ax.set_title("Visit Distribution")
            st.pyplot(fig)

        st.subheader("🏛 Visits by Department")
        vdept = analytics_service.visits_by_department()

        if vdept:
            df = pd.DataFrame(vdept)

            fig, ax = plt.subplots()
            ax.bar(df["department_name"], df["total_visits"])
            ax.set_title("Department Workload")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.subheader("👨‍⚕️ Visits by Doctor")
        vdoc = analytics_service.visits_by_doctor()

        if vdoc:
            df = pd.DataFrame(vdoc)
            df["Doctor"] = df["first_name"] + " " + df["last_name"]

            fig, ax = plt.subplots()
            ax.bar(df["Doctor"], df["total_visits"])
            ax.set_title("Doctor Workload")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.subheader("💰 Revenue by Department")
        rev = analytics_service.revenue_by_department()

        if rev:
            df = pd.DataFrame(rev)

            fig, ax = plt.subplots()
            ax.bar(df["department_name"], df["revenue"])
            ax.set_title("Revenue Breakdown")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        colA, colB, colC = st.columns(3)
        colA.metric("Avg Revenue Per Patient", analytics_service.avg_revenue())
        colB.metric("Avg Admission Days", analytics_service.avg_admission_days())
        colC.metric("Readmission Rate (%)", round(analytics_service.readmission_rate(), 2))



    elif choice == "Patients":
        admin_patients(patient_service)

    elif choice == "Departments":
        admin_departments(dept_service)

    elif choice == "Doctors":
        admin_doctors(doctor_service, dept_service)

    elif choice == "Appointments":
        admin_appointments(appt_service, patient_service, doctor_service)

    elif choice == "Visits":
        admin_visits(visit_service, patient_service, doctor_service)

    elif choice == "Treatments":
        admin_treatments(treatment_service, visit_service)

    elif choice == "Billing":
        admin_billing(billing_service, visit_service)

def main():
    st.set_page_config(page_title="Hospital Management System", layout="wide")
    ensure_session()

    if st.session_state.user is None:
        user_service = UserService()
        login_view(user_service)
    else:
        main_app()

if __name__ == "__main__":
    main()


