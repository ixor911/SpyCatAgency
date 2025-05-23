from rest_framework import viewsets, exceptions
from rest_framework.response import Response

from ..models import SpyCat, SpyCatSerializer, breeds


class SpyCatView(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


    def update(self, request, *args, **kwargs):
        cat = SpyCat.objects.get(id=kwargs.get('pk'))
        cat_serializer = SpyCatSerializer(
            instance=cat,
            data={
                **SpyCatSerializer(instance=cat).data,
                "salary": request.data.get('salary')
            }
        )

        if cat_serializer.is_valid():
            cat_serializer.save()
            return Response(cat_serializer.data, status=exceptions.status.HTTP_202_ACCEPTED)

        return Response(cat_serializer.errors, status=exceptions.status.HTTP_400_BAD_REQUEST)