# RA, 2021-05-18

# https://stackoverflow.com/questions/64570647/google-drive-api-python-service-account-example
# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
# https://developers.google.com/sheets/api/quickstart/python

import itertools
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
KEY_FILE_LOCATION = 'nct1-20210518-24b395f048ea.json'

creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1rr0lp6ByU1bENysPyk0qLXYwMEmwEN0BVQYw7H2Hp30'
SAMPLE_RANGE_NAME = 'Sheet1!A1:ZZ'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()

print(pd.DataFrame(itertools.zip_longest(*result['values'], fillvalue='')).T)

