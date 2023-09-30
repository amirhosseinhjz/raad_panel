from raad.models import Device


def validate_serial_use_case(device_id, license_key):
    device = Device.objects.filter(id=device_id).first()
    company = device.company

    if device is None or company.license_key != license_key:
        return {
                'code': -1,
                'message': 'invalid DeviceId or LicenseKey'
        }

    if company.has_expired() or device.is_activated:
        return {
                'code': 1,
                'message': 'LicenseKey has expired'
        }

    device.is_activated = True
    device.save()
    return {
            'code': 0,
            'message': 'License is valid!'
    }
