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
            rois_in_case = []
            for roi in case.PatientModel.RegionsOfInterest:
                rois_in_case.append(roi.Name)
            if 'External' not in rois_in_case:
                case.PatientModel.CreateRoi(Name="External", Color="Green",
                                            Type="External", TissueName="",
                                            RbeCellTypeName=None, RoiMaterial=None)
            primary = 'CT 1'
            rois_in_primary = []
            for roi in rois_in_case:
                if case.PatientModel.StructureSets[primary].RoiGeometries[roi].HasContours():
                    rois_in_primary.append(roi)
            for exam in case.Examinations:
                case.PatientModel.RegionsOfInterest._External.CreateExternalGeometry(
                    Examination=exam)


            target_exams = []
            for exam in case.Examinations:
                if exam.Name != primary:
                    target_exams.append(exam.Name)
                    case.ComputeRigidImageRegistration(
                        FloatingExaminationName=primary,ReferenceExaminationName = exam.Name,
                        UseOnlyTranslations = False,
                        HighWeightOnBones = True, InitializeImages = True,
                        FocusRoisNames = [], RegistrationName = "BMA_Rigid")
            case.PatientModel.CopyRoiGeometries(SourceExamination=case.Examinations[primary],
                                                TargetExaminationNames=target_exams,
                                                RoiNames=rois_in_primary)


if __name__ == '__main__':
    main()
