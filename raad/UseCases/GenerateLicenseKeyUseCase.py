from raad.models import Company, Device
from raad.utils import generate_random_key
from django.db import IntegrityError


def generate_license_keys(company_id, license_count):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return {
            'code': 404,
            'message': 'company not found'
        }

    generated_license_keys = []
    devices_count = company.get_devices_count()
    for _ in range(license_count):
        license_key = generate_license_key(company, devices_count)
        generated_license_keys.append(license_key)

    return {
        'code': 200,
        'message': 'license keys generated successfully',
        'license_keys': generated_license_keys
    }

def generate_license_key(company: Company, device_count):
    device = Device()
    device.name = f'دستگاه شماره {device_count + 1}'
    device.company = company
    device.save()

    return device.license_key
