from connect import *

case = get_current('Case')
case.PatientModel.CreateRoi(Name="Test3", Color="Blue", Type="Organ",
                            TissueName=None, RbeCellTypeName=None,
                            RoiMaterial=None)
