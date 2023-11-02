from raad.models import Device


def validate_license_key_use_case(_id, device_id, license_key):
    device = Device.objects.filter(id=_id).first()

    if device is None or device.company.license_key != license_key:
        return {
                'code': -1,
                'message': 'invalid DeviceId or LicenseKey'
        }

    if device.company.has_expired() or (device.device_id and (device.device_id != device_id)):
        return {
                'code': 1,
                'message': 'LicenseKey has expired'
        }

    device.device_id = device_id
    device.save()
    return {
            'code': 0,
            'message': 'License is valid!'
    }
