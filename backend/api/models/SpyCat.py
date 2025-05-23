from django.db import models
from rest_framework import serializers, exceptions
from . import breeds


class SpyCat(models.Model):
    name = models.CharField(max_length=50)
    experience = models.PositiveIntegerField()
    salary = models.FloatField()
    breed = models.JSONField()




class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'


    def breed_validate(self, breed):
        if isinstance(breed, str):
            if breed in breeds.keys():
                return breeds.get(breed)
            else:
                raise exceptions.NotFound("Breed is not found")

        elif isinstance(breed, dict):
            if breed in breeds.values():
                return breed
            else:
                raise exceptions.NotFound("Breed is not found")

        raise exceptions.NotAcceptable("Breed format is not acceptable")


    def create(self, validated_data):
        validated_data['breed'] = self.breed_validate(validated_data.get('breed'))

        return super().create(validated_data)


