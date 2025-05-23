from django.db import models
from rest_framework import serializers, exceptions


class Target(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    notes = models.TextField(default="", blank=True)
    is_complete = models.BooleanField(default=False)



class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = '__all__'

    def update(self, instance, validated_data):
        if instance.is_complete:
            raise exceptions.PermissionDenied("Target is complete")
        
        return super().update(instance, validated_data)