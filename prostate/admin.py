from django.contrib import admin

from prostate.models import patientdata, Hospital, TreatmentRecord, Doctor, Diagnosis

# Register your models here.
admin.site.register([patientdata, Hospital, TreatmentRecord, Doctor, Diagnosis])
