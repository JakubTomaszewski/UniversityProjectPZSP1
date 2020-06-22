from astral.geocoder import lookup
from astral.sun import sun


def get_location_info(db, city):
    """Returns an object about a city

    Parameters
    ----------
    :param db: astral geocoder database
    :param city: str
        city name

    :return: astral LocationInfo object info about the city
    """

    db = db
    try:
        return lookup(city, db)
    except KeyError:
        print(f'{city} not found')


def display_city_info(city):
    """Displays info about a city

    Parameters
    ----------
    :param city: str
        city name
    """

    print(f'''City name: {city.name}
Region: {city.region}
Timezone: {city.timezone}
Lat {city.latitude:.02f}
Long {city.longitude:.02f}''')


def get_sun_info(city, dt):
    """Returns an object with sun info on a specific date

    Parameters
    ----------
    :param city: str
        city name
    :param dt: date in datetime.date format

    :return: astral sun info object from a specific city
    """

    return sun(city.observer, date=dt, tzinfo=city.timezone)


def check_after_sunset(sunrise_hour, sunset_hour, now_hour):
    """Checks the sun phase

    Parameters
    ----------
    :param sunrise_hour: int
    :param sunset_hour: int
    :param now_hour: int

    :return: True
        if it is after the sunset
    :return: False
        if it is before the sunset
    """

    if sunset_hour < now_hour <= 24 or 0 <= now_hour < sunrise_hour:
        # print('After sunset, complete darkness')
        return True
    else:
        # print('After sunrise, sun is shining')
        return False
