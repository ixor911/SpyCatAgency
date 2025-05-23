from django.db import models
from rest_framework import serializers, exceptions


class Mission(models.Model):
    is_completed = models.BooleanField(default=False)


    @property
    def cat(self):
        from . import SpyCat

        cats = SpyCat.objects.filter(mission=self.id)
        return cats[0] if cats else None


class MissionSerializer(serializers.ModelSerializer):
    cat = serializers.JSONField(default=None, read_only=True)
    targets = serializers.JSONField(default=list)

    class Meta:
        model = Mission
        fields = '__all__'


    def create(self, validated_data):
        from . import TargetSerializer
        targets_data = validated_data.pop('targets')
        targets = []

        mission = super().create(validated_data)

        for target in targets_data:
            target_serializer = TargetSerializer(data={
                **target,
                "mission": mission.id
            })

            if target_serializer.is_valid():
                target_serializer.save()
                targets.append(target_serializer.data)

            else:
                mission.delete()
                raise exceptions.ParseError(target_serializer.errors)

        return {
            **MissionSerializer(instance=mission).data,
            "targets": targets
        }

    def update(self, instance, validated_data):
        if instance.is_completed:
            raise exceptions.PermissionDenied("Mission is complete")
        
        return super().update(instance, validated_data)
