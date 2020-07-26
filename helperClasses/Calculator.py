from datetime import date


# todo external file for calculation and better with day of date

# This function calculates the current season.
def calculate_current_season():
    today = date.today()
    month = today.strftime("%B")
    if month == ("April" or "May" or "June"):
        return "Frühling"
    elif month == ("July" or "August" or "September"):
        return "Sommer"
    elif month == ("October" or "November" or "December"):
        return "Herbst"
    elif month == ("January" or "February" or "March"):
        return "Winter"


# This function roughly calculates the minutes of the parameter.
def calculate_minutes(slot_duration):
    # years and month aren't really necessary
    years_min = slot_duration["years"] * 60 * 24 * 365
    months_min = slot_duration["months"] * 60 * 24 * 30  # 30.416
    weeks_min = slot_duration["weeks"] * 60 * 24 * 7
    days_min = slot_duration["days"] * 60 * 24
    hours_min = slot_duration["hours"] * 60
    seconds_min = slot_duration["seconds"] / 60

    minutes = years_min + months_min + weeks_min + days_min + hours_min + slot_duration[
        "minutes"] + seconds_min
    # {'kind': 'Duration', 'years': 0, 'quarters': 0, 'months': 0, 'weeks': 0, 'days': 0, 'hours': 2, 'minutes': 0, 'seconds': 0, 'precision': 'Exact'}
    return minutes
