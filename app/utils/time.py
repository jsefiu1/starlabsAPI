from datetime import datetime

unit_to_seconds = {
    "min": 60,
    "orë": 60 * 60,
    "ditë": 60 * 60 * 24,
    "javë": 7 * 60 * 60 * 24,
    "muaj": 60 * 60 * 24 * 30,
}


def string_ago_to_datetime(string_ago: str):
    string_ago = string_ago[3:]
    splited_string = string_ago.split(" ")
    number = int(splited_string[0])
    unit = splited_string[1]

    unit_as_seconds = unit_to_seconds[unit]
    time_stamp_now = datetime.now().timestamp()

    time_stamp_ago = time_stamp_now - (number * unit_as_seconds)

    date_posted = datetime.fromtimestamp(time_stamp_ago)

    return date_posted
