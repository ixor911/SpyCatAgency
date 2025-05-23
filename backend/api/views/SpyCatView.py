from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ..models import SpyCat, SpyCatSerializer, breeds, Mission


class SpyCatView(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


    def update(self, request, *args, **kwargs):
        cat = get_object_or_404(SpyCat, id=kwargs.get('pk'))
        cat_serializer = SpyCatSerializer(instance=cat, data={
                **SpyCatSerializer(instance=cat).data,
                "salary": request.data.get('salary')
            }
        )

        if cat_serializer.is_valid():
            cat_serializer.save()
            return Response(cat_serializer.data, status=exceptions.status.HTTP_202_ACCEPTED)

        return Response(cat_serializer.errors, status=exceptions.status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def give_mission(self, request, pk, *args, **kwargs):
        cat = get_object_or_404(SpyCat, id=pk)
        mission = get_object_or_404(Mission, id=request.data.get('mission'))

        if cat.mission:
            return Response(
                exceptions.PermissionDenied("Cat already has a mission").detail,
                status=exceptions.status.HTTP_403_FORBIDDEN
            )
        elif mission.cat:
            return Response(
                exceptions.PermissionDenied("Mission already has a cat").detail,
                status=exceptions.status.HTTP_403_FORBIDDEN
            )
        elif mission.is_completed:
            return Response(
                exceptions.PermissionDenied("Mission already completed").detail,
                status=exceptions.status.HTTP_403_FORBIDDEN
            )

        cat.mission = mission
        cat.save()

        return Response(
            SpyCatSerializer(instance=cat).data,
            status=exceptions.status.HTTP_200_OK
        )
