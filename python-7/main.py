import requests


def get_temperature(lat, lng):
    if type(lat) != float or type(lng) != float:
        raise TypeError("{0}/{1} invalid".format(lat, lng))

    key = 'e1ee55658d4a2b28c4841e373c3b3d87'
    #   define Système international as default
    #   no need to convert from fahrenheit
    unit = 'si'
    url = 'https://api.darksky.net/forecast/{}/{},{}?unit={}'.format(key, lat, lng, unit)
    reponse = requests.get(url)
    data = reponse.json()
    temperature = data.get('currently').get('temperature')
    if not temperature:
        return
    return temperature
