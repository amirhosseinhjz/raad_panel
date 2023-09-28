import json
from django.http import JsonResponse
from raad.UseCases.ValidateSerial import validate_serial_use_case


def validate_serial(request):
    if request.method != 'POST':
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        device_id = data.get('device_id', '')
        license_key = data.get('license_key', '')

        response = validate_serial_use_case(device_id, license_key)

        return JsonResponse(response)
    except Exception as e:
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=400)

