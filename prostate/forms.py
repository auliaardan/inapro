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
