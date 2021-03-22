import requests
import json

graph_url = 'https://graph.microsoft.com/v1.0'


def get_user(token):
    # Send GET to /m

    user = requests.get(
        '{0}/me'.format(graph_url),
        headers={
            'Authorization': 'Bearer {0}'.format(token)
        },
        params={
            '$select': 'displayName,mail, mailboxSettings, userPrincipalName'
        })
    return user.json()


def create_event(token, subject, start, end, reminder, body=None, timezone='UTC'):
    # Create an event object
    # https://docs.microsoft.com/graph/api/resources/event?view=graph-rest-1.0
    new_event = {
        'subject': subject,
        'start': {
            'dateTime': start,
            'timeZone': timezone
        },
        'end': {
            'dateTime': end,
            'timeZone': timezone
        },
        'isReminderOn': True,
        'reminderMinutesBeforeStart': reminder,
        "attendees": [
            {
                "emailAddress": {
                    "address": "appeals@srgroupllc.com",
                    "name": "Appeals"
                },
                "type": "optional"
            }
        ]
    }

    #     if attendees:
    #       attendee_list = ['appeals@srgroupllc.com']
    #       for email in attendees:
    #           # Create an attendee object
    #           # https://docs.microsoft.com/graph/api/resources/attendee?view=graph-rest-1.0
    #           attendee_list.append({
    #               'type': 'required',
    #               'emailAddress': {'address': email}
    #           })

    #       new_event['attendees'] = attendee_list

    if body:
        # Create an itemBody object
        # https://docs.microsoft.com/graph/api/resources/itembody?view=graph-rest-1.0
        new_event['body'] = {
            'contentType': 'text',
            'content': body
        }

    # Set headers
    headers = {
        'Authorization': 'Bearer {0}'.format(token),
        'Content-Type': 'application/json'
    }

    requests.post('{0}/me/events'.format(graph_url),
                  headers=headers,
                  data=json.dumps(new_event, default=str))
