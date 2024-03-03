import os
import json
# using defaultdict to create a dictionary with default values for keys that haven't been set yet
from collections import defaultdict
from datetime import datetime, timedelta
import meraki
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Meraki client
meraki_dashboard = meraki.DashboardAPI(os.getenv("MERAKI_API_KEY"))

def fetch_organization_data():
    """
    Fetches organizations and their networks from the Meraki API and stores them in a dictionary.
    Returns:
        dict: Dictionary containing organization data.
    """
    data = defaultdict(lambda: defaultdict(list))
    orgs = meraki_dashboard.organizations.getOrganizations()
    for org in orgs:
        # Create a dictionary with organization ID as the key
        data[org['id']] = {'name': org['name'], 'networks': []}
        # Fetch networks for each organization
        networks = meraki_dashboard.organizations.getOrganizationNetworks(org['id'])
        # Add the networks to the dictionary
        data[org['id']]['networks'] = networks
    return data

def createUser(network_id, email):
    """
    Create a user on the network.
    Args:
        network_id (str): ID of the network.
        email (str): Email of the user.
    Returns:
        dict: Response from the Meraki API.
    """
    try:
        # Define the expires_at variable
        expires_at = (datetime.now() + timedelta(minutes=3650)).isoformat() + 'Z'
        # Create the user on the network using the Meraki API
        response = meraki_dashboard.networks.createNetworkMerakiAuthUser(
            network_id, email, [],
            name='Ziebra',  
            password='xyz123', 
            accountType='802.1X',
            emailPasswordToUser=True, 
            isAdmin=False
        )
        # Return the response from the API
        return response
    except meraki.APIError as e:
        for error in e.message["errors"]:
            print("+ ", error)

def getUser(network_id):
    """
    Get users from the network.
    Args:
        network_id (str): ID of the network.
    Returns:
        list: List of users.
    """
    return meraki_dashboard.networks.getNetworkMerakiAuthUsers(network_id)

def deleteUser(network_id, user_id):
    """
    Delete a user from the network.
    Args:
        network_id (str): ID of the network.
        user_id (str): ID of the user to be deleted.
    """
    meraki_dashboard.networks.deleteNetworkMerakiAuthUser(network_id, user_id)

def main():
    # Fetch organization data from the Meraki API
    data = fetch_organization_data()
    if not data:
        print("No organizations found")
        return
    
    # Extract network ID from the fetched data and select the first network
    org_id = list(data.keys())[0]
    network_id = data[org_id]['networks'][0]['id']
    
    # Set email for the user to be created on the network 
    email = 'dmweemba@edulution.org'
    
    # Create a user on the network using the Meraki API
    try:
        response = createUser(network_id, email)
        # Print the response from the API to the console
        print("User created:", response)
    except meraki.APIError as e:
        # Print the error message to the console if an error occurs during the API call
        for error in e.message["errors"]:
            print("+ ", error)
    
    # Get users from the network
    users = getUser(network_id)
    if users:
        # Print the users to the console in a readable format using the json module
        print("Users:", json.dumps(users, indent=2))
    else:
        print("No users found")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()