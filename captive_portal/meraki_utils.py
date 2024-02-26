import meraki
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Meraki API
MERAKI_API_KEY = os.getenv('MERAKI_API_KEY')
dashboard = meraki.DashboardAPI(MERAKI_API_KEY)

def get_organization_id():
    """Retrieves the organization ID."""
    try:
        organizations = dashboard.organizations.getOrganizations()
        if organizations:
            return organizations[0]['id']
        else:
            return None
    except meraki.APIError as e:
        print(f"Failed to fetch organization ID: {e}")
        return None

def get_network_id(organization_id, network_name):
    """Retrieves the network ID given the organization ID and network name."""
    try:
        networks = dashboard.organizations.getOrganizationNetworks(organization_id)
        for network in networks:
            if network['name'] == network_name:
                return network['id']
        return None
    except meraki.APIError as e:
        print(f"Failed to fetch network ID: {e}")
        return None

def get_network_name(organization_id, network_id):
    """Retrieves the network name given the organization ID and network ID."""
    try:
        network = dashboard.networks.getNetwork(organization_id, network_id)
        return network['name'] if network else None
    except meraki.APIError as e:
        print(f"Failed to fetch network name: {e}")
        return None

def authenticate_meraki_user(network_id, email, password):
    """Authenticates a Meraki authentication user."""
    try:
        payload = {
            'email': email,
            'password': password
        }
        response = dashboard.networks.getNetworkMerakiAuthUser(network_id, email)
        if response:
            return True
        else:
            return False
        
    except meraki.APIError as e:
        print(f"Failed to authenticate Meraki Auth user: {e}")
        return False 

def grant_network_access(user, network_name):
    """Grants network access to a user, creating a new Meraki Auth User if needed."""
    try:
        # Fetch organization ID
        organization_id = get_organization_id()

        # Fetch network ID
        network_id = get_network_id(organization_id, network_name)

        if not network_id:
            print("Network not found.")
            return False

        # First, attempt to authenticate to see if the user exists
        if authenticate_meraki_user(network_id, user['email'], user['password']):
            print("User is already authenticated.")
            return True

        # If not, then create a new user
        response = dashboard.networks.createNetworkMerakiAuthUser(
            network_id, 
            user['email'],
            user['name'],
            password=user['password'] 
        )
        
        if response:
            print("Meraki Auth User created successfully.")
            return True
        else:
            print("Failed to create Meraki Auth User.")
            return False

    except meraki.APIError as e:
        print(f"Failed to grant network access: {e}")
        return False


def revoke_network_access(user, network_name):
    """Revokes network access from a user."""
    try:
        organization_id = get_organization_id()
        network_id = get_network_id(organization_id, network_name)

        if not network_id:
            print("Network not found.")
            return False

        response = dashboard.networks.deleteNetworkMerakiAuthUser(network_id, user['email'])
        if response:
            return True
        else:
            return False
    except meraki.APIError as e:
        print(f"Failed to revoke network access: {e}")
        return False
