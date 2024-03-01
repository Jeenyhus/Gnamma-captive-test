import os
import meraki
import logging

logger = logging.getLogger(__name__)

MERAKI_API_KEY = os.getenv('MERAKI_API_KEY')
MERAKI_NETWORK_ID = os.getenv('NETWORK_ID')
BASE_URL = 'https://api.meraki.com/api/v1'

def authenticate_with_meraki(email):
    try:
        dashboard = meraki.DashboardAPI(api_key=MERAKI_API_KEY)

        # organization ID
        guests = dashboard.networks.getNetworkGuests(MERAKI_NETWORK_ID) 

        for guest in guests:
            if guest['email'] == email:
                return True

        return False 
    except meraki.APIError as e:
        logger.error(f"Meraki API Error: {e}")
        return False 


def create_meraki_guest_user(user):
    try:
        dashboard = meraki.DashboardAPI(api_key=MERAKI_API_KEY)
        result = dashboard.guests.createNetworkGuest(
            MERAKI_NETWORK_ID,
            user.email,
            password=user.password, 
            name=user.get_full_name() or user.username,
            authorization_zone='Guest Zone'
        )

        if 'id' in result:
            user.meraki_guest_id = result['id']
            user.save()
        else:
            raise Exception("Failed to create Meraki guest user. API Response: {}".format(result))
    except meraki.APIError as e:
        logger.error(f"Meraki API Error: {e}")
        raise Exception("Failed to create Meraki guest user.")
