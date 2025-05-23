from rest_framework import viewsets, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime

from ..models import Target, TargetSerializer


class TargetView(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


    def is_completed_check(self, target):
        if target.is_complete:
            return Response(
                exceptions.PermissionDenied("Target is already completed").detail,
                status=exceptions.status.HTTP_403_FORBIDDEN
            )
        elif target.mission.is_completed:
            return Response(
                exceptions.PermissionDenied("Target is already completed").detail,
                status=exceptions.status.HTTP_403_FORBIDDEN
            )


    @action(detail=True, methods=['put'])
    def complete(self, request, pk, *args, **kwargs):
        target = get_object_or_404(Target, id=pk)

        is_completed = self.is_completed_check(target)
        if is_completed:
            return is_completed

        target.is_complete = True
        target.save()

        return Response(
            TargetSerializer(instance=target).data,
            status=exceptions.status.HTTP_200_OK
        )


    @action(detail=True, methods=['put'])
    def add_note(self, request, pk, *args, **kwargs):
        target = get_object_or_404(Target, id=pk)

        is_completed = self.is_completed_check(target)
        if is_completed:
            return is_completed

        elif 'notes' not in request.data:
            return Response(
                exceptions.ParseError("Notes are empty").detail,
                status=exceptions.status.HTTP_400_BAD_REQUEST
            )

        target.notes += (
            "\n\n"
            f"{datetime.datetime.now()}\n"
            f"{request.data.get('notes')}"
        )
        target.save()

        return Response(
            TargetSerializer(instance=target).data,
            status=exceptions.status.HTTP_200_OK
        )





