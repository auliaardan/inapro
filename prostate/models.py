from django.db import models
from django.db.models import Max


# Register your models here.
class patientdata(models.Model):
    id_number = models.CharField(max_length=20, unique=True, verbose_name="ID Number",
                                 help_text="Nomor Induk Kependudukan / Nomor Rekam Medis")
    name = models.CharField(max_length=100, verbose_name="Patient's Name", help_text="Nama Pasien")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number", help_text="Nomor Telfon")
    date_of_birth = models.DateField(verbose_name="Date Of Birth", help_text="Tanggal Lahir")
    ethnic_group = models.CharField(max_length=50, verbose_name="Ethnic Group", help_text="Suku Bangsa")
    health_insurance = models.CharField(max_length=100, verbose_name="Health Insurance", help_text="Asuransi Kesehatan")
    address = models.CharField(max_length=255, verbose_name="Address", help_text="Alamat")

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    nidn = models.CharField(max_length=100)
    specialty = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Diagnosis(models.Model):
    name = models.CharField(max_length=100)
    icd_code = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class TreatmentRecordManager(models.Manager):
    def get_last_treatment(self, patient):
        return self.filter(patient=patient).order_by('-date_of_treatment').first()


class TreatmentRecord(models.Model):
    patient = models.ForeignKey(patientdata, on_delete=models.CASCADE)
    medical_record = models.CharField(max_length=20, verbose_name="Medical Record Number",
                                      help_text="Nomor Rekam Medis")
    date_of_treatment = models.DateField(verbose_name="Date of Treatment", help_text="Tanggal Pengobatan")
    hospital_name = models.ForeignKey(Hospital, on_delete=models.CASCADE, verbose_name="Hospital Name",
                                      help_text="Nama Rumah Sakit")
    service_unit = models.CharField(max_length=100, verbose_name="Service Unit", help_text="Unit Layanan")
    doctor_name = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=False)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    stadium = models.CharField(max_length=50, verbose_name="Stadium", help_text="Isi dengan TxNxMx", blank=True, null=True)
    grade = models.CharField(max_length=50, verbose_name="Grade", help_text="Isi Gleason Score atau Grading penyakit tsb", blank=True, null=True)
    tumor = models.CharField(max_length=50, verbose_name="Tumor (T)", help_text="Isi dengan Tx", blank=True, null=True)
    nodes = models.CharField(max_length=50, verbose_name="Nodes (N)", help_text="Isi dengan Nx", blank=True, null=True)
    metastasis = models.CharField(max_length=50, verbose_name="Metastasis (M)", help_text="Isi dengan Mx", blank=True, null=True)
    bone_scan = models.TextField(max_length=100, verbose_name="Bone Scan", help_text="", blank=True)
    pet_scan = models.TextField(max_length=100, verbose_name="Pet Scan", help_text="", blank=True)
    psma_pet_ct = models.TextField(max_length=100, verbose_name="PSMA PET/CT", help_text="", blank=True)
    choline_pet_ct = models.TextField(max_length=100, verbose_name="Choline PET/CT", help_text="", blank=True)
    fluoride_pet = models.TextField(max_length=100, verbose_name="Fluoride PET", help_text="", blank=True)
    foto_lab = models.ImageField(upload_to='lab_photos/', verbose_name="Foto Lab", blank=True, null=True)
    foto_radiologi = models.ImageField(upload_to='radiologi_photos/', verbose_name="Foto Radiologi", blank=True,
                                       null=True)
    foto_laporan_operasi = models.ImageField(upload_to='laporan_operasi_photos/', verbose_name="Foto Laporan Operasi",
                                             blank=True, null=True)
    treatment = models.TextField(verbose_name="Tindakan/Terapi", help_text="", blank=True)
    incontinence = models.BooleanField(default=False)
    pad_usage = models.CharField(max_length=100, blank=True, null=True)
    erectile_dysfunction = models.BooleanField(default=False)
    side_effects = models.TextField(blank=True, null=True)
    ipss = models.CharField(max_length=100, blank=True, null=True)
    iief = models.CharField(max_length=100, blank=True, null=True)
    subjective = models.TextField(blank=True, null=True)
    objective = models.TextField(blank=True, null=True)
    assessment = models.TextField(blank=True, null=True)
    plan = models.TextField(blank=True, null=True)

    objects = TreatmentRecordManager()

    def __str__(self):
        return f"Treatment Record for {self.patient.name} on {self.date_of_treatment}"


class SurveySet(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, default="Survey")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SurveyQuestion(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text Input'),
        ('radio', 'Radio Button'),
        ('checkbox', 'Checkbox'),
        ('textarea', 'Text Area'),
    ]

    survey_set = models.ForeignKey(SurveySet, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(blank=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)

    def __str__(self):
        return self.title


class SurveyOption(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.option_text


class SurveyResponse(models.Model):
    survey_set = models.ForeignKey(SurveySet, on_delete=models.CASCADE, related_name='responses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.survey_set.name} at {self.created_at}"


class SurveyAnswer(models.Model):
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Answer to {self.question.title}"
