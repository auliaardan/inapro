from rest_framework import serializers
from .models import TreatmentRecord

class TreatmentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentRecord
        fields = '__all__'