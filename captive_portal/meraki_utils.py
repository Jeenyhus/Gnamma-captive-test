import requests
import os


# MERAKI_API_BASE_URL = 'https://api.meraki.com/api/v0'  
# MERAKI_API_KEY = os.environ.get('MERAKI_API_KEY')

# Error Handling 
class MerakiAPIError(Exception):
    """Custom exception for errors encountered with Meraki API interactions."""
    pass

def authenticate_with_meraki(username, password, organization_id):
    """Authenticates a user with the Meraki captive portal API.

    Args:
        username: The user's username.
        password: The user's password.
        organization_id: The ID of the Meraki organization.

    Returns:
        True if authentication is successful, False otherwise.

    Raises:
        MerakiAPIError: If there's an issue with the API request.
    """

    endpoint = '/authenticate'
    url = MERAKI_API_BASE_URL + endpoint

    headers = {'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    payload = {'username': username, 'password': password}

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200: 
        return True
    else:
        raise MerakiAPIError(f"Authentication failed. Status Code: {response.status_code}")

def get_networks(organization_id):
    """Retrieves a list of networks within a Meraki organization.

    Args:
        organization_id: The ID of the Meraki organization.

    Returns:
        A list of networks (likely as dictionaries containing network details).

    Raises:
        MerakiAPIError: If there's an issue with the API request.
    """

    endpoint = f'/organizations/{organization_id}/networks'
    url = MERAKI_API_BASE_URL + endpoint

    headers = {'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise MerakiAPIError(f"Error fetching networks. Status Code: {response.status_code}")