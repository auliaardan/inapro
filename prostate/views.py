import json
from datetime import timedelta

import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView

from .forms import patientdataForm, DoctorForm, treatmentrecordForm, HospitalForm, DiagnosisForm, UploadFileForm, \
    ExportDataForm
from .models import patientdata, Hospital, TreatmentRecord, Doctor, Diagnosis


# Create your views here.

class publicView(TemplateView):
    template_name = 'index2.html'


class dashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        total_patients = patientdata.objects.count()
        total_hospital = Hospital.objects.count()
        total_doctor = Doctor.objects.count()
        total_emr = TreatmentRecord.objects.count()

        one_year_ago = now() - timedelta(days=365)

        # Data for patient intake chart (monthly data)
        patient_intake_monthly = TreatmentRecord.objects.filter(
            date_of_treatment__gte=one_year_ago
        ).annotate(month=TruncMonth('date_of_treatment')).values(
            'month'
        ).annotate(count=Count('id')).order_by('month')

        # Preparing data for JavaScript
        patient_intake_data = {
            'labels': [data['month'].strftime('%B %Y') for data in patient_intake_monthly],
            'counts': [data['count'] for data in patient_intake_monthly],
        }

        # Data for common diagnoses (top 5)
        common_diagnoses = TreatmentRecord.objects.values('diagnosis').annotate(count=Count('diagnosis')).order_by(
            '-count')[:5]

        data = {
            'total_patients': total_patients,
            'total_hospitals': total_hospital,
            'total_doctors': total_doctor,
            'total_emr': total_emr,
            'patient_intake_data': json.dumps(patient_intake_data, cls=DjangoJSONEncoder),
            'common_diagnoses': list(common_diagnoses),
        }

        return render(request, 'Dashboard.html', data)


class DashboardUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        total_patients = patientdata.objects.count()
        total_hospital = Hospital.objects.count()
        total_emr = TreatmentRecord.objects.count()
        total_doctor = Doctor.objects.count()

        one_year_ago = now() - timedelta(days=365)

        # Data for patient intake chart (monthly data)
        patient_intake_monthly = TreatmentRecord.objects.filter(
            date_of_treatment__gte=one_year_ago
        ).annotate(month=TruncMonth('date_of_treatment')).values(
            'month'
        ).annotate(count=Count('id')).order_by('month')

        # Preparing data for JavaScript
        patient_intake_data = {
            'labels': [data['month'].strftime('%B %Y') for data in patient_intake_monthly],
            'counts': [data['count'] for data in patient_intake_monthly],
        }

        data = {
            'total_patients': total_patients,
            'total_hospitals': total_hospital,
            'total_doctors': total_doctor,
            'patient_intake_data': json.dumps(patient_intake_data, cls=DjangoJSONEncoder),
            'total_emr': total_emr,
        }

        return JsonResponse(data)


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = patientdata
    form_class = patientdataForm
    template_name = 'medicalrecord/patient_form.html'
    success_url = reverse_lazy('patient_list')


class PatientListView(LoginRequiredMixin, ListView):
    model = patientdata
    template_name = 'medicalrecord/patient_list.html'
    context_object_name = 'patient_list'


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = patientdata
    form_class = patientdataForm
    template_name = 'medicalrecord/patient_form.html'
    success_url = reverse_lazy('patient_list')


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = patientdata
    template_name = 'medicalrecord/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'medicalrecord/doctor_list.html'
    context_object_name = 'doctor_list'


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'medicalrecord/doctor_form.html'
    success_url = reverse_lazy('doctor_list')


class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'medicalrecord/doctor_form.html'
    success_url = reverse_lazy('doctor_list')


class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'medicalrecord/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')


class HospitalListView(LoginRequiredMixin, ListView):
    model = Hospital
    template_name = 'medicalrecord/hospital_list.html'
    context_object_name = 'hospital_list'


class HospitalCreateView(LoginRequiredMixin, CreateView):
    model = Hospital
    form_class = HospitalForm
    template_name = 'medicalrecord/hospital_form.html'
    success_url = reverse_lazy('hospital_list')


class HospitalUpdateView(LoginRequiredMixin, UpdateView):
    model = Hospital
    form_class = HospitalForm
    template_name = 'medicalrecord/hospital_form.html'
    success_url = reverse_lazy('hospital_list')


class HospitalDeleteView(LoginRequiredMixin, DeleteView):
    model = Hospital
    template_name = 'medicalrecord/hospital_confirm_delete.html'
    success_url = reverse_lazy('hospital_list')


class DiagnosisListView(LoginRequiredMixin, ListView):
    model = Diagnosis
    template_name = 'medicalrecord/diagnosis_list.html'
    context_object_name = 'diagnosis_list'


class DiagnosisCreateView(LoginRequiredMixin, CreateView):
    model = Diagnosis
    form_class = DiagnosisForm
    template_name = 'medicalrecord/diagnosis_form.html'
    success_url = reverse_lazy('diagnosis_list')


