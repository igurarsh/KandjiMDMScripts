from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests


# Google Sheet API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Google Sheets API Reference
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = ''


# Getting the required credentials for the API
creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


# Data to be enetered in Sheets 
new_values =[
    # cell values
    ['Serial Number','OS version']
]


# Required APIs constants
getDeviceURL = "APIURL"
API_Token = ""

# Header and payload for the request
payload={}
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer '+API_Token,
}

# Function for getting all the available devices in Kandji
def getDevices():
    response = requests.request("GET", getDeviceURL, headers=headers, data=payload)
    json_data=response.json()
    #counter=1
    for data in json_data:
        try:
            if '10.14' in data['os_version']:
                try:
                    print(data['serial_number'],data['os_version'])
                    new_values.append([data['serial_number'],data['os_version']])
                except:
                    print(data['serial_number'],'N/A')
                    new_values.append([data['serial_number'],'N/A'])
        except:
            print("Error Occured")
        #counter=counter+1
    return exportSheet(new_values)

# Function for exproting data to Google Sheet
def exportSheet(values):
    sheets_service = build('sheets', 'v4', credentials=creds)

    # Sending the data to selected sheet
    body={
        'values': values
    }

    try:
        new_result = sheets_service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME,valueInputOption='RAW', body=body).execute()
        print('Google Sheet Exported Successfully\n')
    except:
            print("Error Occured")
    return 0

# Calling the main function
def main():
    # Calling the APIs requests
    getDevices()


if __name__ == "__main__":
    main()
