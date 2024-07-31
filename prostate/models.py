import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models


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
    stadium = models.CharField(max_length=50, verbose_name="Stadium", help_text="Isi dengan TxNxMx", blank=True,
                               null=True)
    grade = models.CharField(max_length=50, verbose_name="Grade",
                             help_text="Isi Gleason Score atau Grading penyakit tsb", blank=True, null=True)
    tumor = models.CharField(max_length=50, verbose_name="Tumor (T)", help_text="Isi dengan Tx", blank=True, null=True)
    nodes = models.CharField(max_length=50, verbose_name="Nodes (N)", help_text="Isi dengan Nx", blank=True, null=True)
    metastasis = models.CharField(max_length=50, verbose_name="Metastasis (M)", help_text="Isi dengan Mx", blank=True,
                                  null=True)
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

    def save(self, *args, **kwargs):
        if self.foto_lab:
            self.foto_lab = self.compress_image(self.foto_lab)
        if self.foto_radiologi:
            self.foto_radiologi = self.compress_image(self.foto_radiologi)
        if self.foto_laporan_operasi:
            self.foto_laporan_operasi = self.compress_image(self.foto_laporan_operasi)
        super().save(*args, **kwargs)

    def compress_image(self, image):
        im = Image.open(image)
        im_io = BytesIO()
        im = im.convert('RGB')
        im.save(im_io, 'JPEG', quality=85)
        new_image = ContentFile(im_io.getvalue(), name=image.name)
        return new_image

    def delete(self, *args, **kwargs):
        fotos = [self.foto_lab, self.foto_radiologi, self.foto_laporan_operasi]
        super().delete(*args, **kwargs)
        for foto in fotos:
            if foto and os.path.isfile(foto.path):
                os.remove(foto.path)
