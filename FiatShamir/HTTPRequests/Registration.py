from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from Models.FSOtherPK import FSOtherPK
# from Models.FSDevicePK import FSDevicePK
# from Models.FSUser import FSUser
from FiatShamir.models import FSUser, FSDevicePK, FSOtherPK 
import json
import base64
from django.shortcuts import render, get_object_or_404

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            print(json_data)
            protocolType = json_data.get("protocolType")
            payload = json_data.get("payload")
            user_id = json_data.get("userID")
            key = json_data.get("key")
            deviceKey = key.get("device")
            otherKeys = key.get("other")

            n = deviceKey.get("nKey")
            v = deviceKey.get("vKey")
            vKeyInteger=int.from_bytes(base64.b64decode(v), byteorder='big')
            nKeyInteger=int.from_bytes(base64.b64decode(n), byteorder='big')

            user, isNewUser = FSUser.objects.get_or_create(user_id=user_id)

            existingUserDevices = FSDevicePK.objects.filter(user=user)
            deviceIsBindedToUser=False
            for device in existingUserDevices:
                existingVKeyInteger = int.from_bytes(device.v, byteorder='big')
                if existingVKeyInteger==vKeyInteger:
                    deviceIsBindedToUser=True

            if deviceIsBindedToUser:
                return JsonResponse({"error": "User with the specific device exists"}, status=409)
            else:
                nDecoded = base64.b64decode(n)
                vDecoded = base64.b64decode(v)

                # user = FSUser.objects.get_or_create(user_id=user_id)
                deviceKey = FSDevicePK.objects.create(n=nDecoded, v=vDecoded, user=user)

                # otherKeys = []

                for key in otherKeys:
                    print("kkkey:", key)
                    nOtherDecoded=base64.b64decode(key.get("nKey"))
                    vOtherDecoded=base64.b64decode(key.get("vKey"))
                    FSOtherPK.objects.create(n=nOtherDecoded, v=vOtherDecoded, user=user, device=deviceKey)

                return JsonResponse({"message": "User_id successfully binded with the specific device"}, status=200)

        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=400)