from django.db import models
from rest_framework import serializers, exceptions

from . import breeds, Mission


class SpyCat(models.Model):
    name = models.CharField(max_length=50)
    experience = models.PositiveIntegerField(default=0)
    salary = models.FloatField()
    breed = models.JSONField()

    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, default=None, null=True)


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'


    def get_breed(self, breed):
        """
        Try to find the breed by id or the instance, otherwise raise error

        :param breed:
        :return: breed
        """
        check_data = breeds.values() if isinstance(breed, dict) else breeds.keys()

        if breed not in check_data:
            raise exceptions.ParseError("Breed is not found")

        return breeds.get(breed) if isinstance(breed, str) else breed


    def create(self, validated_data):
        """ Validate breed while creating"""

        return super().create({
            **validated_data,
            "breed": self.get_breed(validated_data.get('breed'))
        })

    def update(self, instance, validated_data):
        """ Validate breed while updating"""

        return super().update(instance, {
            **validated_data,
            "breed": self.get_breed(validated_data.get('breed'))
        })