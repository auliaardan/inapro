from django import forms

from .models import patientdata, TreatmentRecord, Doctor, Diagnosis, Hospital


class patientdataForm(forms.ModelForm):
    class Meta:
        model = patientdata
        fields = '__all__'


class treatmentrecordForm(forms.ModelForm):
    date_of_treatment = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD'
        })
    )

    class Meta:
        model = TreatmentRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(treatmentrecordForm, self).__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs['readonly'] = True


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ExportDataForm(forms.Form):
    export_all = forms.BooleanField(required=False, initial=False, label="Export All Data")
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=False, label="Hospital")
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=False, label="Doctor")
    diagnosis = forms.ModelChoiceField(queryset=Diagnosis.objects.all(), required=False, label="Diagnosis")
    treatment = forms.CharField(required=False, label="Treatment")
