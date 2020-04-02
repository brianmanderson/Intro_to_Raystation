from connect import *


def ChangePatient(patient_db, patient_id):
    info = patient_db.QueryPatientInfo(Filter={"PatientID": patient_id},UseIndexService=True)
    patient = patient_db.LoadPatient(PatientInfo=info[0], AllowPatientUpgrade=True)
    return patient


patient_db = get_current("PatientDB")
MRNs = ['000000011']
case = get_current('Case')
for MRN in MRNs:
    patient = ChangePatient(patient_db, MRN)
    for case in patient.Cases:
        case.SetCurrent()