import meraki
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Meraki API
MERAKI_API_KEY = os.getenv('MERAKI_API_KEY')
dashboard = meraki.DashboardAPI(MERAKI_API_KEY)

def create_user(username, password, role, network_id):
    """
    Creates a user on a specified Meraki network.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        role (str): The role to assign to the user (e.g., 'admin', 'observer').
        network_id (str): The ID of the Meraki network where the user will be created.

    Raises:
         Exception: If any errors occur during user creation.
    """

    try:

        # Construct email address
        email = username  # Assuming username can be used as email

        # Create the Meraki network user
        result = dashboard.networks.createNetworkUser(
            network_id, email, name=username, password=password, roles=[role] 
        )

        print("User '{}' created successfully on network '{}'.".format(username, network_id))

    except meraki.exceptions.APIError as e:
        print(f"Meraki API error: {e}")
        raise Exception(f"Failed to create user: {e}") 
    except Exception as e: 
        print(f"General error: {e}")
        raise Exception(f"Failed to create user: {e}") 
    

def authenticate_user_in_network(username, password, network_id):
    """
    Function to authenticate a user in the Meraki network.
    """
    try:
        # Check if the user exists in the network
        users = dashboard.get_network_users(network_id)
        for user in users:
            if user['email'] == username:
                # User found in the network, authenticate
                if user['password'] == password:
                    # Authentication successful
                    return True
                else:
                    # Authentication failed (wrong password)
                    return False
        
        # User not found in the network
        return False
    
    except Exception as e:
        # Handle errors appropriately
        print("Error authenticating user '{}': {}".format(username, str(e)))
        return False
