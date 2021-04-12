import urllib.request
import json

def strip_timeframe(message_text):
    if " 7day" in message_text:
        return "7day", message_text.replace(" 7day", "")
    elif " 7 day" in message_text:
        return "7day", message_text.replace(" 7 day", "")
    elif " 1week" in message_text:
        return "7day", message_text.replace(" 1week", "")
    elif " 1 week" in message_text:
        return "7day", message_text.replace(" 1 week", "")

    elif " 1month" in message_text:
        return "1month", message_text.replace(" 1month", "")
    elif " 1 month" in message_text:
        return "1month", message_text.replace(" 1 month", "")
    elif " 30day" in message_text:
        return "1month", message_text.replace(" 30day", "")
    elif " 30 day" in message_text:
        return "1month", message_text.replace(" 30 day", "")

    elif " 3month" in message_text:
        return "3month", message_text.replace(" 3month", "")
    elif " 3 month" in message_text:
        return "3month", message_text.replace(" 3 month", "")

    elif " 6month" in message_text:
        return "6month", message_text.replace(" 6month", "")
    elif " 6 month" in message_text:
        return "6month", message_text.replace(" 6 month", "")

    elif " 1year" in message_text:
        return "12month", message_text.replace(" 1year", "")
    elif " 1 year" in message_text:
        return "12month", message_text.replace(" 1 year", "")
    elif " 12month" in message_text:
        return "12month", message_text.replace(" 12month", "")
    elif " 12 month" in message_text:
        return "12month", message_text.replace(" 12month", "")

    elif " overall" in message_text:
        return "overall", message_text.replace(" overall", "")
    elif " over all" in message_text:
        return "overall", message_text.replace(" over all", "")

    else:
        return None, message_text

def strip_double_spaces(message_text):
    return ' '.join(message_text.split())

def strip_command(prefix, message_text, command):
    return message_text.lower().replace(f"{prefix}{command}", "", 1)

def get_size_username(message_text):
    size, username = None, None
    for segment in message_text.split(" "):
        if segment.isdigit():
            size = int(segment)
        else:
            username = str(segment)
    return size, username

def validate_username(username, API_KEY):
    url = "https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user="+username+"&api_key="+API_KEY+"&format=json"
    try:
        with urllib.request.urlopen(url) as url:
            data = json.load(url)   # loaded as dict
        data = data.get("user").get("name")
        return data
    except urllib.error.HTTPError:
        return None
