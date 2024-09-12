import os
import requests

def load_config(file_path):
    """Load DocuSign client ID and secret from the configuration file."""
    config = {}
    if not os.path.exists(file_path):
        raise Exception(f"Configuration file not found: {file_path}")

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split('=')
            config[key] = value
    return config


# File paths for tokens
TOKEN_FILE = 'token.txt'
DOCUSIGN_CONFIG_FILE = 'docusign_config.txt'  # Path to the file containing client ID and secret
config = load_config(DOCUSIGN_CONFIG_FILE)

def load_access_token():
    """Load the access token from the token.txt file."""
    if not os.path.exists(TOKEN_FILE):
        raise Exception(f"Token file not found: {TOKEN_FILE}")

    with open(TOKEN_FILE, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("token="):
                return line.split('=')[1].strip()
    raise Exception("Access token not found in the token file")

def send_envelop(template_choice=None):
    if not template_choice:
        # Default value if no template is passed
        template_choice = input("Enter template choice (1 for Template 1, 2 for Template 2): ")

    # Load the access token from the file
    access_token = load_access_token()

    # Determine template ID
    if template_choice == "1":
        template_id = "17cc51e1-5433-4576-98bb-7c60bde50bbd"  # Template 1 ID
    elif template_choice == "2":
        template_id = "fc1fa3af-f87d-4558-aa10-6b275852c78e"  # Template 2 ID
    else:
        print("Invalid template selection.")
        return
    
    # Retrieve account ID from the config dictionary
    account_id = config['ACCOUNT_ID']
    url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"
    
    payload = {
        "templateId": template_id,
        "status": "sent"  # Send the envelope immediately
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Send the envelope
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("Envelope sent successfully!")
    else:
        print(f"Error sending envelope: {response.json()}")

# Call the function to send the envelope
send_envelop()
