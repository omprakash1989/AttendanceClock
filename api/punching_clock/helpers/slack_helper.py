"""
Helper module for the Slack notification operations.
"""

from settings import slack_client


class SlackUtil:
    """
    Utility or helper class for slack operations.
    """

    @staticmethod
    def list_channels():
        """List channels available on the slack with details.

        Returns
        -------
            <Dict>: Response dict with all channel list with short info.

            Sample success response:

            {
                "ok": true,
                "channels": [
                    {
                        "id": "C0G9QF9GW",
                        "name": "random",
                        "is_channel": true,
                        "created": 1449709280,
                        "creator": "U0G9QF9C6",
                        "is_archived": false,
                        "is_general": false,
                        "name_normalized": "random",
                        "is_shared": false,
                        "is_org_shared": false,
                        "is_member": true,
                        "is_private": false,
                        "is_mpim": false,
                        "members": [
                            "U0G9QF9C6",
                            "U0G9WFXNZ"
                        ],
                        "topic": {
                            "value": "Other stuff",
                            "creator": "U0G9QF9C6",
                            "last_set": 1449709352
                        },
                        "purpose": {
                            "value": "A place for non-work-related flimflam, faffing, hodge-podge or jibber-jabber you'd prefer to keep out of more focused work-related channels.",
                            "creator": "",
                            "last_set": 0
                        },
                        "previous_names": [],
                        "num_members": 2
                    },
                    {
                        "id": "C0G9QKBBL",
                        "name": "general",
                        "is_channel": true,
                        "created": 1449709280,
                        "creator": "U0G9QF9C6",
                        "is_archived": false,
                        "is_general": true,
                        "name_normalized": "general",
                        "is_shared": false,
                        "is_org_shared": false,
                        "is_member": true,
                        "is_private": false,
                        "is_mpim": false,
                        "members": [
                            "U0G9QF9C6",
                            "U0G9WFXNZ"
                        ],
                        "topic": {
                            "value": "Talk about anything!",
                            "creator": "U0G9QF9C6",
                            "last_set": 1449709364
                        },
                        "purpose": {
                            "value": "To talk about anything!",
                            "creator": "U0G9QF9C6",
                            "last_set": 1449709334
                        },
                        "previous_names": [],
                        "num_members": 2
                    }
                ],
                "response_metadata": {
                    "next_cursor": "dGVhbTpDMUg5UkVTR0w="
                }
            }

            Sample error response:

            {
                "ok": false,
                "error": "invalid_auth"
            }

            None: In case of no response from slack event.
        """

        channels_call = slack_client.api_call("channels.list")
        if channels_call.get('ok'):
            return channels_call['channels']
        return None

    @staticmethod
    def channel_info(channel_id):
        """Get the channel info.

        Parameters
        ----------
        `channel_id` : <String>
            Slack channel id.

        Returns
        -------
            <Dict>: Response dict with channel info.

            Sample success response:

            {
                "ok": true,
                "channel": {
                    "id": "C1H9RESGL",
                    "name": "busting",
                    "is_channel": true,
                    "created": 1466025154,
                    "creator": "U0G9QF9C6",
                    "is_archived": false,
                    "is_general": false,
                    "name_normalized": "busting",
                    "is_shared": false,
                    "is_org_shared": false,
                    "is_member": true,
                    "is_private": false,
                    "is_mpim": false,
                    "last_read": "1503435939.000101",
                    "latest": {
                        "text": "Containment unit is 98% full",
                        "username": "ecto1138",
                        "bot_id": "B19LU7CSY",
                        "attachments": [
                            {
                                "text": "Don't get too attached",
                                "id": 1,
                                "fallback": "This is an attachment fallback"
                            }
                        ],
                        "type": "message",
                        "subtype": "bot_message",
                        "ts": "1503435956.000247"
                    },
                    "unread_count": 1,
                    "unread_count_display": 1,
                    "members": [
                        "U0G9QF9C6",
                        "U1QNSQB9U"
                    ],
                    "topic": {
                        "value": "Spiritual containment strategies",
                        "creator": "U0G9QF9C6",
                        "last_set": 1503435128
                    },
                    "purpose": {
                        "value": "Discuss busting ghosts",
                        "creator": "U0G9QF9C6",
                        "last_set": 1503435128
                    },
                    "previous_names": [
                        "dusting"
                    ]
                }
            }

            Sample error response:

            {
                "ok": false,
                "error": "channel_not_found"
            }

            None: If no response from slack event.
        """

        channel_info = slack_client.api_call("channels.info", channel=channel_id)
        if channel_info:
            return channel_info.get('channel', {})
        return None

    @staticmethod
    def send_message(channel_id='#punching_clock-errors', message='Hi', username='AttendanceClock BOT', icon_emoji=':robot_face:'):
        """Sends slack message to a channel.

        Parameters
        ----------
        `channel_id` : <String>
            Slack channel id.

        `message` : <List>
            Message to be sent.

        `username` : <String>
            Name of slack bot who will notify.

        `msg` : <String>
            Body of the email.

        `icon_emoji` : <String>
            Slack bot Avatar.

        Returns
        -------
            <Dict>: response dict.
            Sample success response:
            {
                "ok": True,
                "channel": "C1H9RESGL",
                "ts": "1503435956.000247",
                "message": {
                    "text": "Some message",
                    "username": "ecto1",
                    "bot_id": "B19LU7CSY",
                    "attachments": [
                        {
                            "text": "This is an attachment",
                            "id": 1,
                            "fallback": "This is an attachment's fallback"
                        }
                    ],
                    "type": "message",
                    "subtype": "bot_message",
                    "ts": "1503435956.000247"
                }
            }

            Sample error response:
            {
                "ok": False,
                "error": "too_many_attachments"
            }
        """

        return slack_client.api_call("chat.postMessage", channel=channel_id, text=message, username=username,
                                     icon_emoji=icon_emoji)
