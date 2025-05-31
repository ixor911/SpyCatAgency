from rest_framework import viewsets, response, exceptions, generics
from rest_framework.decorators import action

from ..models import Mission, MissionSerializer, SpyCat, SpyCatSerializer, TargetSerializer


class MissionView(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = generics.get_object_or_404(Mission, id=kwargs.get('pk'))

        if mission.cat:
            return response.Response(
                f"Cat {mission.cat.name} is on this mission, you can not delete it",
                status=exceptions.status.HTTP_403_FORBIDDEN
            )

        mission.delete()

        return response.Response()


    @action(detail=True, methods=["put"])
    def cat(self, request, pk):
        mission = generics.get_object_or_404(Mission, id=pk)
        cat = generics.get_object_or_404(SpyCat, id=request.data.get('cat'))

        if mission.is_completed:
            return response.Response(
                f"Mission is already completed",
                status=exceptions.status.HTTP_403_FORBIDDEN
            )
        elif cat.mission and cat.mission != mission:
            return response.Response(
                    f"Cat {cat.name} already has a mission",
                    status=exceptions.status.HTTP_403_FORBIDDEN
                )


        self.delete_cat(request, pk)
        cat.mission = mission
        cat.save()

        return response.Response(MissionSerializer(mission).data)

    @cat.mapping.delete
    def delete_cat(self, request, pk):
        mission = generics.get_object_or_404(Mission, id=pk)

        if mission.cat:
            cat = mission.cat
            cat.mission = None
            cat.save()

        return response.Response(MissionSerializer(mission).data)

    @cat.mapping.get
    def get_cat(self, request, pk):
        mission = generics.get_object_or_404(Mission, id=pk)

        resp = response.Response() if not mission.cat else response.Response(SpyCatSerializer(mission.cat).data)
        return resp

    @action(detail=True, methods=["get"])
    def targets(self, request, pk):
        mission = generics.get_object_or_404(Mission, id=pk)
        return response.Response(TargetSerializer(mission.targets, many=True).data)

    @action(detail=True, methods=["put"])
    def complete(self, request, pk):
        mission = generics.get_object_or_404(Mission, id=pk)
        mission.is_completed = True
        mission.save()

        self.delete_cat(request, pk)

        return response.Response("Mission is completed!")


