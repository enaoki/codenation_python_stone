from main import get_temperature
from unittest.mock import patch
import pytest

parametrized_values_equal = [
    (16, -23.599228, -46.605443, 16),
    (-10, -23.655846, -46.527415, -10)
]

parametrized_values_different = [
    (5, 81.255032, -40.539859, 10),
    (-5, 81.255032, -40.539859, -10),
    (-5, 81.255032, -40.539859, 10)
]

parametrized_values_invalid = [
    (26, 'lat', -124.236147, 20),
    (36, 65.219894, 'long', 35),
    (36, 65.219894, None, 35)
]

@pytest.mark.parametrize(
    "temperature_from_api,lat,lng,temperature_result",
    parametrized_values_equal
)
def test_should_be_equal(temperature_from_api, lat, lng, temperature_result):

    temperature = {
        "currently": {
            "temperature": temperature_from_api
        }
    }

    #   replace get function used in get_temperature
    #   more info: https://realpython.com/python-mock-library/
    with patch('main.requests.get') as mock_get:

        #   define mock result
        #   more info: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.return_value
        mock_get.return_value.json.return_value = temperature

        response = get_temperature(lat, lng)

        assert response == temperature_result, "Should be equal"

@pytest.mark.parametrize(
    "temperature_from_api,lat,lng,temperature_result",
    parametrized_values_different
)
def test_should_be_different(temperature_from_api, lat, lng, temperature_result):

    temperature = {
        "currently": {
            "temperature": temperature_from_api
        }
    }

    with patch('main.requests.get') as mock_get:

        mock_get.return_value.json.return_value = temperature

        response = get_temperature(lat, lng)

        assert response != temperature_result, "Should be different"


@pytest.mark.parametrize(
    "temperature_from_api,lat,lng,temperature_result",
    parametrized_values_invalid
)
def test_invalid_input(temperature_from_api, lat, lng, temperature_result):

    temperature = {
        "currently": {
            "temperature": temperature_from_api
        }
    }

    with patch('main.requests.get') as mock_get:

        mock_get.return_value.json.return_value = temperature

        with pytest.raises(TypeError):

            get_temperature(lat, lng)