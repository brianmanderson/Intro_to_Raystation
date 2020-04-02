__author__ = 'Brian M Anderson'
# Created on 4/2/2020

from connect import *


def get_contour_points_from_roi(geometry):
    '''
    :param geometry: Geometry from case.PatientModel.StructureSets[CT x].RoiGeometries['Roi_name']
    :return:
    '''
    try:    # is it a contour?
        old_contours = geometry.PrimaryShape.Contours

        new_contours = []

        for contour in old_contours:
            new_contour = []
            for point in contour:
                new_contour.append({'x': point.x, 'y': point.y, 'z': point.z})
            new_contours.append(new_contour)

        return new_contours
    except:
        return None


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


def copy_roi_to_another(patient):
    for case in patient.Cases:
        rois_in_case = []
        for roi in case.PatientModel.RegionsOfInterest:
            rois_in_case.append(roi.Name)
        if 'Disease' not in rois_in_case:
            continue
        if 'Disease_BMA' not in rois_in_case:
            case.PatientModel.CreateRoi(Name="Disease_BMA", Color="Blue")
        for exam in case.Examinations:
            if not case.PatientModel.StructureSets[exam.Name].RoiGeometries['Disease_BMA'].HasContours():
                if case.PatientModel.StructureSets[exam.Name].RoiGeometries['Disease'].HasContours():
                    case.PatientModel.RegionsOfInterest['Disease_BMA'].CreateExternalGeometry(Examination=exam,
                                                                                              ThresholdLevel=-250)
        if case.PatientModel.RegionsOfInterest['Disease_BMA'].Type == 'External':
            case.PatientModel.RegionsOfInterest['Disease_BMA'].Type = case.PatientModel.RegionsOfInterest['Disease'].Type
            for exam in case.Examinations:
                if case.PatientModel.StructureSets[exam.Name].RoiGeometries['Disease'].HasContours():
                    new_contours = get_contour_points_from_roi(case.PatientModel.StructureSets[exam.Name]
                                                               .RoiGeometries['Disease'])
                    case.PatientModel.StructureSets[exam.Name].RoiGeometries['Disease_BMA'].PrimaryShape.Contours = new_contours
    return None


def copy_Lits_Disease():
    patient_db = get_current("PatientDB")
    info_all = patient_db.QueryPatientInfo(Filter={"PatientID": 'LiTs'})
    for info in info_all:
        patient = patient_db.LoadPatient(PatientInfo=info, AllowPatientUpgrade=False)
        copy_roi_to_another(patient)
        patient.Save()


if __name__ == '__main__':
    copy_Lits_Disease()