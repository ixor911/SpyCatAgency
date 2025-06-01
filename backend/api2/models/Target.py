from django.db import models
from rest_framework import serializers, exceptions

from . import Mission


class Target(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    notes = models.TextField(default="", blank=True)
    is_complete = models.BooleanField(default=False)

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = '__all__'


    def update(self, instance, validated_data):
        """ Target can not be changed when it or the mission is already completed """

        if instance.is_complete:
            raise exceptions.PermissionDenied("Target is completed, you can not change it")
        elif instance.mission.is_completed:
            raise exceptions.PermissionDenied("Mission is completed, you can not change the target")

        return super().update(instance, validated_data)