from rest_framework.decorators import api_view, authentication_classes
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Device, DeviceReading, Zone
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

def send_telegram_alert(device, temp):
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print(f"Skipping Telegram alert for {device.name} (Not Configured)")
        return
        
    warning = ""
    if temp > device.max_temp:
        warning = f"HIGH TEMP ALERT 🚨\nDevice {device.name} reading {temp}°C (Max allowed: {device.max_temp}°C)"
    elif temp < device.min_temp:
        warning = f"LOW TEMP ALERT ❄️\nDevice {device.name} reading {temp}°C (Min allowed: {device.min_temp}°C)"
    
    if warning:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {"chat_id": TELEGRAM_CHAT_ID, "text": warning}
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"Failed to send Telegram alert: {e}")


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def get_zones(request):
    if request.method == 'GET':
        zones = Zone.objects.all().values()
        return Response(zones)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        zone = Zone.objects.create(
            name=request.data.get("name"),
            description=request.data.get("description", "")
        )
        return Response({"message": "Zone created", "id": zone.id}, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        zone_id = request.data.get("id")
        Zone.objects.filter(id=zone_id).delete()
        return Response({"message": "Zone deleted"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def get_devices(request):

    if request.method == 'GET':
        # Retrieve all devices with zone_id and thresholds
        devices = Device.objects.all().values(
            'id', 'name', 'temperature', 'humidity', 'created_at', 
            'zone_id', 'min_temp', 'max_temp'
        )
        return Response(devices)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        device = Device.objects.create(
            name=request.data.get("name"),
            temperature=request.data.get("temperature"),
            humidity=request.data.get("humidity"),
            zone_id=request.data.get("zone_id"),
            min_temp=request.data.get("min_temp", 0.0),
            max_temp=request.data.get("max_temp", 50.0)
        )

        DeviceReading.objects.create(
            device=device,
            temperature=device.temperature,
            humidity=device.humidity
        )
        
        # Phase 12 Telegram Check
        if device.temperature > device.max_temp or device.temperature < device.min_temp:
            send_telegram_alert(device, device.temperature)
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'dashboard',
            {
                'type': 'device_update',
                'message': 'created'
            }
        )

        return Response({"message": "Device created"}, status=status.HTTP_201_CREATED)

    if request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        device_id = request.data.get("id")
        try:
            device = Device.objects.get(id=device_id)
            device.name = request.data.get("name", device.name)
            device.temperature = request.data.get("temperature", device.temperature)
            device.humidity = request.data.get("humidity", device.humidity)
            device.zone_id = request.data.get("zone_id", device.zone_id)
            device.min_temp = request.data.get("min_temp", device.min_temp)
            device.max_temp = request.data.get("max_temp", device.max_temp)
            device.save()
            
            DeviceReading.objects.create(
                device=device,
                temperature=device.temperature,
                humidity=device.humidity
            )
            
            # Phase 12 Telegram Check
            if device.temperature > device.max_temp or device.temperature < device.min_temp:
                send_telegram_alert(device, device.temperature)
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'dashboard',
                {
                    'type': 'device_update',
                    'message': 'updated'
                }
            )
            
            return Response({"message": "Device updated"}, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        device_id = request.data.get("id")
        Device.objects.filter(id=device_id).delete()
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'dashboard',
            {
                'type': 'device_update',
                'message': 'deleted'
            }
        )
        
        return Response({"message": "Device deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def device_history(request, device_id):
    limit = int(request.GET.get('limit', 20))
    page_number = int(request.GET.get('page', 1))

    # Fetch all readings, ordered by newest first
    readings_query = DeviceReading.objects.filter(device_id=device_id).order_by('-timestamp')
    
    # Paginate
    paginator = Paginator(readings_query, limit)
    page_obj = paginator.get_page(page_number)

    data = [
        {
            "temperature": r.temperature,
            "humidity": r.humidity,
            "timestamp": r.timestamp
        }
        for r in page_obj
    ]

    return Response({
        "data": data,
        "page": page_obj.number,
        "total_pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous()
    })