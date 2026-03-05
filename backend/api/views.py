from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Device, DeviceReading


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

        DeviceReading.objects.create(
            device=device,
            temperature=device.temperature,
            humidity=device.humidity
        )

        return Response({"message": "Device created"}, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        device_id = request.data.get("id")
        Device.objects.filter(id=device_id).delete()
        return Response({"message": "Device deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def device_history(request, device_id):

    readings = DeviceReading.objects.filter(device_id=device_id).order_by('-timestamp')[:20]

    data = [
        {
            "temperature": r.temperature,
            "humidity": r.humidity,
            "timestamp": r.timestamp
        }
        for r in readings
    ]

    return Response(data)