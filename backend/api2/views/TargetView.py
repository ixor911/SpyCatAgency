from rest_framework import viewsets, response, exceptions, generics
from rest_framework.decorators import action
import datetime

from ..models import Target, TargetSerializer, MissionSerializer


class TargetView(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def check(self, request, target):
        """
        Just a checkup function to separate one function into 2

        Error is given:
        - Mission is completed,
        - Mission without SpyCat
        - "notes" field in request body is empty
        """

        if target.mission.is_completed:
            return response.Response(
                "Mission is already completed",
                status=exceptions.status.HTTP_403_FORBIDDEN
            )
        elif not target.mission.cat:
            return response.Response(
                "This mission without SpyCat",
                status=exceptions.status.HTTP_403_FORBIDDEN
            )
        elif "notes" not in request.data:
            return response.Response(
                "<note> field not in request body",
                status=exceptions.status.HTTP_400_BAD_REQUEST
            )
        elif request.data.get('notes') == "":
            return response.Response(
                "<note> field can not be blank",
                status=exceptions.status.HTTP_400_BAD_REQUEST
            )


    @action(detail=True, methods=["put"])
    def add_note(self, request, pk):
        """ Add note to the target with some conditions from top """

        target = generics.get_object_or_404(Target, id=pk)

        check_res = self.check(request, target)
        if check_res:
            return check_res

        target_serializer = TargetSerializer(target)
        target_serializer.update(target, {
            "notes": target.notes + (
                f"\n\n"
                f"{datetime.datetime.now()}\n"
                f"{request.data.get('notes')}"
            )
        })

        return response.Response(target_serializer.data)

    @action(detail=True, methods=["put"])
    def complete(self, request, pk):
        """ Mark Target as completed """

        target = generics.get_object_or_404(Target, id=pk)
        target.is_complete = True
        target.save()

        return response.Response("Target is completed!")

    @action(detail=True, methods=["get"])
    def mission(self, request, pk):
        """ Get Mission data from current Target """

        target = generics.get_object_or_404(Target, id=pk)
        return response.Response(MissionSerializer(target.mission).data)