from __future__ import print_function
import httplib2
import os
import json
from apiclient import discovery
from oauth2client import *
from oauth2client.file import Storage


import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    count = 0
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=30, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])


    # name_events, start_times, end_times will hold each piece of data by index
    name_events = []
    start_times = []
    end_times = []
    locations_events = []
    break_times = []
    dates_events = []
    dates = []


    start_events = []
    end_events = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_events.append((start, event['summary']))

        end = event['end'].get('dateTime', event['end'].get('date'))
        end_events.append((end, event['summary']))
        if event.get('location') is not None:
            locations_events.append(event.get('location'))
        else:
            locations_events.append('N/A')
        dates_events.append(event['start'].get('dateTime'))



    for i in start_events:
        name_events.append((start_events[count][1]))
        start_times.append((start_events[count][0][11:-9]))
        end_times.append((end_events[count][0][11:-9]))
        dates.append(dates_events[count][:-15])
        count += 1

    '''print(name_events)
    print('\n')
    print(start_times)
    print('\n')
    print(end_times)
    print('\n')
    print(locations_events)'''

    data = {'events': name_events, 'start': start_times, 'end': end_times, 'loc': locations_events, 
            'dates': dates}
    '''print(data)
    with open('cal_data.json', 'w') as outfile:
        json.dump(data, outfile)'''
    credentials.revoke(httplib2.Http())
    print(data)

if __name__ == '__main__':
    main()
