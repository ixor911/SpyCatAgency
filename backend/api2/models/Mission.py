from django.db import models
from rest_framework import serializers, exceptions


class Mission(models.Model):
    is_completed = models.BooleanField(auto_created=True, default=False)

    @property
    def cat(self):
        """
        A way to make some sort of connection Mission -> SpyCat

        :return: SpyCat or None
        """
        from . import SpyCat

        cats = SpyCat.objects.filter(mission=self.id)
        return None if not cats else cats[0]


    @property
    def targets(self):
        """
        A way to make some sort of connection Mission -> Target

        :return: List[Target]
        """
        from . import Target

        targets = Target.objects.filter(mission=self.id)
        return targets


class MissionSerializer(serializers.ModelSerializer):
    targets = serializers.ListField(write_only=True)

    class Meta:
        model = Mission
        fields = '__all__'

    def to_representation(self, instance):
        """
        With mission get info about cat and targets

        :param instance:
        :return: dict
        """
        from . import SpyCatSerializer, TargetSerializer

        return {
            **super().to_representation(instance),
            "targets": TargetSerializer(instance.targets, many=True).data,
            "cat": None if not instance.cat else SpyCatSerializer(instance.cat).data
        }

    def create(self, validated_data):
        """
        While creating Mission, create Targets.
        BUT if at least one target is bad, mission will not be created
        It can be changed easily

        :param validated_data:
        :return: Mission
        """
        from . import TargetSerializer

        targets_data = validated_data.pop('targets')
        mission = super().create(validated_data)

        for target_data in targets_data:
            target_serializer = TargetSerializer(data={
                **target_data,
                "mission": mission.id
            })

            if target_serializer.is_valid():
                target_serializer.save()
            else:
                # Commit next line, if you want mission to be created anyway
                mission.delete()
                raise exceptions.ParseError(target_serializer.errors)

        return mission