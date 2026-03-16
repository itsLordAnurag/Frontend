import pandas as pd
from datetime import datetime
from database import get_db
from bson import ObjectId

# Helper function to convert mongo cursor to pandas dataframe
def cursor_to_df(cursor, id_field='_id', rename_id_to=None):
    df = pd.DataFrame(list(cursor))
    if not df.empty and id_field in df.columns:
        df[id_field] = df[id_field].astype(str)
        if rename_id_to:
            df.rename(columns={id_field: rename_id_to}, inplace=True)
    return df

# --- Patient Operations ---
def add_patient(first_name, last_name, phone, dob, age):
    db = get_db()
    db.patients.insert_one({
        "FirstName": first_name,
        "LastName": last_name,
        "PhoneNumber": phone,
        "DateOfBirth": dob.strftime("%Y-%m-%d") if hasattr(dob, 'strftime') else str(dob),
        "Age": age
    })

def get_patients():
    db = get_db()
    cursor = db.patients.find()
    return cursor_to_df(cursor, rename_id_to='PatientID')

# --- Symptom Operations ---
def add_symptom(patient_id, symptom_type, severity, description):
    db = get_db()
    db.symptoms.insert_one({
        "PatientID": str(patient_id),
        "SymptomType": symptom_type,
        "Severity": severity,
        "Description": description,
        "RecordedAt": datetime.now()
    })

def get_symptoms(patient_id):
    db = get_db()
    cursor = db.symptoms.find({"PatientID": str(patient_id)})
    return cursor_to_df(cursor, rename_id_to='SymptomID')