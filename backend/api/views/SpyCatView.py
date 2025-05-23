from rest_framework import viewsets

from ..models import SpyCat, SpyCatSerializer


class SpyCatView(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer