from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from room.serializers import AvailabilitiesListSerializer
from room.utils import availabilities


class AvailabilityMixin(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        data = availabilities(request, obj=self.get_object())
        return Response(AvailabilitiesListSerializer(data, many=True).data, status=200)
