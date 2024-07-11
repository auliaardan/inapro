from django.conf.urls.static import static
from django.urls import path

from Inapro import settings
from .views import publicView, dashboardView, DashboardUpdateView, PatientListView, PatientCreateView, \
    PatientDeleteView, PatientUpdateView, DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView, \
    TreatmentRecordListView, TreatmentRecordCreateView, TreatmentRecordUpdateView, TreatmentRecordDeleteView, \
    PatientDetailView, HospitalCreateView, HospitalDeleteView, HospitalListView, HospitalUpdateView, \
    DiagnosisListView, DiagnosisCreateView, DiagnosisDeleteView, DiagnosisUpdateView, get_treatment_record

urlpatterns = [
                  path('treatmentrecords/', TreatmentRecordListView.as_view(), name='treatmentrecord_list'),
                  path('treatmentrecords/new/<int:patient_id>/', TreatmentRecordCreateView.as_view(), name='treatmentrecord_create'),
                  path('treatmentrecords/edit/<int:pk>/', TreatmentRecordUpdateView.as_view(),
                       name='treatmentrecord_edit'),
                  path('treatmentrecords/delete/<int:pk>/', TreatmentRecordDeleteView.as_view(),
                       name='treatmentrecord_delete'),
                  path('get_treatment_record/', get_treatment_record, name='get_treatment_record'),
                  path('doctors/', DoctorListView.as_view(), name='doctor_list'),
                  path('doctors/new/', DoctorCreateView.as_view(), name='doctor_create'),
                  path('doctors/edit/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_edit'),
                  path('doctors/delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),
                  path('hospital/', HospitalListView.as_view(), name='hospital_list'),
                  path('hospital/new/', HospitalCreateView.as_view(), name='hospital_create'),
                  path('hospital/edit/<int:pk>/', HospitalUpdateView.as_view(), name='hospital_edit'),
                  path('hospital/delete/<int:pk>/', HospitalDeleteView.as_view(), name='hospital_delete'),
                  path('diagnosis/', DiagnosisListView.as_view(), name='diagnosis_list'),
                  path('diagnosis/new/', DiagnosisCreateView.as_view(), name='diagnosis_create'),
                  path('diagnosis/edit/<int:pk>/', DiagnosisUpdateView.as_view(), name='diagnosis_edit'),
                  path('diagnosis/delete/<int:pk>/', DiagnosisDeleteView.as_view(), name='diagnosis_delete'),
                  path('patients/', PatientListView.as_view(), name='patient_list'),
                  path('patients/new/', PatientCreateView.as_view(), name='patient_create'),
                  path('patients/edit/<int:pk>/', PatientUpdateView.as_view(), name='patient_edit'),
                  path('patients/delete/<int:pk>/', PatientDeleteView.as_view(), name='patient_delete'),
                  path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
                  path("dashboard/", dashboardView.as_view(), name="dashboard"),
                  path('update/', DashboardUpdateView.as_view(), name='dashboard_update'),
                  path("", publicView.as_view(), name="public")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
