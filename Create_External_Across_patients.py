from connect import *


def ChangePatient(patient_db, patient_id):
    info_all = patient_db.QueryPatientInfo(Filter={"PatientID": patient_id})
    # If it isn't, see if it's in the secondary database
    if not info_all:
        info_all = patient_db.QueryPatientInfo(Filter={"PatientID": patient_id}, UseIndexService=False)
    info = []
    for info_temp in info_all:
        if info_temp['PatientID'] == patient_id:
            info = info_temp
            break
    return patient_db.LoadPatient(PatientInfo=info, AllowPatientUpgrade=False)



def main():
    patient_db = get_current("PatientDB")
    MRNs = ['000000011']
    case = get_current('Case')
    for MRN in MRNs:
        patient = ChangePatient(patient_db, MRN)
        for case in patient.Cases:
            case.PatientModel.CreateRoi(Name="External", Color="Blue", Type="External",
                                        TissueName=None, RbeCellTypeName=None,
                                        RoiMaterial=None)
            for exam in case.Examinations:
                case.PatientModel.RegionsOfInterest._External.CreateExternalGeometry(
                    Examination=exam)


if __name__ == '__main__':
    main()