class DiagnosisUpdateView(LoginRequiredMixin, UpdateView):
    model = Diagnosis
    form_class = DiagnosisForm
    template_name = 'medicalrecord/diagnosis_form.html'
    success_url = reverse_lazy('diagnosis_list')


class DiagnosisDeleteView(LoginRequiredMixin, DeleteView):
    model = Diagnosis
    template_name = 'medicalrecord/diagnosis_confirm_delete.html'
    success_url = reverse_lazy('diagnosis_list')


class TreatmentRecordListView(LoginRequiredMixin, ListView):
    model = patientdata
    template_name = 'medicalrecord/treatmentrecord_list.html'
    context_object_name = 'patients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patients = context['patients']
        patient_last_treatments = []
        for patient in patients:
            last_treatment = TreatmentRecord.objects.get_last_treatment(patient)
            patient_last_treatments.append({
                'patient': patient,
                'last_treatment': last_treatment
            })
        context['patient_last_treatments'] = patient_last_treatments
        return context


class TreatmentRecordCreateView(LoginRequiredMixin, CreateView):
    model = TreatmentRecord
    form_class = treatmentrecordForm
    template_name = 'medicalrecord/treatmentrecord_form.html'

    def get_success_url(self):
        return reverse('patient_detail', kwargs={'pk': self.kwargs['patient_id']})

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.kwargs.get('patient_id')
        patient = get_object_or_404(patientdata, pk=patient_id)
        initial['patient'] = patient
        return initial

    def form_valid(self, form):
        form.instance.patient = get_object_or_404(patientdata, pk=self.kwargs.get('patient_id'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(patientdata, pk=self.kwargs['patient_id'])
        return context


class TreatmentRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = TreatmentRecord
    form_class = treatmentrecordForm
    template_name = 'medicalrecord/treatmentrecord_form.html'

    def get_success_url(self):
        return reverse('patient_detail', kwargs={'pk': self.object.patient.pk})


class TreatmentRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = TreatmentRecord
    template_name = 'medicalrecord/treatmentrecord_confirm_delete.html'
    success_url = reverse_lazy('treatmentrecord_list')


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = patientdata
    template_name = 'medicalrecord/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        treatment_records = TreatmentRecord.objects.filter(
            patient=patient
        ).exclude(
            treatment__isnull=True
        ).exclude(
            treatment__exact=''
        ).order_by('-date_of_treatment')
        context['date_of_treatments'] = TreatmentRecord.objects.filter(patient=patient).order_by('-date_of_treatment')
        context['treatment_records'] = treatment_records
        context['latest_record'] = treatment_records.first() if treatment_records.exists() else None
        return context


@login_required
def get_treatment_record(request):
    record_id = request.GET.get('id')
    record = TreatmentRecord.objects.get(id=record_id)
    data = {
        'treatment_details': render_to_string('medicalrecord/treatment_details.html', {'record': record})
    }
    return JsonResponse(data)


@login_required
def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["file"]

            try:
                # Read the Excel file using pandas
                df = pd.read_excel(excel_file)

                # Replace NaN values with empty strings
                df = df.fillna('')

                # Iterate through the rows and create TreatmentRecord objects
                for index, row in df.iterrows():
                    try:
                        # Skip empty rows
                        if row.isnull().all():
                            continue

                        # Handle patient data
                        patient_id_number = row.get('patient_id_number')
                        patient_name = row.get('patient_name')
                        patient_phone_number = row.get('patient_phone_number')
                        patient_date_of_birth = row.get('patient_date_of_birth')
                        patient_ethnic_group = row.get('patient_ethnic_group')
                        patient_health_insurance = row.get('patient_health_insurance')
                        patient_address = row.get('patient_address')

                        if patient_id_number:
                            patient, created = patientdata.objects.get_or_create(
                                id_number=patient_id_number,
                                defaults={
                                    'name': patient_name,
                                    'phone_number': patient_phone_number,
                                    'date_of_birth': patient_date_of_birth,
                                    'ethnic_group': patient_ethnic_group,
                                    'health_insurance': patient_health_insurance,
                                    'address': patient_address,
                                }
                            )
                        else:
                            patient, created = patientdata.objects.get_or_create(
                                name=patient_name,
                                defaults={
                                    'phone_number': patient_phone_number,
                                    'date_of_birth': patient_date_of_birth,
                                    'ethnic_group': patient_ethnic_group,
                                    'health_insurance': patient_health_insurance,
                                    'address': patient_address,
                                }
                            )

                        # Handle hospital foreign key
                        hospital_name = row.get('hospital_name')
                        if hospital_name:
                            hospital = get_object_or_404(Hospital, name=hospital_name)
                        else:
                            hospital = None

                        # Handle doctor foreign key
                        doctor_id = row.get('doctor_id')
                        doctor_name = row.get('doctor_name')
                        if doctor_id:
                            doctor = get_object_or_404(Doctor, pk=doctor_id)
                        elif doctor_name:
                            doctor = get_object_or_404(Doctor, name=doctor_name)
                        else:
                            doctor = None

                        # Handle diagnosis foreign key
                        diagnosis_name = row.get('diagnosis')
                        if diagnosis_name:
                            diagnosis = get_object_or_404(Diagnosis, name=diagnosis_name)
                        else:
                            diagnosis = None

                        # Create TreatmentRecord
                        TreatmentRecord.objects.create(
                            patient=patient,
                            medical_record=row.get('medical_record', ''),
                            date_of_treatment=row.get('date_of_treatment', None),
                            hospital_name=hospital,
                            service_unit=row.get('service_unit', ''),
                            doctor_name=doctor,
                            diagnosis=diagnosis,
                            stadium=row.get('stadium', ''),
                            grade=row.get('grade', ''),
                            tumor=row.get('tumor', ''),
                            nodes=row.get('nodes', ''),
                            metastasis=row.get('metastasis', ''),
                            bone_scan=row.get('bone_scan', ''),
                            pet_scan=row.get('pet_scan', ''),
                            psma_pet_ct=row.get('psma_pet_ct', ''),
                            choline_pet_ct=row.get('choline_pet_ct', ''),
                            fluoride_pet=row.get('fluoride_pet', ''),
                            treatment=row.get('treatment', ''),
                            incontinence=row.get('incontinence', False),
                            pad_usage=row.get('pad_usage', ''),
                            erectile_dysfunction=row.get('erectile_dysfunction', False),
                            side_effects=row.get('side_effects', ''),
                            subjective=row.get('subjective', ''),
                            objective=row.get('objective', ''),
                            assessment=row.get('assessment', ''),
                            plan=row.get('plan', ''),
                        )
                    except Exception as e:
                        messages.error(request, f"Error processing row {index + 1}: {e}")
                        continue

                messages.success(request, "Data imported successfully!")
            except Exception as e:
                messages.error(request, f"Error reading the Excel file: {e}")

            return redirect("import_data")

    else:
        form = UploadFileForm()
    return render(request, "medicalrecord/import_data.html", {"form": form})


@login_required
def export_data(request):
    if request.method == "POST":
        form = ExportDataForm(request.POST)
        if form.is_valid():
            export_all = form.cleaned_data['export_all']
            hospital = form.cleaned_data['hospital'] if not export_all else None
            doctor = form.cleaned_data['doctor'] if not export_all else None
            diagnosis = form.cleaned_data['diagnosis'] if not export_all else None
            treatment = form.cleaned_data['treatment'] if not export_all else ""

            queryset = TreatmentRecord.objects.all()

            if not export_all:
                if hospital:
                    queryset = queryset.filter(hospital_name=hospital)
                if doctor:
                    queryset = queryset.filter(doctor_name=doctor)
                if diagnosis:
                    queryset = queryset.filter(diagnosis=diagnosis)
                if treatment:
                    queryset = queryset.filter(treatment__icontains=treatment)

            data = []
            for record in queryset:
                data.append({
                    'patient_id_number': record.patient.id_number,
                    'patient_name': record.patient.name,
                    'patient_phone_number': record.patient.phone_number,
                    'patient_date_of_birth': record.patient.date_of_birth,
                    'patient_ethnic_group': record.patient.ethnic_group,
                    'patient_health_insurance': record.patient.health_insurance,
                    'patient_address': record.patient.address,
                    'medical_record': record.medical_record,
                    'date_of_treatment': record.date_of_treatment,
                    'hospital_name': record.hospital_name.name if record.hospital_name else '',
                    'service_unit': record.service_unit,
                    'doctor_name': record.doctor_name.name if record.doctor_name else '',
                    'diagnosis': record.diagnosis.name if record.diagnosis else '',
                    'stadium': record.stadium,
                    'grade': record.grade,
                    'tumor': record.tumor,
                    'nodes': record.nodes,
                    'metastasis': record.metastasis,
                    'bone_scan': record.bone_scan,
                    'pet_scan': record.pet_scan,
                    'psma_pet_ct': record.psma_pet_ct,
                    'choline_pet_ct': record.choline_pet_ct,
                    'fluoride_pet': record.fluoride_pet,
                    'treatment': record.treatment,
                    'incontinence': record.incontinence,
                    'pad_usage': record.pad_usage,
                    'erectile_dysfunction': record.erectile_dysfunction,
                    'side_effects': record.side_effects,
                    'subjective': record.subjective,
                    'objective': record.objective,
                    'assessment': record.assessment,
                    'plan': record.plan,
                })

            df = pd.DataFrame(data)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=treatment_records.xlsx'
            df.to_excel(response, index=False)

            return response
    else:
        form = ExportDataForm()

    return render(request, "export_data.html", {"form": form})
