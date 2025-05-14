from .auth import authbp
from .lab_result import lab_resultbp
from .med_record import med_recordbp
from .patient import patientbp
from .prescription import prescriptionbp
from .user import userbp


all_blueprints = [authbp,
                  lab_resultbp,
                  med_recordbp,
                  patientbp,
                  prescriptionbp,
                  userbp]
