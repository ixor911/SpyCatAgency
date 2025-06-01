from rest_framework import viewsets, generics, response, exceptions
from rest_framework.decorators import action

from ..models import SpyCat, SpyCatSerializer, Mission, MissionSerializer


class SpyCatView(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


    @action(detail=True, methods=["put"])
    def mission(self, request, pk):
        """
        Assign current SpyCat to the Mission

        You should have 'mission' field with id in request body
        """

        cat = generics.get_object_or_404(SpyCat, id=pk)
        mission = generics.get_object_or_404(Mission, id=request.data.get('mission'))

        cat.mission = mission
        cat.save()

        return response.Response(SpyCatSerializer(cat).data)

    @mission.mapping.get
    def get_mission(self, request, pk):
        """ Get Mission of current Cat or None """

        cat = generics.get_object_or_404(SpyCat, id=pk)

        return response.Response() if not cat.mission else response.Response(MissionSerializer(cat.mission).data)

    @mission.mapping.delete
    def delete_mission(self, request, pk):
        """ Delete Mission from current SpyCat """

        cat = generics.get_object_or_404(SpyCat, id=pk)
        cat.mission = None
        cat.save()

        return response.Response(SpyCatSerializer(cat).data)