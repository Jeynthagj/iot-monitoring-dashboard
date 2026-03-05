from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Device

@api_view(['GET', 'POST', 'DELETE'])
def get_devices(request):

    if request.method == 'GET':
        devices = Device.objects.all().values()
        return Response(devices)

    if request.method == 'POST':
        device = Device.objects.create(
            name=request.data.get("name"),
            temperature=request.data.get("temperature"),
            humidity=request.data.get("humidity")
        )
        return Response({"message": "Device created"}, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        device_id = request.data.get("id")
        Device.objects.filter(id=device_id).delete()
        return Response({"message": "Device deleted"}, status=status.HTTP_204_NO_CONTENT)