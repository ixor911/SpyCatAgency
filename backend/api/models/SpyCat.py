from django.db import models
from rest_framework import serializers


class SpyCat(models.Model):
    name = models.CharField(max_length=50)
    experience = models.PositiveIntegerField()
    salary = models.FloatField()
    breed = models.JSONField()




class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'