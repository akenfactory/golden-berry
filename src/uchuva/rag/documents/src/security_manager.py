#------------------------------------------
# Import the necessary modules
#------------------------------------------

import os
import requests

#------------------------------------------
# Define variables and constants
#------------------------------------------

# Define security manager url
SECURITY_MANAGER_URL = os.getenv('SECURITY_MANAGER_URL', 'http://0.0.0.0:5002/alive')

#------------------------------------------
# Define commons functions
#------------------------------------------

def check_accsess(token):
    """Realiza una peticion POST."""
    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {token}"}
    response = requests.post(SECURITY_MANAGER_URL, headers=headers)
    if response.status_code == 200:
        return True
    if response.status_code == 401 or 422:
        return False
    # Si no es 200 ni 401, lanzamos una excepcion
    response.raise_for_status()