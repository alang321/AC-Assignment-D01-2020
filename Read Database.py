import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def getdata(sheetname):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('Google API credentials.json', scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open(sheetname)

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    records_data = sheet_instance.get_all_records()

    # convert the json to dataframe
    records_df = pd.DataFrame.from_dict(records_data)

    # view the top records
    return records_df


print(getdata('Aircraft Reference Database'))