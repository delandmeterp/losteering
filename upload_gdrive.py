from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']


def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)


def upload_file(filename, filename_gdrive):
    service = get_gdrive_service()
    page_token = None
    folders = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                   spaces='drive',
                                   fields='nextPageToken, files(id, name)',
                                   pageToken=page_token).execute()['files']
    found = False
    for f in folders:
        if f['name'] == 'LOSTeering':
            folder_id = f['id']
            found = True
            break
    
        
    if not found:
        print('Error here')
        return
     
    file_metadata = {
        "name": filename_gdrive,
        "parents": [folder_id]
    }
    # upload
    media = MediaFileUpload(filename, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    