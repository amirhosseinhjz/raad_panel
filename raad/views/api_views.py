import json
from django.http import JsonResponse
from raad.UseCases.ValidateSerial import validate_serial_use_case
from raad.UseCases.GenerateLicenseKeyUseCase import generate_license_keys
from django.views.decorators.http import require_POST
from raad.utils import whitelist_ip


@require_POST
def validate_serial(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        device_id = data.get('device_id', '')
        license_key = data.get('license_key', '')

        response = validate_serial_use_case(device_id, license_key)

        return JsonResponse(response)
    except Exception as e:
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=400)


@whitelist_ip
@require_POST
def generate_license_keys_for_client(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        company_id = data.get('company_id', '')
        license_count = data.get('license_count', '')

        response = generate_license_keys(company_id, license_count)

        return JsonResponse(response)
    except Exception as e:
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=400)
