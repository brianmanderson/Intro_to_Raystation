from connect import *

case = get_current('Case')
patient = get_current('Patient')

for case in patient.Cases:
    rois_in_case = []
    for roi in case.PatientModel.RegionsOfInterest:
        rois_in_case.append(roi.Name)
    if 'External' not in rois_in_case:
        case.PatientModel.CreateRoi(Name="External", Color="Green",
                                    Type="External", TissueName="",
                                    RbeCellTypeName=None, RoiMaterial=None)
    for exam in case.Examinations:
        case.PatientModel.RegionsOfInterest['External'].\
            CreateExternalGeometry(Examination=exam, ThresholdLevel=-250)
