import json
from django.http import JsonResponse
from raad.UseCases.ValidateSerial import validate_license_key_use_case
from django.views.decorators.http import require_POST
from raad.utils import whitelist_ip
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from raad.models import Company
from raad.utils import normalize_phone
from raad.UseCases.data_provider import get_company_full_data


@csrf_exempt
@require_POST
def validate_license_key(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        sub_id = data.get('sub_id', '')
        device_id = data.get('device_id', '')
        license_key = data.get('license_key', '')

        response = validate_license_key_use_case(sub_id, device_id, license_key)

        return JsonResponse(response)
    except Exception as e:
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=400)


@csrf_exempt
@require_POST
def get_user_companies(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        phone_number = data.get('phone_number', '')
        phone_number = normalize_phone(phone_number)

        user = User.objects.get(username=phone_number)

        companies = Company.objects.filter(user=user)

        data = [{'id': company.id, 'name': company.name} for company in companies]

        return JsonResponse({'phone_number': phone_number, 'data': data})
    except Exception as e:
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=400)


@csrf_exempt
@whitelist_ip
def get_full_companies_data(request):
    try:
        companies = Company.get_all_active()

        data = []

        for company in companies:
            data.append(get_company_full_data(company))

        return JsonResponse({'data': data})
    except Exception as e:
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=400)


@csrf_exempt
@require_POST
def get_company_not_activated_devices(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        license_key = data.get('license_key', '')
        device_id = data.get('device_id', '')

        company = Company.objects.filter(license_key=license_key).first()
        if company is None:
            return JsonResponse({
                'code': -1,
                'message': 'invalid LicenseKey'
            })

        response = {
            'license_key': license_key,
            'devices': [
                {'sub_id': str(device.sub_id), 'name': str(device.name)}
                for device in company.devices.all() if (not device.device_id or device.device_id == device_id)]
        }

        return JsonResponse({'data': response})

    except Exception as e:
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=400)
