
MESSENGER_INTEGER_ID = {
    'telegram': 0,
    'bale': 1
}


def get_company_full_data(company):
    return {
        'license': company.license_key,
        'name': company.name,
        'expirationDate': company.expiration_date.strftime("%Y-%m-%d"),
        'subClients': [
            {
                'Name': device.name,
                'SubId': device.id,
                'DeviceId': device.device_id
            } for device in company.devices.all()
        ],
        'messengerUsers': [
            {
                'messengerType': MESSENGER_INTEGER_ID[admin.messenger],
                'accountId': admin.admin_messenger_id
            } for admin in company.admins.all()
        ]
    }
