import requests
import os

# File to store the downloaded envelope IDs
ENVELOPE_LOG_FILE = "downloaded_envelopes.txt"
TOKEN_FILE = "token.txt"  # Path to the file containing the access token

def get_downloaded_envelopes():
    if os.path.exists(ENVELOPE_LOG_FILE):
        with open(ENVELOPE_LOG_FILE, 'r') as file:
            downloaded_envelopes = file.read().splitlines()
    else:
        downloaded_envelopes = []
    return set(downloaded_envelopes)

def save_downloaded_envelope(envelope_id):
    with open(ENVELOPE_LOG_FILE, 'a') as file:
        file.write(f"{envelope_id}\n")

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

def get_signed_envelopes():
    access_token = load_access_token()
    account_id = '29035884'

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"
    params = {
        "from_date": "2023-09-10T00:00:00Z",
        "status": "completed"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        envelopes = response.json().get('envelopes', [])
        return envelopes
    else:
        print(f"Error fetching envelopes: {response.status_code}")
        return []

def download_pdf(envelope_id):
    access_token = load_access_token()
    url = f'https://demo.docusign.net/restapi/v2.1/accounts/29035884/envelopes/{envelope_id}/documents/combined'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Save the PDF with the envelope ID as the filename
        file_path = f'/Users/vladbuzhor/downloads/completed_envelopes/{envelope_id}.pdf'
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"PDF for envelope {envelope_id} downloaded successfully!")
        return True
    else:
        print(f"Failed to download PDF for envelope {envelope_id}: {response.status_code}")
        return False

def process_envelopes():
    downloaded_envelopes = get_downloaded_envelopes()
    signed_envelopes = get_signed_envelopes()

    for envelope in signed_envelopes:
        envelope_id = envelope['envelopeId']
        if envelope_id not in downloaded_envelopes:
            print(f"Downloading PDF for new envelope: {envelope_id}")
            if download_pdf(envelope_id):
                save_downloaded_envelope(envelope_id)
        else:
            print(f"Envelope {envelope_id} already downloaded. Skipping...")

# Execute the envelope processing function
process_envelopes()
