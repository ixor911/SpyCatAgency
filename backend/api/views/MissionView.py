from rest_framework import viewsets, response, exceptions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ..models import Mission, MissionSerializer


class MissionView(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer


    def get_mission_targets(self, mission_id):
        from ..models import Target, TargetSerializer

        return TargetSerializer(Target.objects.filter(mission=mission_id), many=True).data


    def get_mission_cat(self, mission_id):
        from ..models import SpyCat, SpyCatSerializer

        cats = SpyCat.objects.filter(mission=mission_id)
        return SpyCatSerializer(cats[0]).data if cats else None


    def delete_mission_cat(self, mission_id):
        from ..models import SpyCat, SpyCatSerializer

        cats = SpyCat.objects.filter(mission=mission_id)
        if cats:
            cats[0].mission = None
            cats[0].save()


    def retrieve(self, request, *args, **kwargs):
        mission_data = super().retrieve(request, *args, **kwargs).data
        targets_data = self.get_mission_targets(mission_data.get("id"))
        cat_data = self.get_mission_cat(mission_data.get('id'))


        return response.Response(
            data={
                **mission_data,
                "cat": cat_data,
                "targets": targets_data
            }
        )


    def list(self, request, *args, **kwargs):
        missions = Mission.objects.all()

        missions_data = []
        for mission in missions:
            missions_data.append({
                **MissionSerializer(mission).data,
                "cat": self.get_mission_cat(mission.id),
                "targets": self.get_mission_targets(mission.id)
            })

        return Response(
            missions_data,
            status=exceptions.status.HTTP_200_OK
        )


    def destroy(self, request, *args, **kwargs):
        mission = get_object_or_404(Mission, id=kwargs.get('pk'))

        if mission.cat:
            return Response(
                    exceptions.PermissionDenied("Mission is already given to the cat").detail,
                status=exceptions.status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)


    @action(detail=True, methods=['put'])
    def complete(self, request, pk, *args, **kwargs):
        mission = get_object_or_404(Mission, id=pk)

        if mission.is_completed:
            return Response(
                exceptions.PermissionDenied("mission is already completed").detail,
                status=exceptions.status.HTTP_403_FORBIDDEN
            )

        mission.is_completed = True
        mission.save()

        self.delete_mission_cat(mission.id)

        return self.retrieve(request, pk, *args, **kwargs)