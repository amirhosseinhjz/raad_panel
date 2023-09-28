from raad.models import Device
# from django.core.exceptions import ObjectDoesNotExist


def validate_serial_use_case(device_id, license_key):
    device = Device.objects.filter(id=device_id).first()

    if device is None or device.license_key != license_key:
            return {
                    'code': -1,
                    'message': 'invalid DeviceId or LicenseKey'
            }

    if device.company.has_expired():
            return {
                    'code': 1,
                    'message': 'LicenseKey has expired'
            }

    return {
            'code': 0,
            'message': 'License is valid!'
    }
