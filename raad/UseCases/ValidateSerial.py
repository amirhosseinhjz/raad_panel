from raad.models import Device, Company


def validate_license_key_use_case(sub_id, device_id, license_key):
    company = Company.objects.filter(license_key=license_key).first()
    if company is None:
        return {
                'code': -1,
                'message': 'invalid DeviceId or LicenseKey'
        }

    device = Device.objects.filter(company=company).filter(sub_id=sub_id).first()

    if device is None:
        return {
                'code': -1,
                'message': 'invalid DeviceId or LicenseKey'
        }

    if company.has_expired() or (device.device_id and (device.device_id != device_id)):
        return {
                'code': 1,
                'message': 'LicenseKey has expired or used.'
        }

    device.device_id = device_id
    device.save()
    return {
            'code': 0,
            'message': 'License is valid!'
    }
