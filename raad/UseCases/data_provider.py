

def get_company_full_data(company):
    return {
        'license': company.license_key,
        'name': company.name,
        'subClientsCount': company.devices.count(),
        'expirationDate': company.expiration_date,
        'subClients': [
            {
                'Name': device.name,
                'DeviceId': device.device_id
            } for device in company.devices.all()
        ],
        'messengerUsers': [
            {
                'messengerType': admin.messenger,
                'accountId': admin.admin_messenger_id
            } for admin in company.admins.all()
        ]
    }
