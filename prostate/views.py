import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView

from .forms import patientdataForm, DoctorForm, treatmentrecordForm, HospitalForm, DiagnosisForm
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
