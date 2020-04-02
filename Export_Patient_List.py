__author__ = 'Brian M Anderson'
# Created on 4/2/2020

from connect import *
import os


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

patient_db = get_current("PatientDB")
MRN_list = []
fid = open(r'K:\Morfeus\BMAnderson\test\MRN_list.txt')
for line in fid:
    line = line.strip('\n')
    MRN_list.append(line)
fid.close()

base_export_path = r'K:\Morfeus\BMAnderson\test\output2'
for MRN in MRN_list:
    patient = ChangePatient(patient_db,MRN)
    for case in patient.Cases:
        rois_in_case = []
        for roi in case.PatientModel.RegionsOfInterest:
            rois_in_case.append(roi.Name)
        wanted_rois = []
        for roi in rois_in_case:
            for roi_wanted in ['_flair_','_t1c_']:
                if roi.lower().find(roi_wanted) != -1:
                    wanted_rois.append(roi)
        for exam in case.Examinations:
            for roi in wanted_rois:
                if not case.PatientModel.StructureSets[exam.Name].RoiGeometries[roi].HasContours():
                    export_path = os.path.join(base_export_path, patient.PatientID, exam.Name)
                    if not os.path.exists(export_path):
                        os.makedirs(export_path)
                        case.ScriptableDicomExport(ExportFolderPath=export_path, Examinations=[exam.Name],
                                                   RtStructureSetsForExaminations=[exam.Name])